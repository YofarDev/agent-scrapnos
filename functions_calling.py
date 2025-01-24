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
        utils.save_as_json_file(json_response, f"{i}_step", is_step=True)
        print("Response saved as" + str(i) + "_step.json")
        if json_response != "" and json_response["functions_to_call"] != []:
            for function in json_response["functions_to_call"]:
                if function["function"] == "fetch_static_html_body_only":
                    html = utils.fetch_static_html_body_only(function["parameters"]["url"])
                    results += (
                        f"  {function['function']}({function['parameters']['url']}) -> \n{html}"
                    )
                elif function["function"] == "fetch_dynamic_content_with_playwright":
                    html = utils.fetch_dynamic_content_with_playwright(
                        function["parameters"]["url"]
                    )
                    results += (
                        f"  {function['function']}( {function['parameters']['url']}) -> \n{html}"
                    )
                elif function["function"] == "save_urls_as_images":
                    result = utils.save_urls_as_images(
                        function["parameters"]["list_urls"],
                        function["parameters"]["folder_name"],
                    )
                    results += f"   {function['function']}(list) -> {result}"
                elif function["function"] == "save_as_txt_file":
                    result = utils.save_as_txt_file(
                        function["parameters"]["txt"], function["parameters"]["filename"]
                    )
                    results += f"   {function['function']}(txt) -> {result}"
                elif function["function"] == "save_as_json_file":
                    result = utils.save_as_json_file(
                        function["parameters"]["data"], function["parameters"]["filename"]
                    )
                    results += f"   {function['function']}(json_data) -> {result}"
                elif function["function"] == "open_file_as_string":
                    result = utils.open_file_as_string(function["parameters"]["filename"])
                    results += f"   {function['function']}(filename) -> \n{result}"
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
        p = f"The initial request was: {prompt}"
        p += f"\nIteration count: {count}"
        if count > 0:
            previous_rationales = ""
            for step_num in range(count):
                step_data = load_json(project, step_num)
                previous_rationales += f"Step {step_num}: {step_data['current_step_rationale']}\n"
            p += f"\nPrevious steps done:\n{previous_rationales}"
            json_data = load_json(project, count - 1)
            p += f"\nResults from function calling of previous step [iteration {count - 1}] :\n{previous_results}"
            p += f"\nWhat to do now:\n{json_data['next_instructions']}"
        with open("assets/functions_caller.txt") as f:
            sp = f.read()
        functions_str = "\n".join(functions)
        sp = sp.replace("$FUNCTIONS_LIST", functions_str)
        utils.save_as_txt_file(p, f"{count}_prompt", is_step=True)
        print("Prompt saved as" + str(count) + "_prompt.txt")
        response = llm_service.prompt_llm(prompt=p, system_prompt=sp, api=api)
        json_response = utils.extract_json_from_string(response)
        return json_response
    except Exception as e: 
        print("check_functions EXCEPTION", e)
        raise Exception("An error occurred while checking functions.")
        



def load_json(project, step):
    with open(f"output/{project}/steps/{step}_step.json", "r") as f:
        return json.load(f)
