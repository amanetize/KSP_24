# KSP_24
Winning project made in Karnataka State Police Datathon 2024 for the challenge "Data Privacy in Law Enforcement."

## The Model

### Data Collection

- **Data Sources**: Extracted Addresses and Names from `FIR_Details_Data.csv`, `ChargesheetDetails.csv`, and `AccidentReports.csv`.
  
- **Custom Patterns**: Regex patterns for `FIR_No.`, `Crime_No.`, `Date_Time`, etc., can be found in `recognizers.yaml`.

- **Custom Trained SpaCy Pipelines**: Trained pipelines for addresses and person names are located in `custom-ner > ADDRESS` and `custom-ner > PERSON`.

### Analyzation

- **Model Loading**: Custom trained SpaCy models are loaded in `main.py` using `spacy.load()`.

- **Azure AI Language**: Integrated Azure AI Language using `Azure_AI_KEY` and `AZURE_AI_ENDPOINT`.

- **Presidio Analyzer**: Text analysis is performed using both trained SpaCy and Azure AI Language.

- **API Development**: Developed as an API using FastAPI. Endpoints include `@app.post('/text')` for text analysis and `@app.post("/i2t")` for image-to-text conversion.

### Higher Confidence

- **Conflict Resolution**: Handles conflicts or overlapping entities by considering the one with the highest score or larger word span. Refer to `overlapping.py`.

### Anonymization

- **User Input**: Allows users to select entities for anonymization and choose the type of anonymization.
  <img src="https://i.ibb.co/cYP0d4z/Screenshot-2024-04-15-at-20-03-01.png" width="600"/>
  <img src="https://i.ibb.co/sj6SYzy/Screenshot-2024-04-15-at-20-05-25.png" width="600"/>

- **Anonymization Types**:
  - **Replace**: Entities are replaced with unique placeholders. Example:
    ```
    Input: “My name is Aman, I gave an apple to Shreyansh and he gave it to Saurav who returned it back to Shreyansh.”
    Output: “My name is <PERSON_2>, I gave an apple to <PERSON_0> and he gave it to <PERSON_1> who returned it back to <PERSON_0>.”
    ```

  - **Hash**: Entities are replaced with unique hashes. Example:
    ```
    Input: “My name is Aman, I gave an apple to Shreyansh and he gave it to Saurav who returned it back to Shreyansh.”
    Output: “My name is <da12568c4a4247db193898d5569e821b>, I gave an apple to <da5c915d61d13224d7df954adfd09b00> and he gave it to <9a457b4bf029756dad0f32efeb54ee79> who returned it back to <da5c915d61d13224d7df954adfd09b00>.“
    ```

- **Anonymized Output**: Saved on the dashboard with a generated ID storing Input, Output, Share Status, 3rd party response (anonymized), and 3rd party response (deanonymized).

### De-anonymization

- **Entity Mapping**: Utilizes entity maps for de-anonymization. Refer to `entity_mapping.py`.

- **De-anonymization Logic**: Deanonymization logic and code are implemented in `@app.post("/de-ano")` in `main.py`.
