#!/bin/bash

echo $"Installing the dependencies for Covid-19 ETL Task"
python3 -m venv env
#chmod u+x ./activate.sh
#source $(pwd)/activate.sh
#sourceFile="./env/bin/activate"
#source ${sourceFile}
activate () {
    echo Activating Virtual Environment...
    source $(pwd)/env/bin/activate
}
export -f activate
activate
source ~/.bash_profile

# source the virtualenv
source env/bin/activate
cd env
cp ../requirements.txt req.txt
pip install -r req.txt
cd ..
python3 src/run_ETL.py
