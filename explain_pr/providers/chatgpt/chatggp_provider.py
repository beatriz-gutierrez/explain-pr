import openai

MAX_TOKENS = 16000
SUMMARY_WORDS = 200

def get_pull_request_summary(pull_request_content: str) -> str:
    print("> Summarizing pull request")

    # no randomness
    temperature = 0

    prompt = f"""
    Generate a summary of at maximum {SUMMARY_WORDS} words from the following pull request, delimited by triple @ symbols.
    Use a technical language, and first add a summary of the content in 3 lines and then explain each change in the pull 
    request using bullet points. Then, explore issues in the code such as errors, bugs, or potential improvements.
    In case of errors or bugs, add the code that implements the fix delimited by triple '''.
    Finally, add a conclusion with the impact of the changes in the codebase.

    Content: @@@{pull_request_content}@@@
    """

    model = "gpt-3.5-turbo"
    messages = [{"role": "user", "content": prompt}]
    completion = openai.ChatCompletion.create(model=model, messages=messages, temperature=temperature)

    return completion.choices[0].message.content
