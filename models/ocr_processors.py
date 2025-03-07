from enum import Enum

class OCRProcessors(Enum):
    DOCUMENT_OCR = "ec7278f01a93aa49" # default OCR processor, doesn't return entities
    EXPENSE_PARSER = "3f4a6dfbbde11c51" # pre-built OCR processor for receipts, returns entities
    CUSTOM_PARSER = "46f03ca0e2fce20f" # custom-built OCR processor (not trained enough) for our specific case, returns entities
    FORM_PARSER = "3ed4b722e56680da" # pre-built OCR processor for any kind of forms, returns entities
