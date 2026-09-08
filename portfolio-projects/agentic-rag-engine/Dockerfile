FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install .
CMD ["python","-c","from rag_engine.core import Document, hybrid_retrieve; print(hybrid_retrieve('rag',[Document('1','rag retrieval')]))"]
