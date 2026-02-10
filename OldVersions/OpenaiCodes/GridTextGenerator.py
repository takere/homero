import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from generalFunctions import getTime

load_dotenv() #loads enviroment variables from env file

otus = os.getenv('OPENAI_API_KEY') #loads api key

userInput = str(input('Describe the desired grade element:\nGenerate a GridTextQuestion with '))

client = OpenAI(api_key=otus)
completion = client.chat.completions.create(
    model = 'gpt-4o',
    messages = [
        {
            "role":"system",
            "content":"""You are a helpful AI assistant and the provided JSON structure describes a survey item that is a "GridTextQuestion". This item is identified with a "templateID" and "customID" of "TTT1". It includes lines containing grid text items. Here's a detailed breakdown of the JSON:
            |
            1. **Top Level Attributes**:
            - `extents`: "SurveyItem", indicating this is a survey item.
            - `objectType`: "GridTextQuestion", specifying the type of survey item.
            - `templateID` and `customID`: Both are set to "TTT1", likely serving as identifiers.

            2. **Labels**:
            - Provided in three languages: Portuguese (Brazil), English (US), and Spanish (Spain).
            - Each language has a `plainText` and `formattedText`, but only Portuguese contains the actual text "GridTextQuestion input".

            3. **Lines**:
            - This part of the JSON contains an array called `lines`, each element having:
                - `extents`: "StudioObject" and `objectType`: "GridTextLine", which suggests a line within the grid text question.
                - `gridTextList`: An array of `GridText` items.

            4. **Grid Text Items**:
            - Each item within a `gridTextList` includes:
                - `extents`: "SurveyItem", showing it is a survey item.
                - `objectType`: "GridText", specifying the text type.
                - `templateID` and `customID`: Unique identifiers for each grid text following the TTT1 format (e.g., "TTT1a", "TTT1b").
                - `dataType`: "String", indicating the type of data expected.
                - `label`: Contains inputs to gridText from the user (e.g., "gridText line1, column1 input", "gridText line1, column2 input").

            Overall, this JSON describes a structured layout of a grid text question used in a survey:
'            
            ***{"extents":"SurveyItem","objectType":"GridTextQuestion","templateID":"TTT1","customID":"TTT1","metadata":{"extents":"StudioObject","objectType":"MetadataGroup","options":[]},"fillingRules":{"extends":"StudioObject","objectType":"FillingRules","options":{"mandatory":{"extends":"StudioObject","objectType":"Rule","validatorType":"mandatory","data":{"canBeIgnored":false,"reference":true}}}},"label":{"ptBR":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"GridTextQuestion input","formattedText":"GridTextQuestion input"},"enUS":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"","formattedText":""},"esES":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"","formattedText":""}},"lines":[{"extents":"StudioObject","objectType":"GridTextLine","gridTextList":[{"extents":"SurveyItem","objectType":"GridText","templateID":"TTT1a","customID":"TTT1a","dataType":"String","label":{"ptBR":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"gridText line1, column1 input","formattedText":"gridText line1, column1 input"},"enUS":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"","formattedText":""},"esES":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"","formattedText":""}},"layout":{"extents":"StudioObject","objectType":"LayoutGrid","width":100},"unit":{"ptBR":{"extends":"StudioObject","objectType":"Unit","oid":"","plainText":"","formattedText":""},"enUS":{"extends":"StudioObject","objectType":"Unit","oid":"","plainText":"","formattedText":""},"esES":{"extends":"StudioObject","objectType":"Unit","oid":"","plainText":"","formattedText":""}}},{"extents":"SurveyItem","objectType":"GridText","templateID":"TTT1b","customID":"TTT1b","dataType":"String","label":{"ptBR":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"gridText line1, column2 input","formattedText":"gridText line1, column2 input"},"enUS":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"","formattedText":""},"esES":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"","formattedText":""}},"layout":{"extents":"StudioObject","objectType":"LayoutGrid","width":100},"unit":{"ptBR":{"extends":"StudioObject","objectType":"Unit","oid":"","plainText":"","formattedText":""},"enUS":{"extends":"StudioObject","objectType":"Unit","oid":"","plainText":"","formattedText":""},"esES":{"extends":"StudioObject","objectType":"Unit","oid":"","plainText":"","formattedText":""}}}]},{"extents":"StudioObject","objectType":"GridTextLine","gridTextList":[{"extents":"SurveyItem","objectType":"GridText","templateID":"TTT1c","customID":"TTT1c","dataType":"String","label":{"ptBR":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"GridText line2, column1 input","formattedText":"gridText line2, column1 input"},"enUS":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"","formattedText":""},"esES":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"","formattedText":""}},"layout":{"extents":"StudioObject","objectType":"LayoutGrid","width":100},"unit":{"ptBR":{"extends":"StudioObject","objectType":"Unit","oid":"","plainText":"","formattedText":""},"enUS":{"extends":"StudioObject","objectType":"Unit","oid":"","plainText":"","formattedText":""},"esES":{"extends":"StudioObject","objectType":"Unit","oid":"","plainText":"","formattedText":""}}},{"extents":"SurveyItem","objectType":"GridText","templateID":"TTT1d","customID":"TTT1d","dataType":"String","label":{"ptBR":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"GridText line2, column2 input","formattedText":"GridText line2, column2 input"},"enUS":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"","formattedText":""},"esES":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"","formattedText":""}},"layout":{"extents":"StudioObject","objectType":"LayoutGrid","width":100},"unit":{"ptBR":{"extends":"StudioObject","objectType":"Unit","oid":"","plainText":"","formattedText":""},"enUS":{"extends":"StudioObject","objectType":"Unit","oid":"","plainText":"","formattedText":""},"esES":{"extends":"StudioObject","objectType":"Unit","oid":"","plainText":"","formattedText":""}}}]}]}***
            
            Your task is to generate this json object based on user input"""
        },
        {
            "role":"user",
            "content":f"Generate a GridTextQuestion with{userInput}. Do it step by step as specified by the system structure. Return it as a raw JSON, without spaces."
        }
    ],
    response_format={"type": "json_object"}
)

print(completion.choices[0].message.content)
gridText = json.loads(completion.choices[0].message.content)

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

form.update({"itemContainer":[gridText]})

currentTime = getTime()
with open(f"GridText_{currentTime}.json", "w") as outfile: #saves json to a file
    json.dump(form, outfile)