#!/usr/bin/env python3

import fitz
import os
from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate

def extract_text_from_pdf(pdf_path) -> str:
    try:
        with fitz.open(pdf_path) as doc:
            text = ""
            for page in doc:
                text += page.get_text()
            return text
    except Exception as e:
        return f"Error extracting text from {pdf_path}: {e}"

def main():
    model_name = "gpt-4"
    temperature = 0.5

    if "OPENAI_API_KEY" not in os.environ:
        print("Error: OPENAI_API_KEY environment variable not set.")
        return

    try: 
            pdf_path = input("Enter the path to the PDF file or `quit` to exit the program: ")
            if pdf_path.lower() == "quit":
                print("Exiting program...")
                return

            extracted_text = extract_text_from_pdf(pdf_path).strip()
            assistant_template = f"""
            {extracted_text}
            You are an experienced hotel manager and provide assistance regarding general information about the hotel. Please do not provide any information outside of the context of the hotel.

            Question: {{question}}
            Answer:
            """

            assistant_prompt_template = PromptTemplate(
                input_variables=["question"],
                template=assistant_template
            )
            
            llm = OpenAI(model = model_name, temperature = temperature)
            llm_chain = assistant_prompt_template | llm

            while True:
                question = input("Ask a question about the hotel or `quit` to exit the program: ")
                if question.lower() == "quit":
                    print("Exiting program...")
                    break
                response = llm_chain.invoke({"question": question})
                if response:
                    print(f"Answer: {response}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()