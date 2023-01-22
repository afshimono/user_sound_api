FROM python:3.9-alpine

WORKDIR /user_sound

COPY ./user_sound/requirements.txt /user_sound/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /user_sound/requirements.txt

COPY ./user_sound/main.py /user_sound/
COPY ./user_sound/settings.py /user_sound/
COPY ./user_sound/__init__.py /user_sound/
COPY ./user_sound/core /user_sound/core
COPY ./user_sound/v1 /user_sound/v1

WORKDIR /

CMD ["uvicorn", "user_sound.main:app", "--host", "0.0.0.0", "--port", "8000"]