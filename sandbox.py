import utils


results = utils.fetch_static_html_body_only("https://fancaps.net/movies/MovieImages.php?name=My_Neighbor_Totoro&movieid=1492&page=1")
print(results)
