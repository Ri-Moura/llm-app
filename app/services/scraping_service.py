import requests
import pdfplumber
from bs4 import BeautifulSoup

def scrape_website(url: str) -> str:
    """
    Scrape text content from a website.

    Args:
        url (str): The URL of the website to scrape.

    Returns:
        str: The scraped text content.
    """
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.get_text(separator='\n')
    return text

def extract_text_from_pdf(url: str) -> str:
    """
    Extract text content from a PDF file at the given URL.

    Args:
        url (str): The URL of the PDF file.

    Returns:
        str: The extracted text content.
    """
    response = requests.get(url)
    response.raise_for_status()
    with open('temp.pdf', 'wb') as f:
        f.write(response.content)
    text = []
    with pdfplumber.open('temp.pdf') as pdf:
        for page in pdf.pages:
            text.append(page.extract_text())
    return ' '.join(filter(None, text))
