FROM python:3.12
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --cache-dir --upgrade -r /code/requirements.txt
COPY ./ /code
CMD ["fastapi", "run", "main.py"]
