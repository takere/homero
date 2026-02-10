import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()
geminiKey = os.getenv('GEMINI_API_KEY')

userInput = str(input('Describe the desired grade element:\nGenerate a GridIntegerQuestion with '))

client = genai.Client(api_key=geminiKey)

response = client.models.generate_content(
    model="gemini-2.0-flash",
    config=types.GenerateContentConfig(
        system_instruction="""You are a helpful AI assistant and the provided JSON structure describes a survey item that is a "GridIntegerQuestion". This item is identified with a "templateID" and "customID" of "TTT1". It includes lines containing grid integer items. Here's a detailed breakdown of the JSON:
            |
            1. **Top Level Attributes**:
            - `extents`: "SurveyItem", indicating this is a survey item.
            - `objectType`: "GridIntegerQuestion", specifying the type of survey item.
            - `templateIDGridIntegerQuestion
            3. **Lines**:
            - This part of the JSON contains an array called `lines`, each element having:
                - `extents`: "StudioObject" and `objectType`: "GridIntegerLine", which suggests a line within the grid integer question.
                - `gridIntegerList`: An array of `GridInteger` items.

            4. **Grid Integer Items**:
            - Each item within a `gridIntegerList` includes:
                - `extents`: "SurveyItem", showing it is a survey item.
                - `objectType`: "GridInteger", specifying the text type.
                - `templateID` and `customID`: Unique identifiers for each grid integer following the TTT1 format(e.g., "TTT1a", "TTT1b").
                - `dataType`: "Integer", indicating the type of data expected.
                - `label`: Contains inputs to GridInteger from the user (e.g., "GridInteger line1, column1 input", "GridInteger line1, column2 input").

            Overall, this JSON describes a structured layout of a grid integer question used in a survey:
'           
            ***{"extents":"SurveyItem","objectType":"GridIntegerQuestion","templateID":"TTT1","customID":"TTT1","metadata":{"extents":"StudioObject","objectType":"MetadataGroup","options":[]},"fillingRules":{"extends":"StudioObject","objectType":"FillingRules","options":{"mandatory":{"extends":"StudioObject","objectType":"Rule","validatorType":"mandatory","data":{"canBeIgnored":false,"reference":true}}}},"label":{"ptBR":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"GridIntegerQuestion input","formattedText":"GridIntegerQuestion input"},"enUS":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"","formattedText":""},"esES":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"","formattedText":""}},"lines":[{"extents":"StudioObject","objectType":"GridIntegerLine","gridIntegerList":[{"extents":"SurveyItem","objectType":"GridInteger","templateID":"TTT1a","customID":"TTT1a","dataType":"String","label":{"ptBR":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"GridInteger line1, column1 input","formattedText":"GridInteger line1, column1 input"},"enUS":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"","formattedText":""},"esES":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"","formattedText":""}},"layout":{"extents":"StudioObject","objectType":"LayoutGrid","width":100},"unit":{"ptBR":{"extends":"StudioObject","objectType":"Unit","oid":"","plainText":"","formattedText":""},"enUS":{"extends":"StudioObject","objectType":"Unit","oid":"","plainText":"","formattedText":""},"esES":{"extends":"StudioObject","objectType":"Unit","oid":"","plainText":"","formattedText":""}}},{"extents":"SurveyItem","objectType":"GridInteger","templateID":"TTT1b","customID":"TTT1b","dataType":"String","label":{"ptBR":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"GridInteger line1, column2 input","formattedText":"GridInteger line1, column2 input"},"enUS":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"","formattedText":""},"esES":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"","formattedText":""}},"layout":{"extents":"StudioObject","objectType":"LayoutGrid","width":100},"unit":{"ptBR":{"extends":"StudioObject","objectType":"Unit","oid":"","plainText":"","formattedText":""},"enUS":{"extends":"StudioObject","objectType":"Unit","oid":"","plainText":"","formattedText":""},"esES":{"extends":"StudioObject","objectType":"Unit","oid":"","plainText":"","formattedText":""}}}]},{"extents":"StudioObject","objectType":"GridIntegerLine","gridIntegerList":[{"extents":"SurveyItem","objectType":"GridInteger","templateID":"TTT1c","customID":"TTT1c","dataType":"String","label":{"ptBR":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"GridInteger line2, column1 input","formattedText":"GridInteger line2, column1 input"},"enUS":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"","formattedText":""},"esES":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"","formattedText":""}},"layout":{"extents":"StudioObject","objectType":"LayoutGrid","width":100},"unit":{"ptBR":{"extends":"StudioObject","objectType":"Unit","oid":"","plainText":"","formattedText":""},"enUS":{"extends":"StudioObject","objectType":"Unit","oid":"","plainText":"","formattedText":""},"esES":{"extends":"StudioObject","objectType":"Unit","oid":"","plainText":"","formattedText":""}}},{"extents":"SurveyItem","objectType":"GridInteger","templateID":"TTT1d","customID":"TTT1d","dataType":"String","label":{"ptBR":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"GridInteger line2, column2 input","formattedText":"GridInteger line2, column2 input"},"enUS":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"","formattedText":""},"esES":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"","formattedText":""}},"layout":{"extents":"StudioObject","objectType":"LayoutGrid","width":100},"unit":{"ptBR":{"extends":"StudioObject","objectType":"Unit","oid":"","plainText":"","formattedText":""},"enUS":{"extends":"StudioObject","objectType":"Unit","oid":"","plainText":"","formattedText":""},"esES":{"extends":"StudioObject","objectType":"Unit","oid":"","plainText":"","formattedText":""}}}]}]}***
            
            Your task is to generate this json object based on user input""",
            response_mime_type= "application/json"
        ),
    contents=f"Generate a GridIntegerQuestion with{userInput}. Do it step by step as specified by the system structure. Return it as a raw JSON, without spaces."
)

print(response.text)