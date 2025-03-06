import openai
from config import get_settings

settings = get_settings()

def parse_with_gpt(text):
    client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

    system_prompt = get_system_prompt()
    user_prompt = get_user_prompt()

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
    return f"""
        You are an AI document parser specialized in extracting structured data from benefit letters.

        ### Task:
        You will receive three types of text input:
        1. **Email Body** (text content of the email)
        2. **Email Subject** (header/title of the email)
        3. **Parsed Document Text** (OCR-extracted content from attachments like PDFs or images)

        ### Instructions:
        - Determine the **category** of the benefit letter from a predefined list:
        {categories}

        - Extract structured fields based on the detected category.
        **Always return JSON output** in the format:
        
        ```json
        {
            "category": "Category Name",
            "fields": {
            "username": "Extracted Name",
            "email": "Extracted Email (if available)",
            "amount": "Extracted Amount (if available)",
            "date": "Date of the transaction",
            "transaction_id": "Extracted Transaction ID (if available)",
            "description": "Short description of the benefit claim"
            }
        }
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
