#!/bin/sh

echo $"Installing the dependencies for Covid-19 ETL Task"
python3 -m venv env
chmod u+x ./act_env.sh
source ./act_env.sh
#sourceFile="./env/bin/activate"
#source ${sourceFile}
#alias activate  = "source env/bin/activate"
#activate
#$(source env/bin/activate)


cd env
cp ../requirements.txt req.txt
pip install -r req.txt
cd ..
env/bin/python3 src/run_ETL.py
