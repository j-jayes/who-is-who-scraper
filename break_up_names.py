import re
import glob
import yaml

def load_yaml_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def get_surname_pattern(page_number, toc_data):
    for letter, page_range in toc_data.items():
        if page_number >= page_range[0] and page_number <= page_range[1]:
            if letter == "V & W":
                return r"^([VW][a-zåäöé]+)"
            else:
                return fr"^([{letter}][a-zåäöé]+)"
    return r"^([A-Z][a-zåäöé]+)"

def read_page_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.readlines()

def save_biography(file_name, bio_text):
    with open(file_name, "w", encoding="utf-8") as f:
        f.write(bio_text)

def process_files():
    file_paths = sorted(glob.glob("page_text_*.txt"))
    prev_bio = ""
    bio_counter = 1
    toc_data = load_yaml_file("toc-stockholm.yaml")

    for idx, file_path in enumerate(file_paths):
        page_number = idx + 1
        surname_pattern = get_surname_pattern(page_number, toc_data)
        pattern = re.compile(f"{surname_pattern}, [A-Z][a-zåäöé]+")

        lines = read_page_file(file_path)

        for line in lines:
            if pattern.match(line):
                if prev_bio:
                    save_biography(f"biography_{bio_counter}.txt", prev_bio)
                    bio_counter += 1
                prev_bio = line
            else:
                prev_bio += line

        # Save the last biography on the last page
        if idx == len(file_paths) - 1:
            save_biography(f"biography_{bio_counter}.txt", prev_bio)

if __name__ == "__main__":
    process_files()
