# test_single.py
from openai import OpenAI
client = OpenAI()

resp = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "Be brief."},
        {"role": "user", "content": "Say hello in one sentence."}
    ],
)
print(resp.choices[0].message.content)