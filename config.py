import os

basedir = os.path.abspath(os.path.dirname(__file__))


# creating a configuration class
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'app.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb+srv://mikesoft:Emmanuel21@cluster0-lomxd.azure.mongodb.net/mike?retryWrites=true&w=majority'
