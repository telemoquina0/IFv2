FROM python:3.12.7
WORKDIR /IFv2
COPY . /IFv2
RUN pip install -r requirements.txt
EXPOSE 5000
CMD python ./app.py
