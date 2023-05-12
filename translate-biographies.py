import os
import openai
import json
import glob
import yaml

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

openai.api_key = config["default"]["key"]

def translate_and_structure_text(swedish_text):
    # Translate the Swedish text to English
    translate_prompt = f"Translate the following abbreviated Swedish biography to English: {swedish_text}"
    translation_response = openai.Completion.create(
        engine="gpt-3.5-turbo",
        prompt=translate_prompt,
        temperature=0.7,
        max_tokens=200,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    english_text = translation_response.choices[0].text.strip()

    # Structure the biography in Schema.org/Person format
    structure_prompt = f"Given the original Swedish biography: {swedish_text}\nAnd its English translation: {english_text}\n"\
                       "Structure the biography in Schema.org/Person format as a JSON object. Ensure the JSON is RFC 8259 compliant."
    structure_response = openai.Completion.create(
        engine="gpt-3.5-turbo",
        prompt=structure_prompt,
        temperature=0.7,
        max_tokens=200,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    structured_biography = json.loads(structure_response.choices[0].text.strip())

    return english_text, structured_biography


def main():
    input_directory = "data/biographies"
    output_directory = "data/biographies_translated"
    os.makedirs(output_directory, exist_ok=True)

    # Set the file path to the specified file
    file_path = os.path.join(input_directory, "gota48_1_biography_1.txt")

    # Read the original Swedish biography
    with open(file_path, "r", encoding="utf-8") as file:
        original_biography = file.read()

    # Translate the biography to English and structure it
    translated_biography, structured_biography = translate_and_structure_text(original_biography)

    # Prepare JSON data
    data = {
        "original": original_biography,
        "translated": translated_biography,
        "structured": structured_biography,
    }

    # Save the JSON data to the output directory
    output_file_name = os.path.basename(file_path).replace(".txt", ".json")
    output_file_path = os.path.join(output_directory, output_file_name)

    with open(output_file_path, "w", encoding="utf-8") as output_file:
        json.dump(data, output_file, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
