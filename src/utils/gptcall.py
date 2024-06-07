import openai

def post_processing(response: str) -> str:
    """
    This function use to parse Groovy code snippet

    Args:
        response (str): Response to be parsed

    Returns:
        str: Parse Groovy code
    """
    # Extract the code between ```groovy and ```
    if "```groovy" not in response:
        return response
    return response.split("```groovy")[1].split("```")[0]


def GPTChatCompletion(prompt, system="", model='gpt-4-turbo', temperature=0, top_p = 1, max_tokens=-1):
    if system:
        messages = [
            {"role": "system", "content": system},
            {"role": "user", "content": prompt}
        ]
    else:
        messages = [
            {"role": "user", "content": prompt}
        ]
        
    try:
        if max_tokens == -1:
            response = openai.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                top_p = top_p
            )
        else:
            response = openai.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p
            )
        return response.choices[0].message.content
    except Exception as e:
        print(e)
        return None
