from main_app import app, database_uri

from flask_sqlalchemy import SQLAlchemy

#database connection
database_uri = database_uri

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
db = SQLAlchemy(app)