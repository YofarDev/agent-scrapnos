import json
import utils

raw = """
{
                    "museums": [
                        "Ambierle",
                        "Musée Alice Taverne",
                        "Saint-Étienne",
                        "Musée d'art moderne",
                        "Musée d'art et d'industrie",
                        "Musée du vieux Saint-Étienne",
                        "Musée de la mine",
                        "Musée des transports urbains de Saint-Étienne et sa région",
                        "L'Astronef",
                        "Saint-Etienne Mine Museum",
                        "Feurs",
                        "Musée d'Assier"
                    ]
                },
"""

# Load JSON data
json_data = utils.extract_json_from_string(raw)


utils.save_json_as_csv(json_data, "museums_in_la_loire.csv")
