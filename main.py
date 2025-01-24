import os

from dotenv import load_dotenv

import functions_calling as fc
from models.llm_api import LLM_API


def prompt_scrapnos(prompt):
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
The images on the pages are the thumbnails, but I want the original ones. To get them add the prefix https://mvcdn.fancaps.net/ + the id of the image and the extension. Do it a page at a time, save it in a 'Totoro' folder.
"""

# prompt = "Imagine a detailed workflow to write a novel with LLMs based on an user request. You have to take into account the constraints of the LLMs, which are the limited length for input and output they can read/write. So you need to split the process into a multi steps workflow, while trying to keep a coherent narrative, close to the idea of the user request. Write detailed system prompts needed into different files. Reread each of these system prompts to be sure they are detailed enough. Then write a python script to use this workflow, taking an user input the going through each steps and saving results (let's use MockLlmService in the code for now)."


prompt_scrapnos(prompt)
