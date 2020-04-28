FROM python:3
COPY . /app
WORKDIR /app
RUN pip install -U pip
RUN pip install -r requirements.txt
RUN python -m spacy download en_core_web_sm
RUN python install.py
RUN apt update
RUN apt install -y nano
EXPOSE 5000
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
