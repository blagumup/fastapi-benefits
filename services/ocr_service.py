import base64
from google.api_core.client_options import ClientOptions
from google.cloud import documentai
from config import get_settings

from models.ocr_processors import OCRProcessors

SETTINGS = get_settings()

class UnsupportedFileTypeError(Exception):
    """Custom exception for unsupported file types."""
    pass


def process_files(email_data):
    """Processes email attachments using OCR and returns extracted data."""
    extracted_data = []

    for attachment in email_data["attachments"]:
        attachment_content = base64.b64decode(attachment["content"])
        mime_type = attachment["mime_type"]
        file_name = attachment["filename"]
        # Using Custom Processor for OCR
        attachment_text, attachment_entities = process_document_ocr(processor_id=OCRProcessors.CUSTOM_PARSER.value, file=attachment_content, mime_type=mime_type)

        print(f"Processed: {file_name}")
        print(f"Extracted Text: {attachment_text}")
        print(f"Extracted Entities: {attachment_entities}")

        # Append extracted info as a tuple
        extracted_data.append((file_name, attachment_text, attachment_entities))

    return extracted_data

def process_document_ocr(processor_id: str, file: str, mime_type: str) -> None:
    """
    Process a document using Document AI OCR and extract text and entities.

    Args:
        processor_id: The ID of the Document AI processor.
        file: The file to process.

    Returns:
        A tuple containing the extracted text and a list of entities.

    Raises:
        UnsupportedFileTypeError: If the file type is not supported.
    """

    # Online processing request to Document AI
    document = _process_document(
        project_id=SETTINGS.OCR_PROJECT_ID,
        location=SETTINGS.OCR_LOCATION,
        processor_id=processor_id,
        processor_version=SETTINGS.OCR_PROCESSOR_VERSION,
        file=file,
        mime_type=mime_type,
    )
    
    text = document.text
    # Extract entities from the document (available only for non-default processors)
    entities = _extract_entities(document)
            
    return text, entities

def _process_document(
    project_id: str,
    location: str,
    processor_id: str,
    processor_version: str,
    file: str,
    mime_type: str,
) -> documentai.Document:
    """
    Process a document using Google Cloud Document AI.

    Args:
        project_id: The Google Cloud project ID.
        location: The Document AI location ('eu' or 'us').
        processor_id: The processor ID.
        processor_version: The processor version.
        file_path: Path to the file to process.
        mime_type: MIME type of the file.

    Returns:
        The processed Document AI document.
    """
    # Seeting the `api_endpoint` as we are using "eu" location and not "us"
    client = documentai.DocumentProcessorServiceClient(
        client_options=ClientOptions(
            api_endpoint=f"{location}-documentai.googleapis.com"
        )
    )

    # Creating a processor
    processor_name = client.processor_version_path(
        project_id, location, processor_id, processor_version
    )

    # Configure the process request
    request = documentai.ProcessRequest(
        name=processor_name,
        raw_document=documentai.RawDocument(content=file, mime_type=mime_type),
    )

    result = client.process_document(request=request)

    return result.document

def _extract_entities(document: documentai.Document) -> str:
    """
    Extract entities and their properties from a Document AI document.

    Args:
        document: The Document AI document object.

    Returns:
        A list of entities, including their properties.
    """
    entities = ""
    if document.entities:
        for entity in document.entities:
            key = entity.type_
            text_value = entity.text_anchor.content or entity.mention_text
            confidence = entity.confidence
            normalized_value = entity.normalized_value.text if entity.normalized_value else ""
            entities += f"* {repr(key)}: {repr(text_value)} ({confidence:.1%} confident)\n"
            if normalized_value:
                entities += f"* Normalized Value: {repr(normalized_value)}\n"
    
    return entities