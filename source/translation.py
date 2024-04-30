import json
from googletrans import Translator, LANGUAGES

def translate_text(text, dest='en'):
    translator = Translator()
    translation = translator.translate(text, dest=dest)
    return translation.text

def process_json(file_path, output_path):
    # Load the JSON data from the file
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    # Translate and update the values
    translated_data = {}
    for key, value in data.items():
        # Translate the value
        translated_value = translate_text(value)
        # Concatenate the original Chinese value with the translated value
        translated_data[key] = f"{value}\n{translated_value}"

    # Save the updated data to a new JSON file
    with open(output_path, 'w', encoding='utf-8') as file:
        json.dump(translated_data, file, ensure_ascii=False, indent=4)

# Example usage
process_json('world.json', 'world_en.json')
