import functions_calling as fc


def prompt_scrapnos(prompt):
    fc.function_calling_wrapper(prompt)


prompt = """
Scrap the images from the movie My neighbor Totoro for the first 5 pages of https://fancaps.net/movies/MovieImages.php?name=My_Neighbor_Totoro&movieid=1492&page=1. 
The images on the pages are the thumbnails, but I want the original ones. To get them add the prefix https://mvcdn.fancaps.net/ + the id of the image and the extension.
Do it one page at a time.
"""

prompt_scrapnos(prompt)
