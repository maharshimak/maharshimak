FROM python:3.12-slim
WORKDIR /app
COPY . .
RUN pip install .
CMD ["python","-c","from multimodal_studio.planner import plan,to_json; print(to_json(plan('cinematic slow motion subtitles')))"]
