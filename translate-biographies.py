"""
Translate text from Swedish to English using OpenAI API

"""

import openai
import yaml

with open("config.yml", "r") as f:
    config = yaml.safe_load(f)

openai.api_key = config["default"]["key"]

## Translate text from Swedish to English using OpenAI API

translate_prompt = "Translate the following historical biography into English. It includes many Swedish abbreviations:"

def translate_biography(text):
    print(f"Translating {text[:100]}\n")
    translation = None

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert on Swedish family history."},
                {"role": "user", "content": f"{translate_prompt}\n\n{text}\n"}
            ]
        )
    except openai.OpenAIError as e:
        print(f"Error while creating translation: {e}")
    else:
        if response and response.choices and response.choices[0].message:
            translation = response.choices[0].message.content
        else:
            print("Error: No translation was returned.")

    return translation

