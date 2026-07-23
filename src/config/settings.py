import os
from dotenv import load_dotenv

load_dotenv()


class Settings:

    url = {
        "ssc": "https://www.ssc.gov.jo/%D8%A3%D8%B3%D8%A6%D9%84%D8%A9-%D8%B9%D8%A7%D9%85%D8%A9/"
    }

    pdf = {
        "pdf_1": r"src\data\قانون_العمل_رقم_8_لسنة_1996_وتعديلاته.pdf",
    }

    groq_api_key = os.getenv("GROQ_API_KEY")


settings = Settings()
