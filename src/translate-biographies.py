import os
import openai
import json
import yaml
from pathlib import Path

root_dir = 'C:/Users/User/Documents/Recon/who-is-who-scraper'

# Reference the 'data' directory from the root
data_dir = Path(root_dir) / "data"

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

openai.api_key = config["default"]["key"]

def translate_and_structure_text(swedish_text):
    try:
        # Translate the Swedish text to English
        translate_prompt = f"Translate the following abbreviated Swedish biography to English: {swedish_text}. Note that '\\d\\d m. partners name' means that the person married in the year 19xx."
        translation_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert on Swedish family history."},
                {"role": "user", "content": f"{translate_prompt}"}
            ]
        )

        english_text = translation_response.choices[0].message.content

        structure_prompt = f"Given the original Swedish biography: {swedish_text}\nAnd its English translation: {english_text}\n"\
                           "Structure the biography in Schema.org/Person format as a JSON object. Include dates wherever possible. Only provide a  RFC8259 compliant JSON response."

        structure_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                    {"role": "system", "content": "You are an expert on Swedish family history and the Schema.org/Person format."},
                    {"role": "user", "content": f"{structure_prompt}"}
            ]
        )

        structured_biography_raw = structure_response.choices[0].message.content

        structured_biography = json.loads(structure_response.choices[0].message.content)

        print(f"Translated text: {english_text}")

        return english_text, structured_biography, structured_biography_raw

    except Exception as e:
        print(f"Error in translate_and_structure_text: {e}")
        return None, None


def main():
    input_directory = Path(data_dir) / "biographies"
    output_directory = Path(data_dir) / "biographies_translated"
    os.makedirs(output_directory, exist_ok=True)

    # Get the list of all .txt files in the input directory
    all_files = sorted([f for f in os.listdir(input_directory) if f.endswith(".txt")])

    # Process only the first 10 files
    for file_name in all_files[600:3000]:
        file_path = os.path.join(input_directory, file_name)

        try:
            # Read the original Swedish biography
            with open(file_path, "r", encoding="utf-8") as file:
                original_biography = file.read()

            # Translate the biography to English and structure it
            translated_biography, structured_biography, structured_biography_raw = translate_and_structure_text(original_biography)

            if translated_biography is not None and structured_biography is not None:
                # Prepare JSON data
                data = {
                    "original": original_biography,
                    "translated": translated_biography,
                    "structured_raw": structured_biography_raw,
                    "structured": structured_biography,
                }

                # Save the JSON data to the output directory
                output_file_name = os.path.basename(file_path).replace(".txt", ".json")
                output_file_path = os.path.join(output_directory, output_file_name)

                with open(output_file_path, "w", encoding="utf-8") as output_file:
                    json.dump(data, output_file, ensure_ascii=False, indent=4)

                print(f"Processed file: {file_name}")
            else:
                print(f"Error processing file {file_name}: translation or structuring failed. Check the API response for more information.")

        except Exception as e:
            print(f"Error processing file {file_name}: {e}")

if __name__ == "__main__":
    main()
