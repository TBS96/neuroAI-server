Neuro AI App
==============================

This project is a mental health assistant app basically, A User give a test and then based on that test, We will tell the user what kind of mental disorder he has and also Suggestion Exercise and meditation based on disorder he has.

This Project uses Sqlite3 as database.


<!-- Getting up and running
----------------------


The steps below will get you up and running with a local development environment. We assume you have the following installed:

* pip
* virtualenv

First open a terminal of a project then install and activate virtualenv.

After that, In a terminal we have to install Django, Django restframework, Simple JWT.

      $pip install django dajngorestframework djangorestframework-simplejwt

Run django migrations command for creating table.  

    $ python manage.py migrate

Fill Questions Table, Disorder Table and Disordersave Table through admin panel.

Then cd Mentalhealth and runserver.

       $ python manage.py runserver
 -->


# Installation Guide


## For Linux:
1. Install `python`
2.
```bash 
pip install virtualenv
```
3.
```bash 
cd neuroAI-server && python -m venv venv
```
4.
```bash
source venv/bin/activate
```
5.
```bash
python -m ensurepip --upgrade
```
6.
```bash
python -m pip install --upgrade pip setuptools wheel
```
7.
```bash
pip install -r requirements.txt
```
8.
```bash
python Mentalhealth/manage.py runserver <machine’s IP address>:8000
```


## For Windows:
1. Install `python`
2.
```bash 
pip install virtualenv
```
3.
```bash
cd neuroAI-server
```
4.
```bash
python -m venv Venv
```
5.
```bash
Venv\Scripts\activate
```
6.
```bash
python -m ensurepip --upgrade
```
7.
```bash
python -m pip install --upgrade pip setuptools wheel
```
8.
```bash
pip install -r requirements.txt
```
9.
```bash
python Mentalhealth/manage.py runserver <machine’s IP address>:8000
```
----------------------------------------------------------------

# Run server after initial setup (`Linux`)
```bash
source venv/bin/activate
```

```bash
python Mentalhealth/manage.py runserver <machine’s IP address>:8000
```

# Run server after initial setup (`Windows`)
```bash
Venv\Scripts\activate
```

```bash
python Mentalhealth/manage.py runserver <machine’s IP address>:8000
```


### Note:

#### To get your machine's IP address, open terminal paste the following:
- For `Linux`
```bash
hostname -I
```

- For `Windows`
```bash
ipconfig
```
and look for something like
```bash
IPv4 Address: 192.168.0.xxx
```

# Regenerate requirements.txt
```bash
pip freeze > requirements.txt
```