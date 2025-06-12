import pytesseract
from PIL import Image
from argostranslate import package, translate
import os
from SaveToMySQL import save_translation  # Assuming this is in a separate file

class TranslateImageText:
    def __init__(self, image_path, from_language="hi", to_language="en"):
        self.extract_img = image_path
        self.from_language = from_language
        self.to_language = to_language

    def extract_image_text(self):
        try:
            img = Image.open(self.extract_img)
            text = pytesseract.image_to_string(img, lang='hin')  # for Hindi
            return text.strip()
        except Exception as e:
            print(f"Error reading image: {e}")
            return ""

    def translate_image_text(self, text):
        try:
            installed_languages = translate.get_installed_languages()
            from_lang = next((lang for lang in installed_languages if lang.code == self.from_language), None)
            to_lang = next((lang for lang in installed_languages if lang.code == self.to_language), None)
            
            if not from_lang or not to_lang:
                raise Exception("Translation language models not installed.")

            translation = from_lang.get_translation(to_lang)
            return translation.translate(text)
        except Exception as e:
            print(f"Translation error: {e}")
            return ""

    def write_translation(self):
        text = self.extract_image_text()
        if text:
            translated_text = self.translate_image_text(text)
            print("\nOriginal Text:", text)
            print("\nTranslated Text:", translated_text)

            # Save to MySQL
            save_translation(text, translated_text, self.from_language, self.to_language, self.extract_img)
        else:
            print("No text extracted from image.")

if __name__ == "__main__":
    image_path = "test_hindi.png"  # Replace with your actual image file path
    translator = TranslateImageText(image_path)
    translator.write_translation()
