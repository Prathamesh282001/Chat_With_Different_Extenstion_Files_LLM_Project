## ProtonDatalabs AI developer Assignment

### Assignment Description
Build a chatbot application which takes a file (.txt, .pdf, .docx) as an input and answers user's query.

### Assignment Goal
Accurately provide answers based on the uploaded file's text data.

### Approach
We are using OpenAI large language model to answer users query based on uploaded file because of its ability to answer accurately and it is fast. For chatbot's user interface we are using python's chainlit library because of its multiple in-built features, which gives a user experience like chatgpt. 
We are using prompt template to tailor the model's behavior to specific domains or tasks. In this task we are prompting llm to generate an answer to a user's query based on the given context (text present in uploaded file). At the start of the chatbot model, it asks users to upload files. We are suing Chainlit's AskFileMessage feature to take files from users. We are storing this file in a user session because storing it locally or in a database causes performance hindrances of chatbot. 
After taking an uploaded file, we extract the text present in the file. This text is then sent to the text splitter instance, which is creating data chunks. These data chunks are then embedded (mathematical representation of words in higher dimensions which can be understood by llm or computer) using HuggingFaceEmbedding model because this model can handle large amount of tokens, and it is a bit fast compared to other free models. The generated embeddings are then stored in ChromaDb vector database (offers simplicity and it is open-source) to do similarity search and retrive answer relevant to user's query. 
When a user asks a question, the model  generates an answer and sends it back to the user.
The model is deployed on Microsoft Azure cloud service. First we have created created image (containerization) of our app using docker. This image is stored in azure container registry. And hosted the chatbot using azure web app service.


### Tools & Libraries used
All Libraries mentioned in requirements.txt
LLM - OpenAI()
Frontend & Backend - Python & Chainlit
IDE - Visual Studio Code
Containerization - Docker
Cloud service - Microsoft Azure