import openai
from config import get_settings
from models.benefit_category import BenefitCategory

settings = get_settings()
benefit_category_values = [category.value for category in BenefitCategory]

def parse_with_gpt(email_subject: str, email_body: str, ocr_text: str):
    client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

    system_prompt = get_system_prompt(benefit_category_values)
    user_prompt = get_user_prompt(email_subject, email_body, ocr_text)

    response = client.chat.completions.create(
        model=settings.OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        response_format={"type": "json_object"}
    )
    return response.choices[0].message.content


def get_system_prompt(categories: list[str]):
    category_list = "\n  - " + "\n  - ".join(categories)  # Properly format list
    return f"""
        You are an AI document parser specialized in extracting structured data from benefit letters.

        ### Task:
        You will receive three types of text input:
        1. **Email Body** (text content of the email)
        2. **Email Subject** (header/title of the email)
        3. **Parsed Document Text** (OCR-extracted content from attachments like PDFs or images)

        ### Instructions:
        - Determine the **category** of the benefit letter from a predefined list:
        {category_list}

        - Extract structured fields based on the detected category for each document.
        - From one document you must extract only 1 unique field. If you find more - save this to additional_info field
        **Always return JSON output** in the format:
        
        ```json
        [
            {{
                "file_name": "File Name",
                "category": "Category Name",
                "username": "Extracted Name",
                "document_number": "Extracted Document Number",
                "document_date": "Extracted Document Date",
                "address": "Extracted Address (if available)",
                "document_sum": "Extracted document sum",
                "document_currency": "Extracted document currency",
                "account_number": "Extracted account number",
                "additional_info": "Short description of the benefit claim"
            }},
            {{
                "file_name": "File Name",
                "category": "Category Name",
                "username": "Extracted Name",
                "document_number": "Extracted Document Number",
                "document_date": "Extracted Document Date",
                "address": "Extracted Address (if available)",
                "document_sum": "Extracted document sum",
                "document_currency": "Extracted document currency",
                "account_number": "",
                "additional_info": "Short description of the benefit claim"
            }}
        ]
        ```

        - **If any field is missing in the document, return `null` for that field**.
        - Always respond in **valid JSON format**.
    """

def get_user_prompt(email_subject: str, email_body: str, ocr_text: str):
    return f"""
        ### Email Subject:
        {email_subject}

        ### Email Body:
        {email_body}

        ### OCR Extracted Text:
        {ocr_text}

        ### Instructions:
        - Identify the category of this benefit letter.
        - Extract relevant fields (username, amount, date, transaction_id, etc.).
        - Return a structured JSON response.
        """
