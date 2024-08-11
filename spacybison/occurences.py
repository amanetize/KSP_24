def find_all_occurrences(text, substring):
    start = 0
    while start < len(text):
        start = text.find(substring, start)
        if start == -1: 
            break
        yield start, start + len(substring)
        start += len(substring)