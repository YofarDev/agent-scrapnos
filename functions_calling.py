import datetime
import json
import os

import llm_service
import utils
from models.agent_function import functions, get_functions_string
from models.llm_api import LLM_API


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
        json_response = check_functions(
            api=api,
            project=project,
            prompt=prompt,
            count=i,
            previous_results=results,
        )
        results = ""
        utils.save_as_json_file(json_response, f"{i}_step", is_step=True)
        print("Response saved as " + str(i) + "_step.json")
        if json_response != "" and json_response["functions_to_call"] != []:
            for function in json_response["functions_to_call"]:
                func_name = function["function"]
                func_params = function["parameters"]
                if isinstance(func_params, str) and len(func_params) > 150:
                    func_params = func_params[:150] + "[...]"
                # Find the corresponding AgentFunction object
                agent_func = next((f for f in functions if f.name == func_name), None)
                if agent_func:
                    try:
                        result = agent_func.call(func_params)
                        results += f"  {func_name}({func_params}) -> \n{result}"
                    except ValueError as e:
                        print(e)
                else:
                    print(f"Unknown function: {func_name}")
        is_last_step = (
            json_response == ""
            or json_response["is_last_step"] == "true"
            or json_response["is_last_step"]
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
                previous_rationales += (
                    f"Step {step_num}: {step_data['current_step_rationale']}\n"
                )
            p += f"\nPrevious steps done:\n{previous_rationales}"
            json_data = load_json(project, count - 1)
            p += f"\nResults from function calling of previous step [iteration {count - 1}] :\n'''{previous_results}'''"
            p += f"\n\nWhat to do now:\n{json_data['next_instructions']}"
        with open("assets/functions_caller.txt") as f:
            sp = f.read()
        functions_str = get_functions_string()
        sp = sp.replace("$FUNCTIONS_LIST", functions_str)
        utils.save_as_file(p, f"{count}_prompt", is_step=True)
        print("Prompt saved as " + str(count) + "_prompt.txt")
        response =  llm_service.prompt_llm(prompt=p, system_prompt=sp, api=api)
        full_response = response.strip()
        i = 0
        while not is_response_completed(full_response):
            print(f"LLM response incomplete, continuing... [{i}]")
            if i > 20:
                raise Exception("Something went wront with the LLM response (tool long or badly formatted).")
            p += "\nPrevious response was interrupted. Here is the previous response, continue exactly from there (responses will be automatically merged):\n" + full_response
            response =  llm_service.prompt_llm(prompt=p, system_prompt=sp, api=api)
            full_response = response.strip()
            i += 1
        json_response = utils.extract_json_from_string(full_response)
        return json_response
    except Exception as e:
        print("check_functions EXCEPTION", e)
        raise Exception("An error occurred while checking functions.")
    

def is_response_completed(response:str)->bool:
    return response.endswith('}') or response.endswith('```')


def load_json(project, step):
    with open(f"output/{project}/steps/{step}_step.json", "r") as f:
        return json.load(f)
    
    