# ProtonDatalabs AI Developer Assignment Documentation

## Project Overview

The ProtonDatalabs AI Developer Assignment involves building a chatbot application capable of answering user queries based on uploaded files in formats such as .txt, .pdf, and .docx. The primary objective is to provide accurate answers derived from the textual data within the uploaded files.

## Project Goal

The goal is to develop a chatbot application that can effectively respond to user queries by leveraging an OpenAI large language model. This model's capability to deliver accurate and rapid responses makes it an ideal choice for the task. The user interface of the chatbot application is designed to mimic a conversation, offering a seamless and intuitive experience for users.

## Approach

### Model Selection:
The chosen approach involves utilizing the OpenAI large language model (LLM) for generating responses based on the context provided by the uploaded file. This model offers exceptional accuracy and efficiency in processing natural language queries.

### Implementation Framework:
To create the chatbot interface, the project utilizes the Chainlit library in Python. Chainlit offers a range of built-in features that facilitate the development of conversational interfaces. 

### Prompt Template:
A prompt template is employed to customize the behavior of the LLM specifically for the task at hand. By tailoring the prompts, the model can effectively generate responses relevant to the content extracted from the uploaded files.

### File Upload and Session Management:
At the beginning of the chatbot interaction, users are prompted to upload files. The Chainlit library's AskFileMessage feature is utilized to seamlessly collect files from users. These files are stored within the user session to optimize performance and streamline data handling.

### Text Processing and Embedding:
Upon receiving the uploaded file, the text content is extracted and processed. A text splitter instance partitions the text into manageable chunks. These chunks are then embedded using the HuggingFaceEmbedding model, chosen for its capability to handle large volumes of tokens efficiently.

### Vector Database:
The embedded data chunks are stored in the ChromaDb vector database. This database facilitates similarity search operations, enabling the retrieval of relevant answers based on user queries.

### Answer Generation:
When users pose questions to the chatbot, the model generates responses based on the contextual information derived from the uploaded files. The generated answers are promptly delivered to the users.

### Deployment:
The completed chatbot application is deployed on the Microsoft Azure cloud service. Docker is used for containerization, allowing for easy deployment and scalability. The application image is stored in the Azure Container Registry, and the chatbot is hosted using the Azure Web App service.

## Tools & Libraries Used

- Python: Programming language for backend development.
- Chainlit: Library utilized for building the chatbot interface.
- OpenAI LLM: Large language model employed for generating responses.
- Docker: Containerization tool used for creating application images.
- Microsoft Azure: Cloud service provider utilized for deployment.
- Visual Studio Code: Integrated Development Environment (IDE) for code development.
- Other libraries specified in the requirements.txt file.
#### Google drive link for demo video
https://drive.google.com/file/d/1XsrTr9qvdGDJ5t01I0dxEsOAH0vk0adx/view?usp=share_link
