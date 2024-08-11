from collections import defaultdict
from io import BytesIO
from PIL import Image
from pydantic import BaseModel
import uvicorn, urllib3, spacy, nest_asyncio, base64
from fastapi import FastAPI, HTTPException, UploadFile, File, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import RecognizerResult,OperatorConfig, OperatorResult
from presidio_anonymizer.operators import Operator, OperatorType
import json
import os
from typing import List, Dict, Any
import pytesseract

# import google.generativeai as genai
from pdf2image import convert_from_path, convert_from_bytes
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)
import magic

from spacybison.run_llm import run_llm
from entity_mapping import InstanceCounterAnonymizer
from selected_entities import selected_entities
from list2string import convert_list_to_string

# GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
# model = genai.GenerativeModel('gemini-1.5-pro')

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
     allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)

class direct(BaseModel):
  text: str
@app.post("/")
async def direct(input: direct):
  analyzed_text = run_llm(input.text)

  anonymizer = AnonymizerEngine()
  anonymized_text = anonymizer.anonymize(text=input.text, analyzer_results=anodata(analyzed_text))
  
  return anonymized_text


analyzed_text = None
class text_input(BaseModel):
  text: str
@app.post('/text')
async def analyze_text(input_text : text_input):
  results = run_llm(input_text.text)
  return results


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

class entities_input(BaseModel):
    text: str
    all_entities: List[Dict[str, Any]]
    entities: List[str]
    type: str
@app.post("/anonymize")
async def anonymize_text(pii: entities_input):
    entities = pii.entities
    if not entities:
        raise HTTPException(status_code=400, detail="At least one entity type must be provided.")
    
    user_entities = [entity for entity in pii.all_entities if entity['entity_type'] in entities]
    analyzed_text = anodata(user_entities)

    anonymizer = AnonymizerEngine()
    operator_config = OperatorConfig(pii.type)

    entity_mapping = None
    if pii.type == 'replace':
        entity_mapping = dict()
        operator_config = OperatorConfig("entity_counter", {"entity_mapping": entity_mapping})
        anonymizer.add_anonymizer(InstanceCounterAnonymizer)

    anonymized_text = anonymizer.anonymize(
        text=pii.text,
        analyzer_results=analyzed_text,
        operators={"DEFAULT": operator_config}
    )

    return {
        "anonymized_text": anonymized_text,
        "entity_mapping": entity_mapping
    }




@app.post("/i2t")
async def anonymize_ocr(file: UploadFile = File(...)):
    file_sample = await file.read(2048)
    file.file.seek(0)

    mime = magic.Magic(mime=True)
    file_type = mime.from_buffer(file_sample)

    if file_type in ("image/jpeg", "image/png", "image/bmp", "image/gif"):
        print("it's image")
        return await ocr_image(file)
    elif file_type == "application/pdf":
        print("it's pdf")
        return await ocr_pdf(file)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file format")

async def ocr_image(file: UploadFile):
    image = Image.open(BytesIO(await file.read()))
    ocr_text = pytesseract.image_to_string(image=image)

    return ocr_text


async def ocr_pdf(file: UploadFile):
    file_bytes = await file.read()
    pages = convert_from_bytes(pdf_file=file_bytes, fmt="jpeg")

    extracted_text = []

    for page in pages:
        image = page
        ocr_text = pytesseract.image_to_string(image=image)
        append_text = ocr_text
        extracted_text.append(append_text)
        
    ocr_text = convert_list_to_string(extracted_text)
    return ocr_text




class de_ano(BaseModel):
    entity_mapping: str
    text: str

@app.post("/de-ano")
async def replace_entities(de_ano: de_ano):
    entity_mapping = json.loads(de_ano.entity_mapping)
    entity_mapping = de_ano.entity_mapping
    text = de_ano.text

    for entity_type, entity_values in entity_mapping.items():
        for original_text, unique_identifier in entity_values.items():
            text = text.replace(unique_identifier, original_text)

    return text