import os
import openai


def ask_GPT(my_message: str) -> str:
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = openai.chat.completions.create(
        model="gpt-4.1",  # Or "gpt-4", "gpt-3.5-turbo", etc.
        messages=[
            {"role": "user", "content": my_message},
        ],
        max_tokens=5000,
        temperature=0.7,
    )
    return response.choices[0].message.content.strip()


def test_ask_GPT0():
    openai.api_key = os.getenv("OPENAI_API_KEY")
    print('\n', openai.api_key)


def test_ask_GPT1():
    print(ask_GPT("This is a test. Just echo my message."))


def test_ask_GPT():
    code = ask_GPT("This is an API-request"
                   "I am coming back again to Stepfun_1; the last request was aborted."
                   "Adding N step functions requires N calls of __add__, which is slow, O(n^2)"
                   "Write a method sum(*fs) that returns the sum of all fs"
                   "and, likewise, multiply(*fs). Apply heapq.merge to all functions at a time.")

    target = "../../sandbox/stepfunctions/stepfun_2__.py"
    with open(target, "w") as f:
        f.write(code)


def test_token():
    import tiktoken

    program = "../../sandbox/stepfunctions/stepfun_1.py"

    with open(program) as f:
        code = f.read()

    encoding = tiktoken.encoding_for_model("gpt-4")
    tokens = encoding.encode(code)
    print("\nNumber of tokens:", len(tokens))
