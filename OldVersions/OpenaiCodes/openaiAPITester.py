import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
otus = os.getenv('OPENAI_API_KEY')

client = OpenAI(api_key=otus)
completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", 
         "content": "Resume existence in one word"}
    ]
)

print(completion.usage.total_tokens)
print(completion.choices[0].message.content)

