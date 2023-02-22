FROM python:3.9
ADD requirements.txt /
RUN pip3 install cython==0.29.21
RUN pip3 install wheel==0.37.0
RUN pip3 install hl7v2GenomicsExtractor
RUN pip3 install hl7==0.4.5
RUN pip3 install PyYAML==6.0
WORKDIR /app
COPY . /app/
ENTRYPOINT ["python3", "hl7v2GenomicsLabMiddleware.py"]
