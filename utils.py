import google.generativeai as genai
import os
from dotenv import load_dotenv


load_dotenv()


GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=GOOGLE_API_KEY)


def get_suggestion(description, type):
    """
    give suggestions for description section using gemini (free alternative to openai's chatgpt api)
    """

    if type == "education":
        prompt = f"Improve the following education experience description for resume: {description}"
    elif type == "experience":
        prompt = f"Improve the following professional experience description for resume: {description}"

    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text
