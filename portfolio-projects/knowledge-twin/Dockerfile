FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install .
CMD ["python","-c","from knowledge_twin.graph import KnowledgeGraph; print(KnowledgeGraph())"]
