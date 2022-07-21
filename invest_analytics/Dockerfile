FROM python:3.9
RUN apt-get update -y
RUN apt-get upgrade -y

WORKDIR /invest_analytics

COPY ./requirements.txt ./
RUN pip install -r requirements.txt
ENV DJANGO_SKEY_INVEST_ANALYTICS='secret_key'
COPY ./ ./
# You need to specify a token from tinkoff invest
# ENV TINVEST_TOKEN=''

CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000" ]