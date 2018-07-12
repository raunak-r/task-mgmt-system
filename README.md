# Task Management System

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 
1. Set up a new virtualenv directory.

```
virtualenv .
source bin/activate
Pull the repository
```

### Prerequisites

The project is implemented on 
1. Django 1.8
2. Python 2.7
3. Postgres

The requirements.txt file contains the python packages which needs to be installed. 

```
pip install -r /Master/requirements.txt
```
<h4>Database (Postgres)</h4>

1. Install Postgres App. A quick google search will do.
2. install postgres packages using Pip

		pip install postgres
		pip install psycopg2
		pip install psycopg2-binary

## The following project contains 2 Modules:

1. Notes (Application)
2. Master (Web Framework)

## Running the tests in Notes Application
Currently the Project has these urls in working.
```
http://127.0.0.1:8000/tasks/index

```
## Acknowledgments

* The Definitive Guide to Django
* Two Scoops of Django