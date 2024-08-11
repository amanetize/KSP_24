import json
null = None

def selected_entities(json_data, entity_types):
    selected = [entry for entry in json_data if entry.get("entity_type") in entity_types]

    return selected