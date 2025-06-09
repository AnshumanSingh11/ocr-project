
from indictrans import Translator

translator = Translator(source='hi', target='en')

def translate_hi_to_en(text):
    return translator.translate(text)
