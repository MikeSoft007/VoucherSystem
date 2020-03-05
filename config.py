import os

basedir = os.path.abspath(os.path.dirname(__file__))


# creating a configuration class
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'activate.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://donjoe:praise1234@cluster0-shard-00-00-of0j7.azure.mongodb.net:27017,cluster0-shard-00-01-of0j7.azure.mongodb.net:27017,cluster0-shard-00-02-of0j7.azure.mongodb.net:27017/voucher?ssl=true&replicaSet=Cluster0-shard-0&authSource=admin&retryWrites=true&w=majority'