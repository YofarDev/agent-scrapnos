import datetime
import json
import os
import time

import llm_service
import utils
from models.llm_api import LLM_API

functions = [
    "fetch_static_html_body_only(String url)",
    "fetch_dynamic_content_with_playwright(String url)",
    "save_urls_as_images(List<String> list_urls, String folder_name)",
    "save_as_txt_file(String txt, String filename)",
    "save_as_json_file(Map<String, Object> data, String filename)",
    "open_file_as_string(String filename)",
]


def function_calling_wrapper(prompt: str, api: LLM_API):
    project = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    utils.project = project
    os.makedirs(f"output/{project}", exist_ok=True)
    is_last_step = False
    i = 0
    results = ""
    while not is_last_step:
        # Temporary hard coded limit
        if i == 20:
            break
        time.sleep(1)
        json_response = check_functions(
            api=api,
            project=project,
            prompt=prompt,
            count=i,
            previous_results=results,
        )
        results = ""
        save_json_as_file(json_response, f"step_{i}", project, is_step=True)
        print("Response saved as step_" + str(i) + ".json")
        if json_response == "" or json_response["functions_to_call"] == []:
            return results
        for function in json_response["functions_to_call"]:
            if function["function"] == "fetch_static_html_body_only":
                html = utils.fetch_static_html_body_only(function["parameters"]["url"])
                results += (
                    f"{function['function']} {function['parameters']['url']} : \n{html}"
                )
            elif function["function"] == "fetch_dynamic_content_with_playwright":
                html = utils.fetch_dynamic_content_with_playwright(
                    function["parameters"]["url"]
                )
                results += (
                    f"{function['function']} {function['parameters']['url']} : \n{html}"
                )
            elif function["function"] == "save_urls_as_images":
                result = utils.save_urls_as_images(
                    function["parameters"]["list_urls"],
                    function["parameters"]["folder_name"],
                )
                results += f"{function['function']} : \n{result}"
            elif function["function"] == "save_as_txt_file":
                result = utils.save_as_txt_file(
                    function["parameters"]["txt"], function["parameters"]["filename"]
                )
                results += f"{function['function']} : \n{result}"
            elif function["function"] == "save_as_json_file":
                result = utils.save_as_json_file(
                    function["parameters"]["data"], function["parameters"]["filename"]
                )
                results += f"{function['function']} : \n{result}"
            elif function["function"] == "open_file_as_string":
                result = utils.open_file_as_string(function["parameters"]["filename"])
                results += f"{function['function']} : \n{result}"
            else:
                print(f"Unknown function: {function['function']}")
        is_last_step = (
            json_response["is_last_step"] == "true" or json_response["is_last_step"]
        )
        i += 1


def check_functions(
    project: str, prompt: str, count: int, previous_results: str, api: LLM_API
):
    try:
        p = f"""
        Initial request : {prompt}
        Iteration count : {count}
        """
        if count > 0:
            json_data = load_json(project, count - 1)
            p += f"Previous results :\n{previous_results}"
            p += f"Previous steps rationale :\n{json_data['current_step_rationale']}"
            p += f"Next step instructions :\n{json_data['next_instructions']}"
        with open("assets/functions_caller.txt") as f:
            sp = f.read()
        functions_str = "\n".join(functions)
        sp = sp.replace("$FUNCTIONS_LIST", functions_str)
        utils.save_as_txt_file(p, f"prompt_{count}.txt", is_step=True)
        response = llm_service.prompt_llm(prompt=p, system_prompt=sp, api=api)
        json_response = utils.extract_json_from_string(response)
        return json_response
    except Exception as e: 
        print("check_functions EXCEPTION", e)
        raise Exception("An error occurred while checking functions.")
        


def save_json_as_file(json_data, filename, project):
    with open(f"output/{project}/{filename}.json", "w") as f:
        f.write(json.dumps(json_data, indent=4))


def load_json(project, step):
    with open(f"output/{project}/step_{step}.json", "r") as f:
        return json.load(f)
