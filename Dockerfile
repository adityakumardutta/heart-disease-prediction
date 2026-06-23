FROM python:3.10-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_DEBUG=0

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt setup.py ./
COPY src ./src
COPY app.py train.py ./
COPY templates ./templates
COPY static ./static
COPY Notebook_Experiments/Data ./Notebook_Experiments/Data

RUN pip install --no-cache-dir -r requirements.txt

# Generate model artifacts during image build
RUN python train.py

EXPOSE 8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
