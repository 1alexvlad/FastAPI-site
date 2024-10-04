FROM python:3.9

RUN mkdir /booking

WORKDIR /booking

COPY requirements.txt .

RUN pip install -r requirements.txt 

COPY . .

RUN chmod a+x /booking/docker/*.sh

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]