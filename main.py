#!/usr/bin/env python3

import fitz

def extract_text_from_pdf(pdf_path) -> str:
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text

    except Exception as e:
        return f"Error extracting text from {pdf_path}: {e}"

def main():
    try: 
            pdf_path = input("Enter the path to the PDF file or `quit` to exit the program: ")
            if pdf_path.lower() == "quit":
                print("Exiting program...")
                return

            text = extract_text_from_pdf(pdf_path)
            with open("output.txt", "w", encoding="utf-8") as fh:
                fh.write(text)
            
    except Exception as e:
        print(f"Error extracting text from PDF document: {e}")
            

if __name__ == "__main__":
    main()