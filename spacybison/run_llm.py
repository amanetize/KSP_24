from spacybison.occurences import find_all_occurrences
from spacybison.llm_ner import llm_ner
import json

def run_llm(input_text):
    extracted_list = llm_ner(input_text)

    output = []
    seen_occurrences = set()

    for entity, entity_type in extracted_list:
        occurrences = list(find_all_occurrences(input_text, entity))
        for start, end in occurrences:
            if (start, end) not in seen_occurrences:
                seen_occurrences.add((start, end))
                output.append({
                    "entity_type": entity_type,
                    "start": start,
                    "end": end,
                    "score": 1,
                    "analysis_explanation": None,
                    "recognition_metadata": {
                        "recognizer_identifier": "spacy-llm",
                        "recognizer_name": "chat-bison-001"
                    }
                })
    return output