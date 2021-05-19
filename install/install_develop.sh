#!/bin/bash


cat ~/.ssh/id_rsa.pub
if [ ! $? == 0 ]; then
  echo "No hay clave"
  # DEBU<G
  echo ssh-keygen
  echo eval `ssh-agent`
  echo ssh-add ~/.ssh/id_rsa
  cat ~/.ssh/id_rsa.pub


echo "Agregá esto a el proveedor del repositorio git,"
echo "Fijate que la clave se asocie al root/agrupador de los proyectos así entran todos"
echo "Luego presioná una tecla"
while [ true ] ; do
  read -t 3 -n 1
if [ $? = 0 ] ; then
  exit ;
else
  echo "waiting for the keypress"
fi


git clone --recurse-submodules git@bitbucket.org:consultatio/rpa.git
cd rpa
git submodule update --remote rpa_robot


pip3 --version 2>/dev/null
if [ ! $? == 0 ]; then
  echo "Instalando pip3"
  sudo apt-get install python3-pip
fi

virtualenv -v 2>/dev/null
if [ ! $? == 0 ]; then
  echo "Instalando virtualenv"
  sudo pip3 install virtualenv
fi

if [ ! -e .env ]
then
  echo "Creando .env"
  virtualenv .env
fi

echo "Activando entorno virtual"
source .env/bin/activate

echo "Instalando Curl"
sudo apt install curl

echo "Instalando mySQL"
sudo apt-get install libmysqlclient-dev


echo "Instalando conexion con SqlServer"
sudo su
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/ubuntu/18.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
exit

sudo apt-get install unixodbc-dev



echo "Instalando dependencias"
pip3 install -r rpa_robot/install/requirements.txt #2>/dev/null


exit 0
