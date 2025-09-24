FROM python:3.12-slim
WORKDIR /app
COPY . /app
RUN pip install --upgrade pip && \
    pip install -e .
EXPOSE 5000 8888

CMD ["python", "-m", "museums_db"]