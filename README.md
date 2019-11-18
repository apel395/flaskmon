running local


import json to mongodb
'''
mongoimport --db datadb --collection data --file datasetfinal.json
'''

create & activate environment
in osx
'''
virtualenv env -p /usr/bin/python3 && source env/bin/activate
'''
in windows os
'''
virtualenv env
env\Script\activate
'''

install requirements
'''
pip install -r requirements.txt
'''

run app
'''
python main.py
'''