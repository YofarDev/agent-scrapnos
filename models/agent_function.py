import utils


class AgentFunction:
    def __init__(self, name, description, parameters):
        self.name = name
        self.description = description
        self.parameters = parameters

    def to_string(self):
        params_str = ", ".join(
            [f"{param}: {info['type']}" for param, info in self.parameters.items()]
        )
        return f"{self.name}({params_str})\n=> {self.description}\n"

    def call(self, parameters):
        if self.name == "fetch_static_html":
            return utils.fetch_static_html_body_only(parameters["url"])
        elif self.name == "fetch_dynamic_html":
            return utils.fetch_dynamic_content_with_playwright(parameters["url"])
        elif self.name == "download_and_save_images":
            return utils.save_urls_as_images(
                parameters["image_urls"], parameters["folder_name"]
            )
        elif self.name == "save_as_file":
            return utils.save_as_file(parameters["txt"], parameters["filename"])
        elif self.name == "save_as_json_file":
            return utils.save_as_json_file(parameters["data"], parameters["filename"])
        elif self.name == "json_to_csv":
            return utils.save_json_as_csv(parameters["data"], parameters["filename"])
        elif self.name == "open_file_as_string":
            return utils.open_file_as_string(parameters["filename"])
        else:
            raise ValueError(f"Unknown function: {self.name}")


functions = [
    AgentFunction(
        name="fetch_dynamic_html",
        description="Fetches the fully rendered HTML content of a webpage, including dynamically loaded elements. Prefer this over most of the time, except when dealing with urls/images.",
        parameters={
            "url": {"type": "String", "description": "The URL of the webpage to fetch."}
        },
    ),
    AgentFunction(
        name="fetch_static_html",
        description="Fetches the static HTML content of a webpage. Use this when we need content only available in the HTML source like urls.",
        parameters={
            "url": {"type": "String", "description": "The URL of the webpage to fetch."}
        },
    ),
    AgentFunction(
        name="download_and_save_images",
        description="Downloads images from a list of URLs and saves them to the specified folder.",
        parameters={
            "image_urls": {
                "type": "List<String>",
                "description": "A list of image URLs to download.",
            },
            "folder_name": {
                "type": "String",
                "description": "The name of the folder where the images will be saved.",
            },
        },
    ),
    AgentFunction(
        name="save_as_file",
        description="Saves the provided text content as a file.",
        parameters={
            "txt": {"type": "String", "description": "The text content to save."},
            "filename": {
                "type": "String",
                "description": "The name of the file to save the text in.",
            },
        },
    ),
    AgentFunction(
        name="save_as_json_file",
        description="Saves the provided data as a .json file.",
        parameters={
            "data": {"type": "Object", "description": "The data to save as JSON."},
            "filename": {
                "type": "String",
                "description": "The name of the file to save the JSON in.",
            },
        },
    ),
    AgentFunction(
        name="json_to_csv",
        description="Converts JSON data to CSV format and saves it as a .csv file.",
        parameters={
            "data": {
                "type": "Object",
                "description": "The JSON data to convert and save.",
            },
            "filename": {
                "type": "String",
                "description": "The name of the file to save the CSV in.",
            },
        },
    ),
    AgentFunction(
        name="open_file_as_string",
        description="Opens a file and returns its content as a string.",
        parameters={
            "filename": {
                "type": "String",
                "description": "The name of the file to open.",
            },
        },
    ),
]


def get_functions_string():
    f = ""
    for function in functions:
        f += function.to_string() + "\n"
    return f


# Print each function using the to_string method
