import os
import json
from datetime import datetime
from openai import OpenAI
from dotenv import load_dotenv
from time import sleep


def getTime():
    currentTime = str(datetime.now())
    currentTime = currentTime.replace(' ', 'T')
    currentTime = currentTime.replace(':', '_')
    currentTime = currentTime[:19]
    return currentTime

def generate_navigation_structure(num_elements=int, acID='TML'):
    # Define the list for storing the navigation elements
    navigation_list = []

    # Add the BEGIN NODE
    begin_node = {
        "extents": "SurveyTemplateObject",
        "objectType": "Navigation",
        "origin": "BEGIN NODE",
        "index": 0,
        "inNavigations": [],
        "routes": [{"extents": "SurveyTemplateObject",
                    "objectType": "Route",
                    "origin": "BEGIN NODE",
                    "destination": f"{acID}1",
                    "name": f"BEGIN NODE_{acID}1",
                    "isDefault": True,
                    "conditions": []}]
    }
    navigation_list.append(begin_node)

    # Add the END NODE with placeholder for inNavigations, to fill after adding intermediate nodes
    end_node = {
        "extents": "SurveyTemplateObject",
        "objectType": "Navigation",
        "origin": "END NODE",
        "index": 1,
        "inNavigations": [None] * 2,  # Placeholder for inNavigations
        "routes": []
    }
    navigation_list.append(end_node)

    # Add intermediate acID nodes
    for i in range(num_elements):
        origin = f"{acID}{i + 1}"
        # Destination acID or END NODE
        destination = f"{acID}{i + 2}" if i + 1 < num_elements else "END NODE"

        # Create acID node
        acID_node = {
            "extents": "SurveyTemplateObject",
            "objectType": "Navigation",
            "origin": origin,
            "index": i + 2,
            "inNavigations": [{"origin": f"BEGIN NODE" if i == 0 else f"{acID}{i}", "index": i + 1}],
            "routes": [{"extents": "SurveyTemplateObject",
                        "objectType": "Route",
                        "origin": origin,
                        "destination": destination,
                        "name": f"{origin}_{destination}",
                        "isDefault": True,
                        "conditions": []}]
        }
        navigation_list.append(acID_node)

    # Fill inNavigations for END NODE to point to the last acID node
    if num_elements > 0:
        end_node["inNavigations"] = [None, {"origin": f"{acID}{num_elements}", "index": 1 + num_elements + 1}]

    return {"navigationList": navigation_list}

def generateJSON(userInput=str, acID='TML', name='formulario', modelo='gpt-4o'):
    totalTokens = 0
    load_dotenv() #load enviroment variables
    API_KEY = os.getenv('OPENROUTER_API_KEY') #api key here
    form = {
        "extents": "StudioObject",
        "objectType": "Survey",
        "oid": "dXNlclVVSUQ6W3VuZGVmaW5lZF1zdXJ2ZXlVVUlEOltkMzllZTg5MC05MDhkLTExZWYtOWZmYS1jOTM3YmMwNTQ1ODddcmVwb3NpdG9yeVVVSUQ6WyBOb3QgZG9uZSB5ZXQgXQ==",
        "identity": {
            "extents": "StudioObject",
            "objectType": "SurveyIdentity",
            "name": name,
            "acronym": acID,
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
        "navigationList": [],
        "staticVariableList": [],
        "surveyItemGroupList": []
    }

    #print("Generating items...")

    client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=API_KEY)
    itensCompletion = client.chat.completions.create(
        model=modelo,
        messages=[
            {
                "role":"system",
                "content": """You are a helpful AI assistant capable of generating JSONs based on user input. These JSONs are responsible for creating forms in an external appication. Your task is to generate and add JSONs objects to a list inside ***itemContainer*** field in the following JSON: ***{"itemContainer":[]}***. The following are JSON itens options to be added to the list as specified by user input. Fill the correct properties inside the JSON structure with user input:

                ***SingleSelectionQuestion:{"extents":"SurveyItem","objectType":"SingleSelectionQuestion","templateID":"TML1","customID":"TML1","dataType":"Integer","label":{"ptBR":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"SingleSelectionQuestion input","formattedText":"SingleSelectionQuestion input"},"enUS":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"","formattedText":""},"esES":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"","formattedText":""}},"options":[{"extents":"StudioObject","objectType":"AnswerOption","value":1,"extractionValue":1,"imageUrl":null,"imageTitle":false,"dataType":"Integer","label":{"ptBR":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"option 1 input","formattedText":"option 1 input"},"enUS":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"","formattedText":""},"esES":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"","formattedText":""}}},{"extents":"StudioObject","objectType":"AnswerOption","value":2,"extractionValue":2,"imageUrl":null,"imageTitle":false,"dataType":"Integer","label":{"ptBR":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"option 2 input","formattedText":"option 2 input"},"enUS":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"","formattedText":""},"esES":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"","formattedText":""}}},{"extents":"StudioObject","objectType":"AnswerOption","value":3,"extractionValue":3,"imageUrl":null,"imageTitle":false,"dataType":"Integer","label":{"ptBR":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"option 3 input","formattedText":"option 3 input"},"enUS":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"","formattedText":""},"esES":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"","formattedText":""}}}],"metadata":{"extents":"StudioObject","objectType":"MetadataGroup","options":[]},"fillingRules":{"extends":"StudioObject","objectType":"FillingRules","options":{"mandatory":{"extends":"StudioObject","objectType":"Rule","validatorType":"mandatory","data":{"canBeIgnored":false,"reference":true}}}},"imageUrl":null  }***

                ***CheckboxQuestion:{"extents":"SurveyItem","objectType":"CheckboxQuestion","templateID":"TML2","customID":"TML2","dataType":"Array","label":{"ptBR":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"CheckboxQuestion input","formattedText":"CheckboxQuestion input"},"enUS":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"","formattedText":""},"esES":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"","formattedText":""}},"options":[{"extents":"StudioObject","objectType":"CheckboxAnswerOption","optionID":"TML2a","customOptionID":"TML2a","dataType":"Boolean","value":false,"label":{"ptBR":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"option 1 input","formattedText":"option 1 input"},"enUS":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"","formattedText":""},"esES":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"","formattedText":""}}},{"extents":"StudioObject","objectType":"CheckboxAnswerOption","optionID":"TML2b","customOptionID":"TML2b","dataType":"Boolean","value":false,"label":{"ptBR":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"option 2 input","formattedText":"option 2 input"},"enUS":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"","formattedText":""},"esES":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"","formattedText":""}}},{"extents":"StudioObject","objectType":"CheckboxAnswerOption","optionID":"TML2c","customOptionID":"TML2c","dataType":"Boolean","value":false,"label":{"ptBR":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"option 3 input","formattedText":"option 3 input"},"enUS":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"","formattedText":""},"esES":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"","formattedText":""}}}],"metadata":{"extents":"StudioObject","objectType":"MetadataGroup","options":[]},"fillingRules":{"extends":"StudioObject","objectType":"FillingRules","options":{"mandatory":{"extends":"StudioObject","objectType":"Rule","validatorType":"mandatory","data":{"canBeIgnored":false,"reference":true}}}}  }***

                ***CalendarQuestion:{"extents":"SurveyItem","objectType":"CalendarQuestion","templateID":"TML3","customID":"TML3","dataType":"LocalDate","label":{"ptBR":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"CalendarQuestion input","formattedText":"CalendarQuestion input"},"enUS":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"","formattedText":""},"esES":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"","formattedText":""}},"metadata":{"extents":"StudioObject","objectType":"MetadataGroup","options":[]},"fillingRules":{"extends":"StudioObject","objectType":"FillingRules","options":{"mandatory":{"extends":"StudioObject","objectType":"Rule","validatorType":"mandatory","data":{"canBeIgnored":false,"reference":true}}}}  }***

                ***IntegerQuestion:{"extents":"SurveyItem","objectType":"IntegerQuestion","templateID":"TML4","customID":"TML4","dataType":"Integer","label":{"ptBR":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"IntegerQuestion input","formattedText":"IntegerQuestion input"},"enUS":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"","formattedText":""},"esES":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"","formattedText":""}},"metadata":{"extents":"StudioObject","objectType":"MetadataGroup","options":[]},"unit":{"ptBR":{"extends":"StudioObject","objectType":"Unit","oid":"","plainText":"","formattedText":""},"enUS":{"extends":"StudioObject","objectType":"Unit","oid":"","plainText":"","formattedText":""},"esES":{"extends":"StudioObject","objectType":"Unit","oid":"","plainText":"","formattedText":""}},"fillingRules":{"extends":"StudioObject","objectType":"FillingRules","options":{"mandatory":{"extends":"StudioObject","objectType":"Rule","validatorType":"mandatory","data":{"canBeIgnored":false,"reference":true}}}}  }***

                ***DecimalQuestion:{"extents":"SurveyItem","objectType":"DecimalQuestion","templateID":"TML5","customID":"TML5","dataType":"Decimal","label":{"ptBR":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"DecimalQuestion input","formattedText":"DecimalQuestion input"},"enUS":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"","formattedText":""},"esES":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"","formattedText":""}},"metadata":{"extents":"StudioObject","objectType":"MetadataGroup","options":[]},"unit":{"ptBR":{"extends":"StudioObject","objectType":"Unit","oid":"","plainText":"","formattedText":""},"enUS":{"extends":"StudioObject","objectType":"Unit","oid":"","plainText":"","formattedText":""},"esES":{"extends":"StudioObject","objectType":"Unit","oid":"","plainText":"","formattedText":""}},"fillingRules":{"extends":"StudioObject","objectType":"FillingRules","options":{"mandatory":{"extends":"StudioObject","objectType":"Rule","validatorType":"mandatory","data":{"canBeIgnored":false,"reference":true}}}}}***

                ***TextQuestion:{"extents":"SurveyItem","objectType":"TextQuestion","templateID":"TML6","customID":"TML6","dataType":"String","label":{"ptBR":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"TextQuestion input","formattedText":"TextQuestion input"},"enUS":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"","formattedText":""},"esES":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"","formattedText":""}},"metadata":{"extents":"StudioObject","objectType":"MetadataGroup","options":[]},"fillingRules":{"extends":"StudioObject","objectType":"FillingRules","options":{"mandatory":{"extends":"StudioObject","objectType":"Rule","validatorType":"mandatory","data":{"canBeIgnored":false,"reference":true}}}}  }***

                ***EmailQuestion:{"extents":"SurveyItem","objectType":"EmailQuestion","templateID":"TML7","customID":"TML7","dataType":"String","label":{"ptBR":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"EmailQuestion input","formattedText":"EmailQuestion input"},"enUS":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"","formattedText":""},"esES":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"","formattedText":""}},"metadata":{"extents":"StudioObject","objectType":"MetadataGroup","options":[]},"fillingRules":{"extends":"StudioObject","objectType":"FillingRules","options":{"mandatory":{"extends":"StudioObject","objectType":"Rule","validatorType":"mandatory","data":{"canBeIgnored":false,"reference":true}}}}  }***

                ***TimeQuestion:{"extents":"SurveyItem","objectType":"TimeQuestion","templateID":"TML8","customID":"TML8","dataType":"LocalTime","label":{"ptBR":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"TimeQuestion input","formattedText":"TimeQuestion input"},"enUS":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"","formattedText":""},"esES":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"","formattedText":""}},"metadata":{"extents":"StudioObject","objectType":"MetadataGroup","options":[]},"fillingRules":{"extends":"StudioObject","objectType":"FillingRules","options":{"mandatory":{"extends":"StudioObject","objectType":"Rule","validatorType":"mandatory","data":{"canBeIgnored":false,"reference":true}}}},"options":{"extends":"StudioObject","objectType":"QuestionOption","data":{}}  }***

                ***PhoneQuestion:{"extents":"SurveyItem","objectType":"PhoneQuestion","templateID":"TML9","customID":"TML9","dataType":"Integer","label":{"ptBR":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"PhoneQuestion input","formattedText":"PhoneQuestion input"},"enUS":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"","formattedText":""},"esES":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"","formattedText":""}},"metadata":{"extents":"StudioObject","objectType":"MetadataGroup","options":[]},"fillingRules":{"extends":"StudioObject","objectType":"FillingRules","options":{"mandatory":{"extends":"StudioObject","objectType":"Rule","validatorType":"mandatory","data":{"canBeIgnored":false,"reference":true}}}}  }***

                ***TextItem:{"extents":"SurveyItem","objectType":"TextItem","templateID":"TML10","customID":"TML10","dataType":"String","value":{"ptBR":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"TextItem input","formattedText":"TextItem input"},"enUS":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"","formattedText":""},"esES":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"","formattedText":""}}  }***

                ***AutocompleteQuestion: {"extents":"SurveyItem","objectType":"AutocompleteQuestion","templateID":"TML11","customID":"TML11","dataType":"String","dataSources":[],"label":{"ptBR":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"AutocompleteQuestion input","formattedText":"AutocompleteQuestion input"},"enUS":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"","formattedText":""},"esES":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"","formattedText":""}},"metadata":{"extents":"StudioObject","objectType":"MetadataGroup","options":[]},"fillingRules":{"extends":"StudioObject","objectType":"FillingRules","options":{"mandatory":{"extends":"StudioObject","objectType":"Rule","validatorType":"mandatory","data":{"canBeIgnored":false,"reference":true}}}}}***

                ***FileUploadQuestion: {"extents":"SurveyItem","objectType":"FileUploadQuestion","templateID":"TML12","customID":"TML12","dataType":"Binary","label":{"ptBR":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"FileUploadQuestion input","formattedText":"FileUploadQuestion input"},"enUS":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"","formattedText":""},"esES":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"","formattedText":""}},"metadata":{"extents":"StudioObject","objectType":"MetadataGroup","options":[]},"fillingRules":{"extends":"StudioObject","objectType":"FillingRules","options":{"mandatory":{"extends":"StudioObject","objectType":"Rule","validatorType":"mandatory","data":{"canBeIgnored":false,"reference":true}}}}}***

                ***ImageItem: {"extents":"SurveyItem","objectType":"ImageItem","templateID":"TML13","customID":"TML13","dataType":"String","url":"","footer":{"ptBR":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"","formattedText":""},"enUS":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"","formattedText":""},"esES":{"extends":"StudioObject","objectType":"Label","oid":"","plainText":"","formattedText":""}}}***
                """
            },
            {
                "role":"user",
                "content":f"Generate a JSON with {userInput}. Do it step by step as specified by the system structure. Return it as a raw JSON, without spaces."
            }
        ],
        response_format={"type": "json_object"}
    )

    totalTokens += itensCompletion.usage.total_tokens

    if model == 'google/gemini-2.0-flash-001':
        experiment = 'sample_MO_Gemini20Flash'
    elif model == 'gpt-4o':
        experiment = 'sample_MO_GPT4o'
    elif model == 'openai/gpt-4o-mini':
        experiment = 'sample_MO_GPT4oMini'
    elif model == 'google/gemini-2.0-flash-lite-001':
        experiment = 'sample_MO_Gemini20FlashLite'
    elif model == 'google/gemini-2.5-flash-lite':   
        experiment = 'sample_MO_Gemini25FlashLite'
    elif model == 'google/gemini-2.5-flash':
        experiment = 'sample_MO_Gemini25Flash'
    elif model == 'google/gemini-2.5-pro':
        experiment = 'sample_MO_Gemini25Pro'
    else:
        experiment = 'sample_MO_OpenRouter'
    
    completition = itensCompletion.choices[0].message.content

    try:
        itemCont = json.loads(itensCompletion.choices[0].message.content) #loads generated itemContainer field json to variable
    except json.JSONDecodeError as e:
        print(f'Error decoding JSON: {e}')
        
        with open(f'error_log_json_{experiment}_{getTime()}.txt', 'a') as error_file:
            error_file.write(f'{getTime()} - Error decoding JSON: {e}\n')
        
        with open(f'raw_response_{experiment}_{getTime()}.txt', 'w') as raw_file:
            raw_file.write(completition)
        return None

    form['itemContainer'] = itemCont['itemContainer'] #adds generated json to dictionary field

    numOfItens = len(form['itemContainer'])

    #print('Generating navigation...')

    navigationList = generate_navigation_structure(numOfItens)

    form['navigationList'] = navigationList['navigationList']

    #print('Adjusting indexes...')

    acronym = form['identity']['acronym']
    numOfItens = len(form['itemContainer'])
    alphaArray = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    for i in range(0, numOfItens):
        form['itemContainer'][i]['templateID'] = f'{acronym}{i+1}'
        form['itemContainer'][i]['customID'] = f'{acronym}{i+1}'

        if form['itemContainer'][i]['objectType'] == 'CheckboxQuestion':
            currentIndex = form['itemContainer'][i]['templateID']
            for j in range(0, len(form['itemContainer'][i]['options'])):
                form['itemContainer'][i]['options'][j]['optionID'] = f'{acronym}{i+1}{alphaArray[j]}'
                form['itemContainer'][i]['options'][j]['customOptionID'] = f'{acronym}{i+1}{alphaArray[j]}'
        
    return form

    #print(f'Finished with {totalTokens} used tokens')

if __name__ == "__main__":
    #listaModelos = ['google/gemini-2.0-flash-001', 'gpt-4o', 'openai/gpt-4o-mini','google/gemini-2.5-flash-lite' ,'google/gemini-2.5-flash', 'google/gemini-2.5-pro' ]
    #listaModelos = ['gpt-4o'] #uncomment to test only one model
    listaModelos = ['google/gemini-2.5-pro']

    prompt = 'prompt1.txt'

    with open (f'{os.path.dirname(os.path.abspath(__file__))}/{prompt}', 'r') as file:
        userForm = file.read()


    #model = listaModelos[5] #choose the model to be used in generation, changing the index will change the model

    for model in listaModelos:
        if model == 'google/gemini-2.0-flash-001':
            experiment = 'sample_MO_Gemini20Flash'
        elif model == 'gpt-4o':
            experiment = 'sample_MO_GPT4o'
        elif model == 'openai/gpt-4o-mini':
            experiment = 'sample_MO_GPT4oMini'
        elif model == 'google/gemini-2.0-flash-lite-001':
            experiment = 'sample_MO_Gemini20FlashLite'
        elif model == 'google/gemini-2.5-flash-lite':   
            experiment = 'sample_MO_Gemini25FlashLite'
        elif model == 'google/gemini-2.5-flash':
            experiment = 'sample_MO_Gemini25Flash'
        elif model == 'google/gemini-2.5-pro':
            experiment = 'sample_MO_Gemini25Pro'
        else:
            experiment = 'sample_MO_OpenRouter'
        for i in range(10): #number of forms to be generated
            try:
                print(f'Tentativa formulário {i+1}...')
                generatedForm = generateJSON(userForm, modelo=model)
                
                #saving sample to my computer
                mydirectory = os.path.dirname(os.path.abspath(__file__))
                mydirectory = mydirectory.replace('experimentos', 'samples')
                if not os.path.exists(mydirectory):
                    os.makedirs(mydirectory)

                if os.name == 'nt': #windows
                    with open(f'{mydirectory}\\{experiment}_{getTime()}.json', 'w') as outfile:
                        json.dump(generatedForm, outfile)
                else: #linux or others
                    with open(f'{mydirectory}/{experiment}_{getTime()}.json', 'w') as outfile:
                        json.dump(generatedForm, outfile) 

            except Exception as e:
                print(f'Error generating form {i+1}: {e}')
                with open(f'error_log_{experiment}_{getTime()}.txt', 'a') as error_file:
                    error_file.write(f'{getTime()} - Error generating form {i+1}: {e}\n')
                pass
        
            #sleep(15) #sleep to avoid hitting rate limits
