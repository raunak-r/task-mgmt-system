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
```
pip install postgres
pip install psycopg2-binary
```

## The following project contains 2 Modules:

1. Notes (Application)
2. Master (Web Framework)

## Running the tests in Notes Application

Currently the Project has these Api's in working.
###
```
INDEX PAGE: > http://127.0.0.1:8000/Notes/index/

1. See all tasks Grouped by Label (Todo, Doing, Done)
	> GET via Postman via /Notes/tasks

2. Post a new Task
	> POST via Postman via /Notes/tasks/

3. Update a Task (Change Anything except Author) 
	> PUT via Postman via /Notes/tasks/?id=

4. Delete a Task
	> DELETE via Postman via /Notes/tasks/?id=

5. See a Task by it's ID
	> /Notes/tasks/?id=


5. See All Comments Ordered by Task ID
	> GET via Postman via /Notes/comments

6. Post a new comment given Task Id, Author and the Comment Text
	> POST via Postman via 

7. Update text on a comment given Comment ID
	> PUT via Postman via /Notes/comments/?id=
```

## DATABASE EXPLAINED

### Task Table
FIELDS THAT CANNOT BE BLANK = Title. Label. CreatedBy. DueDate
CAN BE BLANK = Description. Color. Comments. Attachment
```
	LABEL_LIST = (
        ('1', 'Todo'),
        ('2', 'Doing'),
        ('3', 'Done'),
    )
	COLOURS = (
		('#808080','Gray'),
		('#000000','Black'),
		('#FF0000','Red'),
		('#0000FF','Blue')
	)	

	taskId = AutoField(primary_key=True)
	title = CharField(max_length = 30, blank=False)
	description = CharField(max_length = 100, blank=True)
	label = CharField(max_length=1, choices=LABEL_LIST, blank=False)
	color = CharField(max_length=7, choices=COLOURS, blank=True) #STORE A HEX FIELD.
	attachment = FileField(upload_to='attachments', blank=True)
	comments = CharField(max_length=255, blank=True)
	createdBy = CharField(max_length=10, blank=False)
	dueDate = DateField(null=False)
```

### Comments Table
* FIELDS THAT CANNOT BE BLANK = createdBy, CommentText.
* Rest all are auto inserted.
```
	commentId = AutoField(primary_key=True)
	taskId = ForeignKey(Task, null=False, blank=False)
	createdOn = DateTimeField(auto_now_add=True)
	UpdatedOn = DateTimeField(auto_now_add=True)
	createdBy = CharField(max_length=10, blank=False)
	commentText = CharField(max_length=100, blank=False)
```
## Acknowledgments

* The Definitive Guide to Django
* Two Scoops of Django