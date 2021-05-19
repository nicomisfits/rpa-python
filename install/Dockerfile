FROM python:3.8




# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable


## install chromedriver
#RUN apt-get install -yqq unzip
#RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
#RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/


########################################
#### instalo cosas particulares de Fusap
########################################
RUN apt-get install libmariadb-dev -y


# install FreeTDS and dependencies
RUN apt-get update \
 && apt-get install unixodbc -y \
 && apt-get install unixodbc-dev -y \
 && apt-get install freetds-dev -y \
 && apt-get install freetds-bin -y \
 && apt-get install tdsodbc -y \
 && apt-get install --reinstall build-essential -y

# populate "ocbcinst.ini"
RUN echo "[FreeTDS]\n\
Description = FreeTDS unixODBC Driver\n\
Driver = /usr/lib/x86_64-linux-gnu/odbc/libtdsodbc.so\n\
Setup = /usr/lib/x86_64-linux-gnu/odbc/libtdsS.so" >> /etc/odbcinst.ini


RUN apt-get install curl
RUN apt-get install apt-transport-https
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/16.04/prod.list | tee /etc/apt/sources.list.d/msprod.list

RUN apt-get update
ENV ACCEPT_EULA=y DEBIAN_FRONTEND=noninteractive
RUN apt-get install mssql-tools unixodbc-dev -y



RUN pip install --trusted-host pypi.python.org pyodbc==4.0.26

#RUN pip install selenium
#RUN pip install gspread
#RUN pip install configparser
#RUN pip install oauth2client
#RUN pip install mysqlclient

COPY ./requirements.txt /var/www/requirements.txt
RUN pip install -r /var/www/requirements.txt

########################################
WORKDIR /usr/workspace
RUN mkdir -p /usr/workspace

COPY . /usr/workspace


# set display port to avoid crash
ENV DISPLAY=:99



# Expose
EXPOSE  8090

ENTRYPOINT ["python"]
CMD ["fusap_rpa_test_fwk/fusap_ws_runner/run.py"]
