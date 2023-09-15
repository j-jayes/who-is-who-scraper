import os
import json
import yaml
from pathlib import Path
import asyncio
import httpx

root_dir = 'C:/Users/User/Documents/Recon/who-is-who-scraper'
data_dir = Path(root_dir) / "data"

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

API_KEY = config["default"]["key"]
API_ENDPOINT = "https://api.openai.com/v1/engines/gpt-3.5-turbo/completions"
MAX_RETRIES = 3
RATE_LIMIT_DELAY = 0.5  # in seconds, adjust based on your OpenAI rate limit

async def translate_and_structure_text(swedish_text):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    async with httpx.AsyncClient() as client:
        for _ in range(MAX_RETRIES):
            try:
                # Rate limiting
                await asyncio.sleep(RATE_LIMIT_DELAY)

                # Translate
                translate_payload = {
                    "messages": [
                        {"role": "system", "content": "You are an expert on Swedish family history."},
                        {"role": "user", "content": f"Translate the following abbreviated Swedish biography to English: {swedish_text}. Note that '\\d\\d m. partners name' means that the person married in the year 19xx."}
                    ]
                }

                translate_response = await client.post(API_ENDPOINT, json=translate_payload, headers=headers)
                english_text = translate_response.json()["choices"][0]["message"]["content"]

                # Rate limiting
                await asyncio.sleep(RATE_LIMIT_DELAY)

                # Structure
                structure_payload = {
                    "messages": [
                        {"role": "system", "content": "You are an expert on Swedish family history and the Schema.org/Person format."},
                        {"role": "user", "content": f"Given the original Swedish biography: {swedish_text}\nAnd its English translation: {english_text}\nStructure the biography in Schema.org/Person format as a JSON object. Include dates wherever possible. Only provide a RFC8259 compliant JSON response."}
                    ]
                }

                structure_response = await client.post(API_ENDPOINT, json=structure_payload, headers=headers)
                structured_biography_raw = structure_response.json()["choices"][0]["message"]["content"]
                structured_biography = json.loads(structured_biography_raw)

                return english_text, structured_biography, structured_biography_raw

            except httpx.RequestError:
                continue

    print(f"Error: Maximum retries reached for text: {swedish_text}")
    return None, None, None

async def process_file(file_name, input_directory, output_directory):
    file_path = os.path.join(input_directory, file_name)
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            original_biography = file.read()

        translated_biography, structured_biography, structured_biography_raw = await translate_and_structure_text(original_biography)

        if translated_biography and structured_biography:
            data = {
                "original": original_biography,
                "translated": translated_biography,
                "structured_raw": structured_biography_raw,
                "structured": structured_biography,
            }

            output_file_name = os.path.basename(file_path).replace(".txt", ".json")
            output_file_path = os.path.join(output_directory, output_file_name)

            with open(output_file_path, "w", encoding="utf-8") as output_file:
                json.dump(data, output_file, ensure_ascii=False, indent=4)

            print(f"Processed file: {file_name}")

        else:
            print(f"Error processing file {file_name}: translation or structuring failed. Check the API response for more information.")

    except Exception as e:
        print(f"Error processing file {file_name}: {e}")

async def main():
    input_directory = Path(data_dir) / "biographies"
    output_directory = Path(data_dir) / "biographies_translated"
    os.makedirs(output_directory, exist_ok=True)

    all_files = sorted([f for f in os.listdir(input_directory) if f.endswith(".txt")])

    tasks = [process_file(file_name, input_directory, output_directory) for file_name in all_files[4001:4005]]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
