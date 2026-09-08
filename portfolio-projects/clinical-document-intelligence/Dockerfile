FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install .
CMD ["python","-c","from clinical_intel.extract import extract; print(extract('Study ID: DEMO-1'))"]
