from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain_core.prompts import PromptTemplate
from youtube_transcript_api import YouTubeTranscriptApi, NoTranscriptFound, TranscriptsDisabled
import pickle
from langchain.docstore.document import Document
from langchain.chains import LLMChain
from langchain_openai import ChatOpenAI
import faiss
from langchain_core.runnables import RunnableParallel, RunnableLambda, RunnablePassthrough
from dotenv import load_dotenv

load_dotenv()

def process_transcript_and_query(video_id, query):
    try:
        # Fetch English auto-generated transcript
        api = YouTubeTranscriptApi()
        data = api.fetch(video_id, languages=["en"])
        transcript_text = " ".join(chunk.text for chunk in data)

        # Embeddings
        embeddings = OpenAIEmbeddings()

        # Create embeddings for the transcript text
        embedding_result = embeddings.embed_documents([transcript_text])

        document = Document(page_content=transcript_text)

        # Save documents.pkl file after creating it
        with open('documents.pkl', 'wb') as f:
            pickle.dump([document], f)

        # Create FAISS index
        faiss_index = FAISS.from_documents([document], embeddings)

        # Save the FAISS index to disk
        faiss.write_index(faiss_index.index, 'faiss_index.index')

        # Save the index_to_docstore_id mapping to disk
        index_to_docstore_id = faiss_index.index_to_docstore_id
        with open('index_to_docstore_id.pkl', 'wb') as f:
            pickle.dump(index_to_docstore_id, f)

        # Load the FAISS index from disk
        loaded_index = faiss.read_index('faiss_index.index')

        # Load the documents
        with open('documents.pkl', 'rb') as f:
            documents = pickle.load(f)

        # Load the index-to-docstore mapping
        with open('index_to_docstore_id.pkl', 'rb') as f:
            index_to_docstore_id = pickle.load(f)

        # Recreate the FAISS object with the loaded index, documents, and mapping
        loaded_faiss_index = FAISS(
            index=loaded_index,
            docstore=documents,
            index_to_docstore_id=index_to_docstore_id,
            embedding_function=embeddings
        )

        # Convert FAISS index into a retriever
        retriever = faiss_index.as_retriever(search_type="similarity", search_kwargs={"k": 1})

        # LLM Setup
        llm = ChatOpenAI(model="gpt-4", temperature=0.2)

        # Prompt template for answering questions based on the context
        prompt_template = """
        You are a helpful assistant.
        Answer ONLY from the provided transcript context.
        If the context is insufficient, just say you don't know.
        {context}
        Question: {question}
        """

        # Create the prompt template
        prompt = PromptTemplate(template=prompt_template, input_variables=["context", "question"])

        # LLM Chain
        llm_chain = LLMChain(prompt=prompt, llm=llm)

        def format_docs(retrieved_docs):
            context_text = "\n\n".join(doc.page_content for doc in retrieved_docs)
            return context_text

        # Create a chain using RunnableParallel
        parallel_chain = RunnableParallel({
            'context': retriever | RunnableLambda(format_docs),
            'question': RunnablePassthrough()
        })

        # Query the retriever
        results = retriever.get_relevant_documents(query)

        # Extract relevant context from the retriever results
        context = "\n".join([result.page_content for result in results])

        # Generate the response using the LLM chain
        response = llm_chain.run({"context": context, "question": query})

        return response

    except NoTranscriptFound as e:
        raise Exception(f"Transcript not found: {e}")
    except TranscriptsDisabled:
        raise Exception("Transcripts are disabled for this video")
    except Exception as e:
        raise Exception(f"An error occurred: {e}")