import spacy
import re

# Load the NLP model
nlp = spacy.load("en_core_web_sm")

def extract_ingredients(text):
    wants = []
    dont_wants = []
    want_patterns = r"(want|include)([^don't，。]+)"
    dont_want_patterns = r"don't want([^，。]+)"
    
    for match in re.finditer(want_patterns, text):
        phrase = match.group(2).strip()
        sub_doc = nlp(phrase)
        for ent in sub_doc.ents:
            if ent.label_ in ["FOOD", "ORG"]:
                wants.append(ent.text)

    for match in re.finditer(dont_want_patterns, text):
        phrase = match.group(1).strip()
        sub_doc = nlp(phrase)
        for ent in sub_doc.ents:
            if ent.label_ in ["FOOD", "ORG"]:
                dont_wants.append(ent.text)

    return wants, dont_wants
