FROM python:3
ADD requirements.txt /
RUN pip3 install cython wheel
RUN pip3 install -r requirements.txt
WORKDIR /app
COPY . /app/
ENTRYPOINT ["python3", "hl7v2GenomicsLabMiddleware.py"]
