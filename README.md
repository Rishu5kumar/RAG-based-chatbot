# RAG-based-chatbot

This project is a RAG-based-chatbot that answers questions based on a text file the user uploads. It works by:

1. **Reading and breaking the document into smaller pieces** so we can efficiently search for relevant information.
2. **Training a Word2Vec model** to understand the meaning and relationships of words in the document.
3. **Retrieving relevant information** when a user asks a question by comparing the words in the question to the words in the document.
4. **Using Google Gemini AI** to generate an answer using the retrieved information.
5. **Displaying everything on a simple website** using Streamlit.

---

## Step-by-Step Explanation
### Setting Up the Required Tools
Before starting, we need to import libraries that help us perform different tasks. Here’s what each library does:

- Streamlit → Helps us build a simple web interface where users can upload files and ask questions.
- Google Generative AI (Gemini) → Used to generate answers based on relevant information from the document.
- dotenv → Used to securely store and load the API key for Gemini AI.
- NLTK (Natural Language Toolkit) → Helps in processing text, breaking sentences into words, and removing unnecessary words.
- Gensim (Word2Vec model) → Learns the relationships between words, helping to find similar words in the text.
- NumPy → Used for performing mathematical operations like calculating word similarity.
- LangChain → Splits long documents into smaller, more manageable parts for easy searching.

### Fixing Missing Downloads (NLTK Tokenizer)
- Why is this needed?
When working with text, we need a way to break sentences into words (called "tokenization"). NLTK provides a tool for this, but it may not be installed by default. So, we download it manually to make sure everything works smoothly.

### Loading API Key for Gemini AI

- Google Gemini AI is a cloud-based service, meaning it doesn’t run directly on our computer. Instead, we send a request to Google’s servers, and they return a response.
- To use Gemini AI, we need an API key (like a password) that allows us to communicate with it.
- We store the API key securely in a .env file instead of writing it directly in our code. This prevents others from misusing it.

### Splitting the Document into Smaller Parts

- If a document is very large, searching for relevant information becomes slow and inefficient.
- Instead of working with the whole document at once, we break it into smaller pieces (called "chunks").
- Each chunk is about 500 characters long, with a 50-character overlap between chunks.
- The overlap helps ensure that important sentences that span two chunks are not lost.

📌 Example:
Let’s say we have this text:
"AI is the future of technology. Machine learning is a key part of AI."
After splitting, the first chunk might be:
"AI is the future of technology."
And the second chunk might be:
"technology. Machine learning is a key part of AI."
This way, "technology" is in both chunks, ensuring smooth transitions.

### Training the Word2Vec Model

- Word2Vec is a machine learning model that helps computers understand relationships between words.
- Instead of treating words as just letters, it converts them into mathematical vectors (lists of numbers) so they can be compared.
- Words that appear in similar contexts will have similar vector representations.

📌 Example:

- If a document contains the sentence: "AI is smart", Word2Vec learns that "AI" and "smart" are related.
- If another sentence says, "AI is intelligent", Word2Vec understands that "intelligent" is similar to "smart".
- If a user asks, "Is AI intelligent?", Word2Vec recognizes that "intelligent" is similar to "smart" and finds relevant text.

#### How does training work?

- The document is broken into sentences.
- Each sentence is split into words.
- Word2Vec learns patterns and relationships between words by looking at how often they appear together.

### Retrieving Relevant Context (Finding the Best Answer Source)

- When a user asks a question, we don’t want to search the whole document.
- Instead, we find the most relevant chunks of text and use them to answer the question.

📌 How does it work?

- The question is broken into words.
- We compare each word to the words in every text chunk.
- Using Word2Vec, we check which chunk has the most similar words.
- The top 2 most relevant chunks are selected and passed to Gemini AI.
📌 Example:

User asks: "What is AI?"
The document has chunks like:
Chunk 1: "AI is the future of technology."
Chunk 2: "Machine learning is a part of AI."
The chatbot selects Chunk 1 and Chunk 2 because they contain the most relevant words.

### Generating the Final Answer with Google Gemini AI
Why do we use Gemini AI?

- Even though Word2Vec helps us find relevant text, it cannot generate human-like answers.
- Instead, we send the relevant text to Gemini AI, which reads it and creates a well-structured response.
📌 How does it work?

We combine the retrieved text chunks into a single prompt.
We send this prompt to Google Gemini AI.
Gemini analyzes the text and generates a natural answer.
📌 Example:

If the user asks: "What is AI?", and the document says "AI is the future of technology.", Gemini might generate:
"AI stands for Artificial Intelligence, which is a field of technology focused on building smart systems."
### Streamlit Web App (Making Everything User-Friendly)
What is Streamlit?

Streamlit is a Python library that helps us create a simple web app without needing advanced web development skills.
Instead of running the chatbot in a terminal, we create a graphical user interface (GUI) where users can:
Upload a document
Type a question
See the AI-generated answer
📌 How does the app work?

A user uploads a text file.
The file is processed and stored.
The Word2Vec model is trained on the document.
The user asks a question in a text box.
The chatbot retrieves relevant text and uses Gemini AI to generate a response.
The answer is displayed on the webpage.
📌 Example:

User uploads a file about AI.
They type "What is deep learning?"
The chatbot searches for relevant information.
Gemini AI generates: "Deep learning is a subset of machine learning that uses neural networks to process data."
The answer appears on the screen.
🚀 Final Summary
User uploads a document 📂
The document is split into smaller chunks 📝
A Word2Vec model is trained on the text 🧠
The user asks a question 💬
The chatbot finds relevant text 🔍
Gemini AI generates an answer 🤖
The answer is displayed on a simple web app 🖥️
This project combines document processing, AI, and a web interface to create an intelligent chatbot that can answer questions based on uploaded files.
---
📌 Sample Example
We will go through each step, assuming we have a text document uploaded.

1️⃣ User Uploads a Document
Let's assume the user uploads a text file with the following content:

vbnet
Copy
Edit
Artificial Intelligence (AI) is a branch of computer science that focuses on creating smart systems.
Machine Learning (ML) is a subset of AI that enables machines to learn from data.
Deep Learning, a part of ML, uses neural networks to make decisions.
AI is widely used in healthcare, finance, and autonomous vehicles.
2️⃣ Document is Split into Chunks
Since the document is short, it might be split into two chunks like this:

Chunk 1:
"Artificial Intelligence (AI) is a branch of computer science that focuses on creating smart systems. Machine Learning (ML) is a subset of AI that enables machines to learn from data."

Chunk 2:
"Deep Learning, a part of ML, uses neural networks to make decisions. AI is widely used in healthcare, finance, and autonomous vehicles."

3️⃣ Word2Vec Model is Trained
The Word2Vec model reads the document and learns word relationships.
It now understands that "AI" is related to "Machine Learning", and "Deep Learning" is related to "Neural Networks".
4️⃣ User Asks a Question
The user enters:
💬 "What is deep learning?"

5️⃣ Finding Relevant Text
The chatbot tokenizes the question → ["What", "is", "deep", "learning", "?"]
It compares these words to words in each chunk using Word2Vec.
Chunk 2 is most relevant because it contains "Deep Learning" and "Neural Networks".
✅ Retrieved Context:
"Deep Learning, a part of ML, uses neural networks to make decisions."

6️⃣ Generating Answer Using Gemini AI
The chatbot sends this retrieved context to Google Gemini AI with the following prompt:
📌 Prompt Sent to Gemini AI:
"You are a helpful AI assistant. Answer the following question based on the provided information.
Relevant Context: Deep Learning, a part of ML, uses neural networks to make decisions.
User's Question: What is deep learning?
Answer:"

🤖 Gemini AI generates this response:
"Deep learning is a specialized subset of machine learning that uses artificial neural networks to process complex data patterns and make intelligent decisions."

7️⃣ Answer is Displayed
The chatbot shows:

💬 🤖 AI Response:
"Deep learning is a specialized subset of machine learning that uses artificial neural networks to process complex data patterns and make intelligent decisions."

✅ Final Result
User uploaded a document 📂
The document was split into smaller chunks 📝
A Word2Vec model was trained to learn word relationships 🧠
The user asked a question 💬
The chatbot found the most relevant text 🔍
Gemini AI generated a clear answer 🤖
The answer was displayed on the Streamlit web app 🖥️
🎯 Summary
This project understands the user’s question, finds the best answer from the document, and uses AI to provide a clear response. 🚀

Would you like to test this with a custom document? 😃
