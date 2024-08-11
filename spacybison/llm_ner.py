import asyncio
import json
from spacy_llm.util import assemble

def llm_ner(input_text):
    nlp = assemble("spacybison/config.cfg")
    doc = nlp(input_text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]

    return entities