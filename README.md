# App Icon

[[_TOC_]]

## How to setup dependency?

```shell script
pip install -r requirements.txt
```

## How to run it?

```shell script
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## API

### How to upload with file?

```shell script
curl -X POST -F "file=@~/logo.png" https://api.appicon.org/api/icons/
```

### How to upload with link?

```shell script
curl -X POST -d "file_link=https://example.com/logo.png" https://api.appicon.org/api/icons/
``` 

## Domain

[AppIcon](https://api.appicon.org)

