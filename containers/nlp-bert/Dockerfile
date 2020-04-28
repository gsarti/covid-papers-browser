FROM tensorflow/tensorflow:1.12.0-py3
RUN pip install -U pip
RUN pip install --no-cache-dir bert-serving-server
RUN pip install -U bert-serving-server[http]
COPY ./ /app
COPY ./entrypoint.sh /app
WORKDIR /app
ENTRYPOINT ["/app/entrypoint.sh"]
CMD []
