FROM python:3.9


WORKDIR /code
COPY ./requirements.txt /code/requirements.txt 
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app
COPY ./app/ihmpolytech-15b17-firebase-adminsdk-xhoym-6f6672a5ab.json /code/ihmpolytech-15b17-firebase-adminsdk-xhoym-6f6672a5ab.json
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]