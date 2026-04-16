import json
import subprocess

def call_llm(prompt):
    result = subprocess.run(
        ["ollama", "run", "llama3"],
        input=prompt.encode("utf-8"),
        capture_output=True
    )
    return result.stdout.decode("utf-8", errors="ignore")


def extract_with_llm(user_input, current_data):
    prompt = f"""
You are an intelligent form filling assistant.

Your job:
- Understand user input
- Extract or UPDATE fields

Fields:
name, age, email, city

Current data:
{json.dumps(current_data)}

Rules:
- Return ONLY JSON
- If user says "change/update", modify existing field
- If new info, add it
- Do NOT return empty unless nothing found

Examples:

Input: My name is John and I am 25  
Output: {{"name": "John", "age": "25"}}

Input: change email to abc@gmail.com  
Output: {{"email": "abc@gmail.com"}}

User input:
{user_input}

Output:
"""

    response = call_llm(prompt)

    try:
        start = response.find("{")
        end = response.rfind("}") + 1
        return json.loads(response[start:end])
    except:
        return {}