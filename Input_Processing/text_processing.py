from langdetect import detect
from transformers import MarianMTModel, MarianTokenizer
import spacy
import re
from functools import lru_cache

class TextProcessor:
    def __init__(self):
        """Load the English NLP model"""
        self.nlp = spacy.load("en_core_web_sm")

    @lru_cache(maxsize=100)
    def translate_text(self, text, target_lang='en'):
        """Translates text to English using Helsinki NLP models from detected language."""
        detected_lang = detect(text)
        if detected_lang == target_lang:
            return text
        model_name = f"Helsinki-NLP/opus-mt-{detected_lang}-en"
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name)
        inputs = tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
        translated = model.generate(**inputs)
        translated_text = tokenizer.decode(translated[0], skip_special_tokens=True)
        return translated_text

    def extract_ingredients(self, text):
        """Extracts ingredients that the user wants and doesn't want based on patterns in the text."""
        doc = self.nlp(text)
        wants = []
        dont_wants = []
        want_patterns = r"\b(want|include|desire|would like)\b(.+?);"
        dont_want_patterns = r"\b(don't want|exclude|without)\b(.+?);"
        for match in re.finditer(want_patterns, text, re.IGNORECASE):
            phrase = match.group(2).strip()
            sub_doc = self.nlp(phrase)
            for ent in sub_doc.ents:
                if ent.label_ == "FOOD":
                    wants.append(ent.text)
        for match in re.finditer(dont_want_patterns, text, re.IGNORECASE):
            phrase = match.group(2).strip()
            sub_doc = self.nlp(phrase)
            for ent in sub_doc.ents:
                if ent.label_ == "FOOD":
                    dont_wants.append(ent.text)
        return wants, dont_wants

    def process_text(self, text):
        """Processes text by translating it to English, then extracting ingredient preferences."""
        translated_text = self.translate_text(text)
        wants, dont_wants = self.extract_ingredients(translated_text)
        return {"wants": wants, "dont_wants": dont_wants}
if __name__ == '__main__':
    app.run(debug=True, port=5000)
