#!/bin/bash
cd ..

yum install git

cd
mkdir rpa-robot
cd rpa-robot
git clone






yum install python3 -y
yum install mysql mysql-devel mysql-lib

curl https://packages.microsoft.com/config/rhel/7/prod.repo > /etc/yum.repos.d/mssql-release.repo
yum remove unixODBC-utf16 unixODBC-utf16-devel #to avoid conflicts
ACCEPT_EULA=Y yum install msodbcsql17


python3 -m venv .env
source .env/bin/activate

pip install -r requirements.txt



################ con Docker



sudo docker start
#Construimos la imagen
docker build .
docker images
#Le ponemos un nombre
docker tag dc7504b319d4 rpa
#Creamos el container
docker run --name rpa_python -dit --network host -w /usr/workspace -v $(pwd):/usr/workspace rpa python


Si no está creado el container:

docker start
docker run --name rpa_python -dit --network host -w /usr/workspace -v $(pwd):/usr/workspace rpa python





#Creamos el alias (para correrlos más cómodo)
alias robot.rpa='docker exec -it rpa_python'

#Corremos el automatismo
robot.rpa backoffice/cotizacion_dolar_db/run.py



######################################333
INSTALL docker on linux amazon

yum update -y
amazon-linux-extras install docker
service docker start

sudo service docker start
sudo usermod -a -G docker ec2-user
usermod -a -G docker ec2-user
docker info
sudo service docker start
service docker start
passwd -a $USER docker
service docker start










if [ ! -e /opt/google/chrome/chromedriver ]
then
  echo "Instalando chromedriver"
  curl https://chromedriver.storage.googleapis.com/81.0.4044.138/chromedriver_linux64.zip --output /opt/google/chrome/chromedriver_linux64.zip
  unzip /opt/google/chrome/chromedriver_linux64.zip
  rm /opt/google/chrome/chromedriver_linux64.zip
fi


echo "Instalando conexion con SqlServer"
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/ubuntu/18.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
exit

apt-get install unixodbc-dev




if [ ! -e .env ]
then
  echo "Creando .env"
  virtualenv .env
fi




echo "Activando entorno virtual"
source .env/bin/activate

cd install/
echo "Instalando dependencias"
pip3 install -r requirements.txt #2>/dev/null
