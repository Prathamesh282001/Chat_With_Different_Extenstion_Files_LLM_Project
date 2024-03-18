# Importing all necessary libraries
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQAWithSourcesChain
from langchain_community.chat_models import ChatOpenAI
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
import os
import chainlit as cl
import PyPDF2
from docx import Document
from dotenv import load_dotenv
load_dotenv()

# Fetching environment variable where i have stored OpenAI api key
#api_key = os.environ.get("OPEN_API_KEY")
api_key = "your api key"

# providing prompt for LLM
system_template = """Use the following pieces of context to answer the users question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.
ALWAYS return a "SOURCES" part in your answer.
The "SOURCES" part should be a reference to the source of the document from which you got your answer.

Begin!
----------------
{summaries}"""

system_template1 = """Given the following context, generate an answer of user's question based on the context.
In the answer try to provide as much text as possible from context.
Generate accurate answer. If you don't know the answer just say "Sorry!,I don't know". Don't try to make up an answer.

Begin!
----------------
{summaries}"""


messages = [
    SystemMessagePromptTemplate.from_template(system_template),
    HumanMessagePromptTemplate.from_template("{question}"),
]
prompt = ChatPromptTemplate.from_messages(messages)
chain_type_kwargs = {"prompt": prompt}

# creating text splitter instace using which data chunks are created to store in vector database.
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)


# this is processing part which happens when we open chatbot interface to start chat with model.
@cl.on_chat_start
async def on_chat_start():

    elements = [
    cl.Image(name="image1", size="small",display="inline", path="public/logo.png")
    ]
    await cl.Message(content="Hello there, I am here to assist you!", elements=elements).send()
    files = None

    # Asking user to upload a file. Wait for the user to upload a file
    while files is None:
        files = await cl.AskFileMessage(
            content="Please upload a file to begin!",
            accept=["application/pdf","text/plain","application/vnd.openxmlformats-officedocument.wordprocessingml.document"], # allowed extensions
            max_size_mb=40, # maximum file size allowed
            timeout=180,
        ).send()

    file = files[0]

    # processing of uploaded file
    msg = cl.Message(content=f"Processing `{file.name}`...")
    await msg.send()

    # .txt file
    if file.type == "text/plain":
        # trying different encoding styles to avoid error
        encodings_to_try = ['utf-8', 'latin-1', 'utf-16']

        for encoding in encodings_to_try:
            try:
                with open(file.path, 'r', encoding=encoding) as file:
                    txt_text = file.read()
                    texts = text_splitter.split_text(txt_text)
                break
            except UnicodeDecodeError:
                continue
        else:
            print("Unable to decode the file using any of the specified encodings.")

    # .pdf file
    elif file.type == "application/pdf":
        pdf = PyPDF2.PdfReader(file.path)
        pdf_text = ""
        for page in pdf.pages:
            pdf_text += page.extract_text()
    
        texts = text_splitter.split_text(pdf_text)

    # .docx file
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        doc = Document(file.path)
        text = []
        for paragraph in doc.paragraphs:
            text.append(paragraph.text)
        doc_text = '\n'.join(text)
        texts = text_splitter.split_text(doc_text)


    # Create metadata for each chunk
    metadatas = [{"source": f"{i}-pl"} for i in range(len(texts))]

    # embedding data chunks using HuggingFaceEmbeddings
    embeddings =  HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2',
                                       model_kwargs={'device': 'cpu'})
    
    # storing embedded documents in chromadb vector store
    docsearch = await cl.make_async(Chroma.from_texts)(
        texts, embeddings, metadatas=metadatas
    )

    # creating a chain that uses the chroma vector store
    chain = RetrievalQAWithSourcesChain.from_chain_type(
        ChatOpenAI(temperature=0.7,openai_api_key=api_key),
        chain_type="stuff",
        retriever=docsearch.as_retriever(),
    )
    

    # Save the metadata and texts in the user session
    cl.user_session.set("metadatas", metadatas)
    cl.user_session.set("texts", texts)

    # Let the user know that the system is ready to proceed
    msg.content = f"Processing `{file.name}` done. You can now ask questions!"
    await msg.update()
    
    # saving the above created chain in user session for further use
    cl.user_session.set("chain", chain) 


# this is a processing part which happens when user ask questions to model
@cl.on_message
async def main(message:str):

    chain = cl.user_session.get("chain")  # type: RetrievalQAWithSourcesChain
    cb = cl.AsyncLangchainCallbackHandler(
        stream_final_answer=True, answer_prefix_tokens=["FINAL", "ANSWER"]
    )
    cb.answer_reached = True

    # getting response from chain
    res = await chain.acall(message.content, callbacks=[cb])

    answer = res["answer"]
    sources = res["sources"].strip()
    source_elements = []
    
    # Get the metadata and texts from the user session
    metadatas = cl.user_session.get("metadatas")
    all_sources = [m["source"] for m in metadatas]
    texts = cl.user_session.get("texts")

    if sources:
        found_sources = []

        # Add the sources to the message
        for source in sources.split(","):
            source_name = source.strip().replace(".", "")
            # Get the index of the source
            try:
                index = all_sources.index(source_name)
            except ValueError:
                continue
            text = texts[index]
            found_sources.append(source_name)

            source_elements.append(cl.Text(content=text, name=source_name))

        if found_sources:
            answer += f"\nSources: {', '.join(found_sources)}"
        else:
            answer += "\nNo sources found"

    if cb.has_streamed_final_answer:
        cb.final_stream.elements = source_elements
        await cb.final_stream.update()
    else:
        await cl.Message(content=answer, elements=source_elements).send() # sending response back to the user with source chunks

@cl.on_chat_end
def on_chat_end():
    cl.user_session.set("metadatas", None)
    cl.user_session.set("texts", None)
    cl.user_session.set("chain",None)