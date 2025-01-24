import time

import google.generativeai as genai
from google.generativeai.types import HarmBlockThreshold, HarmCategory
from openai import OpenAI

from models.llm_api import LLM_API

last_used = 0

def prompt_llm(system_prompt: str, prompt: str, api: LLM_API) -> str:
    global last_used
    current_time = time.time() * 1000
    if last_used > 0 and api.delay_ms > 0:
        time_since_last_call = current_time - last_used
        if time_since_last_call < api.delay_ms:
            time.sleep((1000 - time_since_last_call) / 1000)
    last_used = current_time
    if api.is_gemini:
        return prompt_gemini(system_prompt, prompt, api)
    else:
        return prompt_openai(system_prompt, prompt, api)


def prompt_gemini(system_prompt: str, prompt: str, api: LLM_API):
    genai.configure(api_key=api.api_key)
    model = genai.GenerativeModel(api.model, system_instruction=system_prompt)
    response = model.generate_content(
        prompt,
        safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        },
    )
    return response.text


def prompt_openai(system_prompt: str, prompt: str, api: LLM_API) -> str:
    client = OpenAI(api_key=api.api_key, base_url=api.url)
    response = client.chat.completions.create(
        model=api.model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt},
        ],
        stream=False,
        max_tokens=8192,
    )
    return response.choices[0].message.content
