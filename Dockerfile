FROM python:3.9-slim

ENV OPENAI_API_KEY=""
ENV PALM_API_KEY=""

RUN apt-get update \
    && apt-get install -y tesseract-ocr \
    && apt-get install -y --no-install-recommends \
    poppler-utils \
    libmagic1\
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

RUN pip install numpy==1.26.4 spacy
RUN python -m spacy download en_core_web_sm

COPY . /app/

EXPOSE 7860

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]