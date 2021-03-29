FROM python:3.9.2-slim-buster

WORKDIR /code

COPY requirements.txt /code

# RUN pip3 install psycopg2-binary openpyxl Unidecode textract wordcloud nltk numpy dash pandas gunicorn flask

RUN pip3 install -r requirements.txt

# Expose Ports
EXPOSE 8050

# CMD ["gunicorn", "--workers=5", "--threads=1", "-b 0.ffdfd0.0.0:8050", "app:server"]

CMD ["./start.sh"]