import time

import gemini_service
import utils

functions = [
    "save_urls_as_images(List<String> list_urls, String folder_name)",
    "get_html_from_url(String url)",
]


def function_calling_wrapper(prompt):
    is_last_step = False
    i = 0
    results = ""
    next_step_instructions = ""
    while not is_last_step:
        # Temporary hard coded limit
        if i == 20:
            break
        time.sleep(0.5)
        json_response = check_functions(
            prompt=prompt,
            count=i,
            previous_results=results,
            next_step_instructions=next_step_instructions,
        )
        results = ""
        next_step_instructions = ""
        print(f"{json_response} [{i}] ")
        if json_response == "" or json_response["functions_to_call"] == []:
            return results
        for function in json_response["functions_to_call"]:
            if function["function"] == "save_urls_as_images":
                result = utils.save_urls_as_images(
                    function["parameters"]["list_urls"],
                    function["parameters"]["folder_name"],
                )
                results += f"{function['function']} : \n{result}"
            elif function["function"] == "get_html_from_url":
                html = utils.get_html_from_url(function["parameters"]["url"])
                results += (
                    f"{function['function']} {function['parameters']['url']} : \n{html}"
                )
        i += 1
        is_last_step = (
            json_response["is_last_step"] == "true"
            or json_response["is_last_step"]
        )
        next_step_instructions = json_response["next_step_instructions"]


def check_functions(prompt, count, previous_results, next_step_instructions):
    p = f"""
    Initial request : {prompt}
    Iteration count : {count}
    """
    if count > 0:
        p += f"Previous results :\n{previous_results}"
        p += f"Next step instructions :\n{next_step_instructions}"
    with open("assets/functions_caller.txt") as f:
        sp = f.read()
    functions_str = "\n".join(functions)
    sp = sp.replace("$FUNCTIONS_LIST", functions_str)
    response = gemini_service.prompt_model(prompt=p, system_prompt=sp)
    json_response = utils.extract_json_from_string(response)
    return json_response

