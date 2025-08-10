# YouTube Transcript Q&A Chatbot

A **Streamlit-based** application that fetches **YouTube video transcripts** and answers user questions using a **chat-like interface**, powered by **OpenAI embeddings**, **FAISS vector storage**, and **GPT-4**.

## Features

- **Transcript Retrieval**: Fetches English auto-generated transcripts from YouTube videos.
- **Embedding & Retrieval**: Uses OpenAI embeddings and FAISS for efficient transcript storage and retrieval.
- **Chat Interface**: Provides a modern, chat-like UI with message history for user questions and bot responses.
- **Error Handling**: Gracefully handles cases like missing or disabled transcripts.

## Prerequisites

- **Python 3.8** or higher
- **OpenAI API key** (set in `.env` file as `OPENAI_API_KEY`)
- **Git** for cloning the repository
- **GitHub account** for hosting

## Installation

### Clone the Repository:

```bash
git clone <https://github.com/mnabeelasad/Youtube-Video-Transcript-Questions-Answer.git>
cd <Youtube-Video-Transcript-Questions-Answer>
```

## Output Examples

### Generated Text Example

![YouTube Transcript Q&A Interface](https://github.com/mnabeelasad/Youtube-Video-Transcript-Questions-Answer/blob/master/assets/ss_ui.png)
