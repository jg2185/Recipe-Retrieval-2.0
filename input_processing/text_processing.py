from googletrans import Translator

class TextProcessor:
    def __init__(self):
        self.translator = Translator()

    def translate_text(self, text, dest='en'):
        """Translates text to the specified language using Google Translate."""
        translation = self.translator.translate(text, dest=dest)
        return translation.text

    def process_ingredients(self, wants_list, dont_wants_list):
        """Processes lists of ingredient names, translating each to English if necessary."""
        wants_translated = [self.translate_text(want) for want in wants_list]
        dont_wants_translated = [self.translate_text(dont_want) for dont_want in dont_wants_list]
        return {"wants": wants_translated, "dont_wants": dont_wants_translated}

# Example of usage
# processor = TextProcessor()
# wants = ["蕃茄", "牛肉", "queso"]  # Example ingredients in different languages
# dont_wants = ["cebolla", "大蒜"]

# result = processor.process_ingredients(wants, dont_wants)
# print(result)
