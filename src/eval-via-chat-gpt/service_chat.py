import openai

import config

def _get_completion(prompt, model="gpt-3.5-turbo", temperature = 0, messages = None, dummy_response = None):
    if config.is_dry_run:
        return dummy_response

    if messages is None:
        messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        # Temperature is the degree of randomness of the model's output
        # 0 would be same each time. 0.7 or 1 would be difference each time, and less likely words can be used:
        temperature=temperature,
    )
    return response.choices[0].message["content"]

def send_prompt(prompt, show_input = True, show_output = True, dummy_response = None):
    if show_input:
        print("=== INPUT ===")
        print(prompt)

    response = _get_completion(prompt, temperature=config.temperature, dummy_response=dummy_response)

    if show_output:
        print("=== RESPONSE ===")
        print(response)

    return response
