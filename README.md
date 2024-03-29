# dsbd-backend

dashboard backend

### develop environment

```
mkdir venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

###    

```
python3 manage.py runserver --settings=dsbd.settings
```

## make migration

```
python3 manage.py makemigrations --settings=dsbd.develop_settings
python3 manage.py migrate --settings=dsbd.develop_settings
```

## SQL

```
# initial install
pip3 install PyYAML
```

### Dump SQL_DATA

```
python3 manage.py dumpdata --format=yaml myapp > myapp/fixtures/data.json --settings=dsbd.develop_settings
```

### R SQL_DATA

```
python manage.py loaddata --format=yaml myapp/fixtures/data.json --settings=dsbd.develop_settings
```