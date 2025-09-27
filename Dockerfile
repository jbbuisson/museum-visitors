FROM python:3.12-slim
WORKDIR /app
# TODO: do not copy hidden directories like .git
COPY . /app
RUN pip install --upgrade pip && \
    pip install -e .
EXPOSE 5000 8888

CMD ["python", "-m", "museums_db"]