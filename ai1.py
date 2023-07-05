import openai
import os

OPENAI_KEY=""

# key is in .openai.key if it is exist
# is file exist?
if os.path.isfile(".openai.txt"):
    with open(".openai.txt") as f:
        OPENAI_KEY = f.read().strip()

def ask_gpt3(question, personality="You are AI assistant"):
    if len(OPENAI_KEY) == 0:
        return "OPENAI_KEY not available. This is simulated answer."

    openai.api_key = OPENAI_KEY

    # Generate the chat response
    response = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=[
        {"role": "system", "content": f"{personality}"},
        {"role": "user", "content": f"{question}"},
        ]
    )

    # Extract and return the answer from the response
    try:
        answer = response.choices[0].message['content']
    except:
        answer = "Something strange happened when I tried to answer. :("
    
    return answer

