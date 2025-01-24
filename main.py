import os

from dotenv import load_dotenv

import functions_calling as fc
from models.llm_api import LLM_API


def run_scrapnos(prompt):
    load_dotenv()
    gemini = LLM_API(
        model="gemini-2.0-flash-exp",
        api_key=os.getenv("GEMINI_API_KEY"),
        is_gemini=True,
        delay_ms=1000,
    )
    #     deepseek = LLM_API(
    #         model="deepseek-chat",
    #         api_key=os.getenv("DEEPSEEK_API_KEY"),
    #         is_gemini=False,
    #         url="https://api.deepseek.com/",
    #         delay_ms=1000,
    # )
    fc.function_calling_wrapper(prompt, gemini)


prompt = """
Scrap the images from the movie My neighbor Totoro for the first 5 pages of https://fancaps.net/movies/MovieImages.php?name=My_Neighbor_Totoro&movieid=1492&page=.
The images on the pages are the thumbnails, but I want the original ones. To get them add the prefix https://mvcdn.fancaps.net/ + the id of the image and the extension. 
Do it a page at a time, save it in a 'Totoro' folder.
"""

run_scrapnos(prompt)
