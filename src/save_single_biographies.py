"""
This script reads the translated biographies from the joined YAML files
and saves each biography to a separate YAML file in the "data/single_biographies" directory.
The file names are formatted as "Letter-biography-index_translated.yaml".

Functions:
----------
save_individual_biographies(letters: List[str]) -> None
    Reads the translated biographies from the joined YAML files and saves each
    biography to a separate YAML file in the "data/single_biographies" directory.

Usage:
------
1. Make sure the translated YAML files exist in the "data/joined" directory
   with the naming format "Letter-names_translated.yaml".

2. Update the 'letters' list variable in the __main__ block with the
   appropriate list of letters, including special characters and combined letters.

3. Run this script after running the `process_all_yaml_files()` function
   in the previous script.
"""


import os
import re

def save_individual_biographies(letters):
    for letter in letters:
        input_file = os.path.join("data", "joined", f"{letter}-names_clean.yaml")

        if os.path.exists(input_file):
            with open(input_file, "r", encoding="utf-8") as file:
                yaml_text = file.read()

            # Split biographies
            biographies = re.split(r'(?<=\n\n)[\s]*(?=[^\n]+)', yaml_text, flags=re.MULTILINE)

            for index, biography in enumerate(biographies):
                output_file = os.path.join("data", "single_biographies", f"{letter}-biography-{index}_clean.yaml")
                with open(output_file, "w", encoding="utf-8") as file:
                    file.write(biography)

if __name__ == "__main__":
    letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZÅÄ") + ["V & W"]
    save_individual_biographies(letters)
