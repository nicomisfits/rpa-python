#!/bin/bash
cd ..

python3.6 --version 2>/dev/null
if [ ! $? == 0 ]; then
  echo "Instalando Python3.6"
  sudo apt-get install python3-setuptools

  sudo apt update
  sudo apt install software-properties-common
  sudo add-apt-repository ppa:deadsnakes/ppa
  sudo apt install python3.6
fi


pip3 --version 2>/dev/null
if [ ! $? == 0 ]; then
  echo "Instalando pip3"
  sudo apt-get install python3-pip
fi


sudo apt-get install python-pip python-dev libmysqlclient-dev


virtualenv -v 2>/dev/null
if [ ! $? == 0 ]; then
  echo "Instalando virtualenv"
  sudo pip3 install virtualenv
fi


if [ ! -e /opt/google/chrome/chromedriver ]
then
  echo "Instalando chromedriver"
  sudo curl https://chromedriver.storage.googleapis.com/81.0.4044.138/chromedriver_linux64.zip --output /opt/google/chrome/chromedriver_linux64.zip
  sudo unzip /opt/google/chrome/chromedriver_linux64.zip
  sudo rm /opt/google/chrome/chromedriver_linux64.zip
fi


echo "Instalando conexion con SqlServer"
sudo su
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/ubuntu/18.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
exit

sudo apt-get install unixodbc-dev




if [ ! -e .env ]
then
  echo "Creando .env"
  virtualenv .env
fi




echo "Activando entorno virtual"
source .env/bin/activate

echo "Instalando dependencias"
pip3 install -r requirements.txt #2>/dev/null
