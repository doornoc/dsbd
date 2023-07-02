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