from langchain_core._api.deprecation import LangChainDeprecationWarning
import warnings

# from langchain_core._api.deprecation import LangChainDeprecationWarning

warnings.filterwarnings("ignore", category=LangChainDeprecationWarning)
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
import os
from dotenv import load_dotenv

load_dotenv()


def initialize_rag_pipeline(data_path="cleaned_rwanda_data.txt"):
    # Load the dataset
    loader = TextLoader(data_path)
    documents = loader.load()

    # Split documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_documents(documents)

    # Initialize embeddings
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Store chunks in ChromaDB
    vector_store = Chroma.from_documents(
        chunks, embeddings, persist_directory="./chroma_db"
    )
    vector_store.persist()

    # Initialize LLM (placeholder; replace with Grok API or other LLM)
    llm = ChatOpenAI(
        model_name="mistralai/Mistral-7B-Instruct-v0.2",  # pick any model OpenRouter offers
        base_url="https://openrouter.ai/api/v1",  # OpenRouter endpoint
        api_key=os.getenv("OPENROUTER_API_KEY"),
        temperature=0.3,
        max_tokens=500,
    )

    return vector_store, llm


def query_rag(vector_store, llm, query):
    # Respond to simple greetings immediately
    greetings = [
        "hi",
        "hello",
        "hey",
        "greetings",
        "good morning",
        "good afternoon",
        "good evening",
    ]
    if query.lower().strip() in greetings:
        return "Hello! 👋 I'm LocalGuide, your friendly chatbot for everything about Rwanda. How can I help you today?"

    # Respond to questions about capabilities
    capability_phrases = [
        "what can you do",
        "what do you do",
        "how can you help",
        "what help can you assist",
        "how can you assist",
        "what services do you offer",
    ]
    if any(phrase in query.lower() for phrase in capability_phrases):
        return (
            "I can answer questions about Rwanda—its culture, history, attractions, transportation, local customs, "
            "events, travel tips and more. Ask me anything from ‘What's the best time to visit Nyungwe?’ to 'Where can I get a SIM card in Kigali?' and I'll do my best to help."
        )

    # Check if query is Rwanda-related (simple keyword check)
    rwanda_keywords = [
        "rwanda",
        "kigali",
        "genocide",
        "genocide memorial",
        "nyungwe forest",
        "akagera",
        "kibungo",
        "kibuye",
        "ingagi",
        "lake kivu",
        "umuganura",
        "volcanoes",
        "education",
        "hospital",
        "tourism",
        "sports",
        "culture",
        "history",
        "economy",
        "politics",
        "environment",
    ]
    if not any(keyword in query.lower() for keyword in rwanda_keywords):
        return "I'm focused on Rwanda-related information. Please ask about Rwanda's destinations, culture, history or travel logistics and I'll gladly help!"

    # Retrieve relevant documents
    docs = vector_store.similarity_search(query, k=3)
    context = "\n".join([doc.page_content for doc in docs])

    # Generate response
    prompt = f"Answer the following question about Rwanda based on the context:\nContext: {context}\nQuestion: {query}\nAnswer:"
    message = [
        SystemMessage(
            content="You are a helpful assistant that can answer questions about Rwanda."
        ),
        HumanMessage(content=prompt),
    ]
    response = llm.invoke(message)
    return response.content
