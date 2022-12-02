# link shortener
## Getting started

In order to start using the bot, write the following commands:

Make a clone of the repository
```python
$ git clone https://github.com/dennyaap/link_shortener.git
```
```python
$ cd link_shortener
```

Create a virtual environment:
```python
$ python -m venv venv
```

Activate the virtual environment:
```python
$ venv/Scripts/activate
```

or for mac os:
```python
$ source venv/bin/activate
```

Install all required dependencies:
```python
$ pip install -r requirements.txt
```

And finally create an .env file in the main_app folder, in which specify: (for example)
```
SECRET_KEY=sweetchocolate123
DATABASE_URI=postgresql://postgres:root@localhost/link_shortener
SERVER_URI=http://127.0.0.1:5000
``` 

To run the application use the command:
```python
flask --app start run
```


## Enjoy using ! :relaxed: