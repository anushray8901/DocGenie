import openai
import os
import PyPDF2
import pandas as pd
import docx

# Set OpenAI API Key
OPENAI_API_KEY = ""  # Replace with actual API key

def read_documents_from_folder(folder_path):
    """Reads all PDFs, Excel, CSV, and Word files from a folder and extracts their combined text."""
    if not os.path.exists(folder_path):
        print(f"❌ Folder not found: {folder_path}")
        return None

    files = [os.path.join(folder_path, file) for file in os.listdir(folder_path)
             if file.endswith((".pdf", ".csv", ".xlsx", ".xls", ".docx"))]

    if not files:
        print("⚠️ No supported files found in the folder.")
        return None

    combined_text = ""

    for file_path in files:
        try:
            ext = os.path.splitext(file_path)[1].lower()

            if ext == ".pdf":
                text = extract_text_from_pdf(file_path)
            elif ext == ".csv":
                text = extract_text_from_csv(file_path)
            elif ext in [".xlsx", ".xls"]:
                text = extract_text_from_excel(file_path)
            elif ext == ".docx":
                text = extract_text_from_word(file_path)
            else:
                text = None

            if text:
                combined_text += f"\n\n--- Extracted from {os.path.basename(file_path)} ---\n{text}"
            else:
                print(f"⚠️ No readable text in {os.path.basename(file_path)}")

        except Exception as e:
            print(f"⚠️ Error reading {os.path.basename(file_path)}: {e}")

    return combined_text if combined_text else "⚠️ No readable text in provided documents."

def extract_text_from_pdf(file_path):
    """Extracts text from a PDF file."""
    try:
        with open(file_path, "rb") as file:
            reader = PyPDF2.PdfReader(file)
            return "\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
    except Exception as e:
        print(f"Error reading PDF {file_path}: {e}")
        return None

def extract_text_from_csv(file_path):
    """Extracts text from a CSV file."""
    try:
        df = pd.read_csv(file_path)
        return df.to_string()
    except Exception as e:
        print(f"Error reading CSV {file_path}: {e}")
        return None

def extract_text_from_excel(file_path):
    """Extracts text from an Excel file."""
    try:
        df = pd.read_excel(file_path)
        return df.to_string()
    except Exception as e:
        print(f"Error reading Excel {file_path}: {e}")
        return None

def extract_text_from_word(file_path):
    """Extracts text from a Word (.docx) file."""
    try:
        doc = docx.Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])
    except Exception as e:
        print(f"Error reading Word document {file_path}: {e}")
        return None

def chat_with_llm(user_query, file_contents):
    """Sends a query to OpenAI's GPT model and retrieves a response."""
    if not OPENAI_API_KEY:
        print("❌ No OpenAI API key available, cannot proceed with LLM call.")
        return "❌ Authentication Error"

    try:
        openai.api_key = OPENAI_API_KEY

        # Define the conversation
        messages = [
            {"role": "system", "content": "You are an AI assistant that answers queries based on the provided document data."},
            {"role": "system", "content": f"Here is the extracted text from the documents: {file_contents}"},
            {"role": "user", "content": user_query}
        ]

        # Call the OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        formatted_response = response['choices'][0]['message']['content'].strip()

        print("\n🤖 AI Response:", formatted_response)  # Debugging
        return formatted_response

    except Exception as e:
        print(f"⚠️ Error calling OpenAI model: {e}")
        return "⚠️ AI service is unavailable."
