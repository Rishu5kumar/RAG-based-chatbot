import os
import streamlit as st
import google.generativeai as genai
from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
from langchain.schema import Document
from gensim.models import Word2Vec
import numpy as np
from scipy import triu
import nltk
from nltk.tokenize import word_tokenize
from pypdf import PdfReader

# Download missing tokenizer
nltk.download('punkt_tab')

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("API_KEY"))

# Function to extract text from files
def extract_text_from_file(uploaded_file):
    """Extracts text from TXT, PDF, or DOCX files."""
    if uploaded_file.type == "text/plain":
        return uploaded_file.read().decode("utf-8")
    elif uploaded_file.type == "application/pdf":
        reader = PdfReader(uploaded_file)
        return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    else:
        return ""

# Function to process document text
def process_text(text):
    """Splits long text into smaller chunks for better retrieval."""
    text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = text_splitter.split_text(text)
    return [Document(page_content=chunk) for chunk in chunks]

# Function to train Word2Vec model
def train_word2vec(documents):
    """Trains a Word2Vec model on tokenized document data."""
    sentences = [word_tokenize(doc.page_content.lower()) for doc in documents]
    model = Word2Vec(sentences, vector_size=100, window=5, min_count=1, workers=4)
    return model

# Function to compute similarity using Word2Vec
def retrieve_relevant_context(query, model, documents):
    """Finds the most relevant text chunks for the given query."""
    query_tokens = word_tokenize(query.lower())
    doc_scores = []

    for doc in documents:
        doc_tokens = word_tokenize(doc.page_content.lower())
        similarity_scores = []

        for word in query_tokens:
            if word in model.wv:
                word_vector = model.wv[word]
                doc_vectors = [model.wv[w] for w in doc_tokens if w in model.wv]

                if doc_vectors:
                    avg_doc_vector = np.mean(doc_vectors, axis=0)
                    similarity = np.dot(word_vector, avg_doc_vector) / (np.linalg.norm(word_vector) * np.linalg.norm(avg_doc_vector))
                    similarity_scores.append(similarity)

        doc_scores.append((doc, np.mean(similarity_scores) if similarity_scores else 0))

    top_docs = sorted(doc_scores, key=lambda x: x[1], reverse=True)[:2]  # Get top 2 docs
    return "\n".join([doc[0].page_content for doc in top_docs if doc[1] > 0])

# Function to generate response using Gemini
def generate_response(user_query, model, documents):
    """Generates a user-friendly response using Gemini with context retrieval."""
    context = retrieve_relevant_context(user_query, model, documents)
    
    # User-friendly prompt
    prompt = f"""
    You are a helpful AI assistant. Answer the following question based on the provided information.
    
    📌 **Relevant Context**:
    {context}

    ❓ **User's Question**: {user_query}

    💡 **Answer**:
    """

    gemini_model = genai.GenerativeModel("gemini-1.5-pro")  
    response = gemini_model.generate_content(prompt)

    if response and hasattr(response, "text"):
        return response.text.strip()
    else:
        return "Sorry, I couldn't generate a response. Try rephrasing your question."

# Streamlit UI
st.title("📚 RAG-Based Chatbot with Gemini & Word2Vec")

uploaded_file = st.file_uploader("📂 Upload a document (TXT, PDF)", type=["txt", "pdf"])

documents = []
if uploaded_file:
    file_text = extract_text_from_file(uploaded_file)
    documents = process_text(file_text)
    
    if documents:
        model = train_word2vec(documents)
        st.success(f"✅ Document '{uploaded_file.name}' uploaded and processed successfully!")
    else:
        st.error("❌ Failed to process the document.")
        model = None
else:
    model = None

input_text = st.text_input("💬 Ask a question based on the document:")

if input_text and model:
    response_text = generate_response(input_text, model, documents)
    st.markdown(f"### 🤖 AI Response:\n{response_text}")
elif input_text:
    st.warning("⚠️ Please upload a document first.")
