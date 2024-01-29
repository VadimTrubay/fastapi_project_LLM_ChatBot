import os
import pandas as pd
import textract
import ipywidgets as widgets
from IPython.display import display
import langchain
import matplotlib.pyplot as plt
from dotenv import load_dotenv
from transformers import GPT2TokenizerFast
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain.llms import OpenAI
from langchain.chains import ConversationalRetrievalChain



# from dotenv import load_dotenv
#
# from src.config.config import settings

# os.environ["TOKENIZERS_PARALLELISM"] = "false"
load_dotenv()

# OPENAI_API_KEY = settings.openai_api_key
# print(OPENAI_API_KEY)
# OPENAI_API_KEY = "!!!!!!!!!!"
#
# os.environ[OPENAI_API_KEY] = "!!!!!!!!!!!"
# load_dotenv()
#
# OPENAI_API_KEY = settings.openai_api_key

""" Convert PDF to Text"""
file_path = "./Andrew Osypenko CV Sep 2023.pdf"
doc = textract.process(filename=file_path)
txt_file_path = f"{file_path.rstrip('.pdf')}.txt"
""" Save to txt and reopen """
with open(txt_file_path, "w", encoding="utf-8") as f:
    f.write(doc.decode("utf-8"))

with open(txt_file_path, "r", encoding="utf-8") as f:
    text = f.read()

print(len(text))

""" Create function to count tokens """
tokenizer = GPT2TokenizerFast.from_pretrained("gpt2")


def count_tokens(text: str) -> int:
    return len(tokenizer.encode(text))


""" Split text in to chunks """
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=512,
    chunk_overlap=24,
    length_function=count_tokens
)

chunks = text_splitter.create_documents([text])
print(type(chunks), len(chunks))
# print(langchain.schema.document)

""" Embedding text and store it embedings """

embeddings = OpenAIEmbeddings()

""" Create vector DB """
vector_db = FAISS.from_documents(chunks, embeddings)

""" Setup retrieval function"""
query = "What is the last name of ANDREW?"
docs = vector_db.similarity_search(query)
print(len(docs))

chain = load_qa_chain(OpenAI(temperature=0), chain_type="stuff")
query = "Who is andrew?"
docs = vector_db.similarity_search(query)

print(chain.run(input_documents=docs, question=query))

""" Create conversational chain that use vector db for retrival
    Also allow chain history
"""
qa = ConversationalRetrievalChain.from_llm(OpenAI(temperature=0), vector_db.as_retriever())
chat_history = []


def print_chat_history():
    for user_query, bot_response in chat_history:
        print(f'User: {user_query}')
        print(f'Bot: {bot_response}')
        print('-' * 20)


print("Welcome to my BOT! Type 'exit' to stop")

while True:
    user_input = input("You: ")

    if user_input.lower() == 'exit':
        print("Thank you for using the chatbot. Goodbye!")
        break

    # Process user input
    result = qa({"question": user_input, "chat_history": chat_history})
    bot_response = result["answer"]

    # Update chat history
    chat_history.append((user_input, bot_response))

    # Print the chat history
    print_chat_history()
