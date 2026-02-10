from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

num = int(input('Digite o número de elementos desejados: '))

otus_openai = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=otus_openai)
completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {
            "role": "system",
            "content": """You are a helpful assistant whose task is to generate several prompts to the user for testing purposes. These prompts are inputs for a form generation aplication. 

            ***The list of possible elements is: [SingleSelectionQuestion, CheckboxQuestion, CalendarQuestion, IntegerQuestion, DecimalQuestion, TextQuestion, EmailQuestion, TimeQuestion, PhoneQuestion, TextItem]***

            ***Check the following example: one SingleSelectionQuestion item, with the following question: 'What is your City?' with the following options: 'Porto', 'Alegrete', 'Viamao'. Include one CheckboxQuestion item with the following question: 'what is do you eat?' with the following options: 'meat', 'vegetables'. Include one CalendarQuestion with the following question: 'When is your birthday?'. Include one IntegerQuestion with the following question: 'How Old are you?***. Generate a response without lines and spaces"""
        },
        {"role": "user", 
            "content": f"Generate a prompt with {num} elements in the form"}
    ]
)

print(completion.usage.total_tokens)
print(completion.choices[0].message.content)

