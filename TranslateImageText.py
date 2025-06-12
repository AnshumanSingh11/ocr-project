from PIL import Image
import pytesseract
import os
import subprocess
from googletrans import Translator
from SaveToMySQL import save_translation  # <- MySQL Integration

class Translation:
    def __init__(self, extract_img, extract_file, translate_file, pytesseract_image_language, from_language, to_language):
        self.extract_img = extract_img
        self.extract_file = extract_file
        self.translate_file = translate_file
        self.pytesseract_image_language = pytesseract_image_language
        self.from_language = from_language
        self.to_language = to_language

    def extract_image_text(self):
        img = Image.open(self.extract_img)
        text = pytesseract.image_to_string(img, lang=self.pytesseract_image_language)
        text = text.replace('.', '.\n').replace('!', '!\n').replace('?', '?\n')
        return text

    def translate_image_text(self, text):
        translator = Translator()
        translation = translator.translate(text, src=self.from_language, dest=self.to_language).text
        return translation

    def write_image_text(self, text):
        with open(self.extract_file, 'w', encoding='utf-8') as f:
            f.write(text)

    def write_translation(self):
        with open(self.extract_file, 'r', encoding='utf-8') as f1, open(self.translate_file, 'w', encoding='utf-8') as f2:
            for i, line in enumerate(f1, 1):
                line = line.strip()
                if line:
                    translated_line = self.translate_image_text(line)
                    f2.write(f"{i}) {line}\n")
                    f2.write(f"{i}) {translated_line}\n\n")
                    # Save to MySQL database
                    save_translation(line, translated_line, self.from_language, self.to_language, self.extract_img)

    def remove_extract_file(self):
        if os.path.exists(self.extract_file):
            os.remove(self.extract_file)

    def view_translation(self):
        subprocess.Popen(['notepad', self.translate_file])  # Use Notepad if Sublime not installed

if __name__ == "__main__":
    mypath = os.path.dirname(os.path.abspath(__file__))

    for f in os.listdir(mypath):
        if f.endswith(".png"):  # You can extend to .pdf later
            extract_img = f
            extract_file = f"{os.path.splitext(f)[0]}_extracted.txt"
            translate_file = f"translated_{os.path.splitext(f)[0]}.txt"
            pytesseract_image_language = 'hin'  # or 'eng', 'fra', etc.
            from_language = 'hi'               # Hindi
            to_language = 'en'                 # English

            t = Translation(extract_img, extract_file, translate_file, pytesseract_image_language, from_language, to_language)
            raw_text = t.extract_image_text()
            t.write_image_text(raw_text)
            t.write_translation()
            t.remove_extract_file()
            # t.view_translation()
            print(f"[DONE] Processed: {f}")