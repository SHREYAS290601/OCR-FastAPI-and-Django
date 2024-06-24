from PIL import Image
import pytesseract
import os
from concurrent.futures import ThreadPoolExecutor
import google.generativeai as genai
from dotenv import load_dotenv
import json

load_dotenv()
_executor = ThreadPoolExecutor(1)


async def read_data_on_image(SessionID, fextention):
    img = Image.open(f"output/{SessionID}.{fextention}")
    text = pytesseract.image_to_string(img)
    return text


async def OCR(SessionID, fextention):
    return await read_data_on_image(SessionID, fextention)


genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction="""
    Generate "summary", "categories", "wordcloud" and "key_points" for the given text.
    *Do not change the names of the keys*.
    *Summary must be 3-4 sentences long and in layman explanation, categories must be in a list having 3-4 categories, wordcloud must be a word cloud of the text in a list and key-points must be 3-4 key points of the text*.
    The summary must be concise and coherent, the categories must be relevant to the text, the wordcloud must be text count and the key-points must be relevant to the text.
    Response must be in JSON format.
""",
)


async def get_information(text):
    response = (
        (await model.generate_content_async(text))
        .text.replace("```", "")
        .replace("json", "")
        .strip()
    )
    # print(response)
    return json.loads(response)
