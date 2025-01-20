#!/usr/bin/env python3

import fitz
import os
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate

def extract_text_from_pdf(pdf_path) -> str:
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text
    except Exception as e:
        return f"Error extracting text from {pdf_path}: {e}"
    finally:
        doc.close()

def main():
    model_name = "gpt-3.5-turbo"
    temperature = 0.5

    if "OPENAI_API_KEY" not in os.environ:
        print("Error: OPENAI_API_KEY environment variable not set.")
        return

    try: 
            pdf_path = input("Enter the path to the PDF file or `quit` to exit the program: ")
            if pdf_path.lower() == "quit":
                print("Exiting program...")
                return

            prompt = extract_text_from_pdf(pdf_path).strip()
            assistant_template = prompt + """
            You are an experienced hotel manager and provide assistance regarding general information about the hotel. Please do not provide any information outside of the context of the hotel.
            Question: {question}
            Answer:
            """

            assistant_prompt_template = PromptTemplate(
                input_variables=["question"],
                template=assistant_template
            )
            
            llm = OpenAI(model = model_name, temperature = temperature)
            llm_chain = assistant_prompt_template | llm

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()