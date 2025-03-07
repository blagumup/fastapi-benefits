from enum import Enum

class BenefitCategory(Enum):
    MEDICAL_INSURANCE_PERSONAL = "Medical Insurance personal"
    PROFESSIONAL_DEVELOPMENT = "Professional development (incl. English courses)"
    ENGLISH_COURSES = "English courses (internal / external)"
    SPANISH_COURSES = "Spanish courses"
    BUSINESS_COMMUNICATION = "Business / Client communication"
    SPORTS_PROGRAM = "Sports program"
    PSYCHOTHERAPY = "Psychotherapy"
    MASSAGES_PHYSIOTHERAPY = "Massages, physiotherapy, kinesiotherapy, etc."
    HOBBY = "Hobby"
    SPA_COMPLEX = "SPA complex / Facial, body cosmetology, etc"
    VITAMIN_COMPLEX = "Vitamin complex / Nutritionist consultation"
    PET_CARE = "Pet care (veterinary clinic, classes with cynologist, groomings, pet store)"
    FAMILY_MEDICAL_INSURANCE = "Family medical insurance"

    UNDEFINED = "Undefined"