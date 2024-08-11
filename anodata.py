import json

class RecognizerResult:
    def __init__(self, entity_type, start, end, score):
        self.entity_type = entity_type
        self.start = start
        self.end = end
        self.score = score

    def __repr__(self):
        return f'RecognizerResult(entity_type="{self.entity_type}", start={self.start}, end={self.end}, score={self.score})'

def anodata(json_data):
    data = json_data
    results = []
    
    for item in data:
        result = RecognizerResult(
            entity_type=item["entity_type"],
            start=item["start"],
            end=item["end"],
            score=item["score"]
        )
        results.append(result)
    return results