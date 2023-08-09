## Clone repo
```bash
git clone https://github.com/MihailRoot/MihailRoot-test-o-parser.git
```
```
cd MihailRoot-test-o-parser
```

## Install redis, celery, mysql
```
apt update && apt install redis mysql-server celery
```

## Installing pip requirements
```bash
pip install -r requirements.txt
```

## Setup 

### Setup mysql

In `settings.py`

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'test',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
```
## Usage
```
python3 manage.py migrate && python3 manage.py runserver

```

## Chat with bot
```
https://t.me/TESTBOT_API
```

## Bot
```
@testozonapi_bot
```
