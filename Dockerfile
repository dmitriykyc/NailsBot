FROM python:3.8

WORKDIR /NailsBot
COPY requirements.txt /NailsBot
RUN pip install -r requirements.txt
COPY . /NailsBot
