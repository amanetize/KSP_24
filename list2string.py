def convert_list_to_string(text_list):
    combined_string = ' '.join(text_list)
    cleaned_string = ' '.join(combined_string.split())
    return cleaned_string