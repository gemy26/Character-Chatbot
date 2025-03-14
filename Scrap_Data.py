import os
import fitz
from pypdf import PdfReader
import requests
from bs4 import BeautifulSoup

files = []

def download_pdf(link, name):
    try:
        response = requests.get(link)
        if response.status_code == 200:
            if link.endswith('.pdf') or 'application/pdf' in response.headers.get('Content-Type', ''):
                filename = f"{name}.pdf"
                files.append(filename)
                with open(filename, "wb") as pdf_file:
                    pdf_file.write(response.content)
                print(f"PDF downloaded successfully: {filename}")
            else:
                print(f"Skipping non-PDF link: {link}")
        else:
            print(f"Failed to download PDF from {link}. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred while downloading {link}: {e}")


# convert_to_txt(name + ".pdf")
def convert_to_txt():
    for pdf_path in files:
        doc = fitz.open(pdf_path)
        output_txt_path = f"{pdf_path[:-4]}.txt"
        with open(output_txt_path, "w", encoding="utf-8") as file:
            for page in doc:
                file.write(page.get_text("text") + "\n\n")


def seed_data():
    site = requests.get("https://www.bbc.co.uk/writers/scripts/tv-drama/sherlock")
    soup = BeautifulSoup(site.content, 'lxml')
    for li in soup.find_all('li', class_="component-links-item"):
        link = li.a.get("href")
        if link:
            name = li.a.get_text()[:19]
            download_pdf(link, name)
            
            


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text from a single PDF file.
    """
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text


def merge_pdfs_to_txt(pdf_folder: str, output_txt: str) -> None:
    """
    Merge all PDFs in a folder into a single text file.
    """
    # Get a list of all PDF files in the folder
    pdf_files = [f for f in os.listdir(pdf_folder) if f.endswith(".pdf")]
    pdf_files.sort()  # Sort files alphabetically (optional)

    # Extract text from each PDF and merge into one
    merged_text = ""
    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdf_folder, pdf_file)
        print(f"Extracting text from: {pdf_file}")
        text = extract_text_from_pdf(pdf_path)
        merged_text += f"\n\n=== {pdf_file} ===\n\n{text}"

    # Save the merged text to a .txt file
    with open(output_txt, "w", encoding="utf-8") as file:
        file.write(merged_text)
    print(f"All PDFs merged into: {output_txt}")     