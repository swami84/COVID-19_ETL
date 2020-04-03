#!/bin/bash

echo $"Installing the dependencies for Covid-19 ETL Task"
python3 -m venv env
chmod u+x ./activate.sh
sh ./activate.sh
cd env
cp ../requirements.txt req.txt
pip install -r req.txt
cd ..
python3 src/run_ETL.py
