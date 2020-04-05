FROM python:3.7
WORKDIR /usr/src/app
COPY ./requirements.txt .
RUN pip install -r ./requirements.txt
# spacy needs to download the model
RUN python -m spacy download en_core_web_sm
COPY . .
RUN chmod 755 ./scripts/start.sh
EXPOSE 5000
CMD ["./scripts/start.sh"]