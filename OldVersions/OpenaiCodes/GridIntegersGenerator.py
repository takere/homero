import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from generalFunctions import getTime

load_dotenv()
otus = os.getenv('OPENAI_API_KEY')

userInput = str(input('Describe the desired grade element:\nGenerate a GridIntegerQuestion with '))

client = OpenAI(api_key=otus)
completion = client.chat.completions.create(
    model = 'gpt-4o',
    messages = [
        {
            "role":"system",
            "content":"""You are a helpful AI assistant and the provided JSON structure describes a survey item that is a "GridIntegerQuestion". This item is identified with a "templateID" and "customID" of "TTT1". It includes lines containing grid integer items. Here's a detailed breakdown of the JSON:
            |
            1. **Top Level Attributes**:
            - `extents`: "SurveyItem", indicating this is a survey item.
            - `objectType`: "GridIntegerQuestion", specifying the type of survey item.
            - `templateID` and `customID`: Both are set to "TTT1", likely serving as identifiers.

            2. **Labels**:
            - Provided in three languages: Portuguese (Brazil), English (US), and Spanish (Spain).
            - Each language has a `plainText` and `formattedText`, but only Portuguese contains the actual text "GridIntegerQuestion input".

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
            
            Your task is to generate this json object based on user input"""
        },
        {
            "role":"user",
            "content":f"Generate a GridIntegerQuestion with{userInput}. Do it step by step as specified by the system structure. Return it as a raw JSON, without spaces."
        }
    ],
    response_format={"type": "json_object"}
)

print(completion.choices[0].message.content)
GridInteger = json.loads(completion.choices[0].message.content)

form = {
    "extents": "StudioObject",
    "objectType": "Survey",
    "oid": "dXNlclVVSUQ6W3VuZGVmaW5lZF1zdXJ2ZXlVVUlEOltkMzllZTg5MC05MDhkLTExZWYtOWZmYS1jOTM3YmMwNTQ1ODddcmVwb3NpdG9yeVVVSUQ6WyBOb3QgZG9uZSB5ZXQgXQ==",
    "identity": {
        "extents": "StudioObject",
        "objectType": "SurveyIdentity",
        "name": "testMultipleLabels",
        "acronym": "TTT",
        "recommendedTo": "",
        "description": "",
        "keywords": []
    },
    "metainfo": {
        "extents": "StudioObject",
        "objectType": "SurveyMetaInfo",
        "creationDatetime": "2024-10-22T15:53:48.697Z",
        "otusStudioVersion": ""
    },
    "dataSources": [],
    "itemContainer": [],
    "navigationList": [{
    "extents": "SurveyTemplateObject",
    "objectType": "Navigation",
    "origin": "BEGIN NODE",
    "index": 0,
    "inNavigations": [],
    "routes": [
        {
            "extents": "SurveyTemplateObject",
            "objectType": "Route",
            "origin": "BEGIN NODE",
            "destination": "TTT1",
            "name": "BEGIN NODE_TTT1",
            "isDefault": True,
            "conditions": []
        }
    ]
},
{
    "extents": "SurveyTemplateObject",
    "objectType": "Navigation",
    "origin": "END NODE",
    "index": 1,
    "inNavigations": [
        None,
        {
            "origin": "TTT1",
            "index": 2
        }
    ],
    "routes": []
},
{
    "extents": "SurveyTemplateObject",
    "objectType": "Navigation",
    "origin": "TTT1",
    "index": 2,
    "inNavigations": [
        {
            "origin": "BEGIN NODE",
            "index": 0
        }
    ],
    "routes": [
        {
            "extents": "SurveyTemplateObject",
            "objectType": "Route",
            "origin": "TTT1",
            "destination": "END NODE",
            "name": "TTT1_END NODE",
            "isDefault": True,
            "conditions": []
        }
    ]
}],
    "staticVariableList": [],
    "surveyItemGroupList": []
}

form.update({"itemContainer":[GridInteger]})

currentTime = getTime()
with open(f"GridInteger_{currentTime}.json", "w") as outfile: #saves json to a file
    json.dump(form, outfile)