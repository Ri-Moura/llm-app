# Multimodal RAG Implementation

## Overview
LLM-App is designed to ensure content generation aligns with a brand's voice and style. Users can input text, provide a URL, or upload a file containing brand guidelines and sample content. The application extracts and utilizes the brand voice from these inputs to guide content generation.

## Features
- **Natural Language Processing**: Utilizes advanced language models to extract brand voice from provided inputs.
- **PDF and HTML Support**: Handles URLs and PDF files, extracting text for processing.
- **Scalable Deployment**: Dockerized for easy and consistent deployment.

## Task
Develop a RAG-LLM based system to:
- Accept a URL for a PDF file.
- Extract and return the brand voice captured in the PDF text.

## Technology Stack
- **LLM Stack**: OpenAI API.
- **RAG**: Pinecone API.
- **API**: FastAPI.

## Installation
1. Clone the repository:
    ```bash
    git clone https://github.com/Ri-Moura/llm-app.git
    cd llm-app
    ```
2. Build the Docker image:
    ```bash
    docker build -t llm-app .
    ```
3. Run the Docker container:
    ```bash
    docker run -d -p 8000:8000 llm-app
    ```

## Usage
1. Access the application:
    Open a web browser and navigate to `http://localhost:8000`.
2. Endpoints:
    - **/generate-content/**: Extracts brand voice from a PDF URL or file.
    - **/handle-query/**: Handles user queries related to the brand voice.
    - **/embed-and-store/**: Embeds and stores text chunks from a URL.
    - **/delete-index/**: Deletes a specified index from Pinecone.

## API Routes
- **POST /generate-content/**: Accepts a URL or file and extracts brand voice.
- **POST /handle-query/**: Accepts a query and returns the relevant brand voice information.
- **POST /embed-and-store/**: Embeds text from a URL and stores it in Pinecone.
- **POST /delete-index/**: Deletes an index from Pinecone.

## Requirements
- Docker
- Python 3.x
- OpenAI API Key
- Pinecone API Key

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m 'Add your feature'`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact
For questions or support, please open an issue in this repository.
