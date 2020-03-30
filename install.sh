echo $"Installing the dependencies for Covid-19 ETL Task"
python3 -m venv env
alias activate_env = "source /env/bin/activate"
activate_env
cd env
cp ../requirements.txt req.txt
pip install -r req.txt
cd ..
python3 src/run_ETL.py
