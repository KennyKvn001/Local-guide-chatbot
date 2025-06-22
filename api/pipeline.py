from langchain_core._api.deprecation import LangChainDeprecationWarning
import warnings
import os

os.environ["TOKENIZERS_PARALLELISM"] = "false"

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
import csv
from langchain.schema import Document

load_dotenv()


def initialize_rag_pipeline(
    text_paths: list[str] = ["cleaned_rwanda_data.txt", "data.txt", "data.txt"],
    csv_path: str = "rwanda_qa_cleaned.csv",
):
    """Initialise the RAG components using **both** a plain-text corpus and
    the structured Q&A CSV dataset.

    Parameters
    ----------
    text_path : str
        Path to a `.txt` knowledge file (optional).
    csv_path : str
        Path to the `rwanda_qa_cleaned.csv` file containing `question` / `answer` columns.
    """

    documents = []

    # 1. Plain text corpus (if present)
    for text_path in text_paths:
        if os.path.exists(text_path):
            loader = TextLoader(text_path)
            documents.extend(loader.load())

    # 2. CSV Q&A pairs → individual Documents
    if os.path.exists(csv_path):
        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                qa_pair = f"Question: {row['question']}\nAnswer: {row['answer']}"
                documents.append(
                    Document(
                        page_content=qa_pair,
                        metadata={"domain": row.get("domain", "")},
                    )
                )

    # Split into overlap-aware chunks for embedding
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
        model_name="mistralai/Mistral-7B-Instruct-v0.2",
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        temperature=0.0,
        max_tokens=500,
    )

    print("Docs indexed:", len(vector_store.get()))

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
            "events, travel tips and more. Ask me anything from 'What's the best time to visit Nyungwe?' to 'Where can I get a SIM card in Kigali?' and I'll do my best to help."
        )

    # Check for specific questions about places to visit in Kigali
    if "where can I visit in Kigali" in query.lower():
        return "You can visit the Kigali Genocide Memorial, Camp Kigali Museum, and local markets."

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
        "Kinyarwanda",
        "Umurage",
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

    # Retrieve relevant documents (more chunks improves coverage)
    docs = vector_store.similarity_search(query, k=5)
    context = "\n".join([doc.page_content for doc in docs])

    # Generate response
    system_msg = (
        "You are LocalGuide, a knowledgeable assistant **only** about Rwanda. "
        "Answer using *exclusively* the information provided in the context. "
        'If the context does not contain the answer, reply with "I don\'t know based on the information I have." Do not invent facts. '
        "Keep your responses concise and to the point."
    )

    human_prompt = f"Context:\n{context}\n\n" f"Question: {query}\n" "Answer:"

    message = [
        SystemMessage(content=system_msg),
        HumanMessage(content=human_prompt),
    ]
    response = llm.invoke(message)
    return response.content
