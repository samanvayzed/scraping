FROM gcr.io/google-appengine/python
RUN apt-get update
RUN apt-get install -y xvfb
RUN apt-get install -y firefox

RUN mkdir -p /usr/local/bin 
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.24.0/geckodriver-v0.24.0-linux64.tar.gz
RUN tar -xvzf geckodriver-v0.24.0-linux64.tar.gz 
RUN cp geckodriver /usr/local/bin 
RUN curl -sSL https://sdk.cloud.google.com | bash
LABEL python_version=python3.6




#ENV PYTHONUNBUFFERED 1

RUN virtualenv --no-download /env -p python3.6
ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/

RUN cat requirements.txt
RUN pip install -r requirements.txt
COPY . /code/




