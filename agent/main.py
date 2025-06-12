from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()

client = OpenAI()

# response = client.responses.create(
#     model="gpt-5",
#     input="Write a one-sentence bedtime story about a unicorn."
# )

# SYSTEM_PROMPT = """You are a javascript developer, you have experience of 10 years. You will only answer questions related to javascript only. If a user asks you anything apart from javascript then you can roast them.

# Examples:
# User: How to write python?
# Assistant: what makes you think I am a python developer.

# Examples:
# User: How to write a function in javascript?
# Assistant: There are 2 ways to write function in javascript one is normal function and other is arrow function. function(){} or const res = () => {}
# """

SYSTEM_PROMPT = """
    You are an helpful AI assistant who is specialized in resolving user query. For the given user input, analyse the input and break down the problem step by step.
    
    The steps are you get a user input, you analyse, you think, you think again, and think for several times and then return the output with an explanation.
    
    Follow the steps in sequence that is "analyse", "think", "output", "validate" and finally "result".
    
    Rules:
    1. Follow the strict JSON output as per schema.
    2. Always perform one step at a time and wait for the next input.
    3. Carefully analyse the user query.
    
    Output Format:
    {{"step": "string", "content": "string"}}
    
    Example:
    Input: What is 2 + 2
    Output: {{"step": "analyse", "content": "Alright! The user is interested in maths query and he is asking a basic arthematic operation"}}
    Output: {{"step": "think", "content": "To perform this addition, I must go from left to right and add all the operands."}}
    Output: {{"step": "output", "content": "4"}}
    Output: {{"step": "validate", "content": "Seems like 4 is correct ans for 2 + 2}}
    Output: {{"step": "result", "content": "2 + 2 = 4 and this is calculated by adding all numbers"}}
"""

# response = client.chat.completions.create(
#     model='chatgpt-4o-latest',
#     response_format={"type": "json_object"},
#     messages=[
#         {"role": "system", "content": SYSTEM_PROMPT},
#         {"role": "user", "content": "how to learn python fast? is python similar to javascript?"},
#         {"role": "assistant", "content": json.dumps({"step": "analyse", "content": "The user is asking two separate questions: one about learning Python quickly, and another about comparing Python with JavaScript in terms of similarity."})},
#         {"role": "assistant", "content": json.dumps({"step": "think", "content": "The user has asked two separate but related questions: one about strategies to learn Python quickly, and the other about how Python compares to JavaScript. This suggests the user may have some familiarity with one language and is looking to understand or transition to the other."})},
#         {"role": "assistant", "content": json.dumps({"step": "output", "content": "To address this properly, I need to break this into two parts: (1) explain effective methods for quickly learning Python, and (2) compare Python's syntax, paradigms, and use-cases with those of JavaScript."})},
#         {"role": "assistant", "content": json.dumps({"step": "validate", "content": "Confirmed that each part of the output addresses the user queries accurately and meaningfully: guidance on learning Python and comparison with JavaScript."})}
#     ]
# )


messages = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

query = input("> ")
messages.append({"role": "user", "content": query})

while True:
    response = client.chat.completions.create(
        model="gpt-4",
        response_format={'type': 'json_object'},
        messages=messages
    )
    
    messages.append({"role": "assistant", "content": response.choices[0].message.content})
    parsed_response = json.loads(response.choices[0].message.content)
    
    if parsed_response.get("step") != 'result':
        print("          🧠:", parsed_response.get("content"))
        continue
    
    print("🤖:", parsed_response.get("content"))
    break

# print(response.choices[0].message.content)