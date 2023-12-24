#!/usr/bin/env python3

"""
Test mongo connection availability.
"""

import sys
from os import getenv

try :
    from pymongo import MongoClient
    from pymongo.errors import ConnectionFailure
except ImportError :
    print('Cannot find pymongo, try installing by executing:\npip install pymongo')
    sys.exit(4)


def mongo_connection() -> bool :
    """Test MongoDB connection."""
    mongo_url = f"mongodb://localhost:{getenv('MONGO_PORT')}"

    try :
        # https://pymongo.readthedocs.io/en/stable/api/pymongo/mongo_client.html
        client = MongoClient(mongo_url, serverSelectionTimeoutMS=5000)
        # The ismaster command is cheap and does not require auth.
        client.admin.command('ismaster')
    except ConnectionFailure :
        result = False
    else :
        result = True
        client.close()
    return result

    # Test user credentials
    # https://www.mongodb.com/docs/manual/reference/connection-string/
    # https://www.urlencoder.io/python/
    # mongodb_url = f"mongodb://{urllib.parse.quote(getenv('MONGO_INITDB_ROOT_USERNAME'))}:{urllib.parse.quote(getenv('MONGO_INITDB_ROOT_PASSWORD'))}@localhost:{getenv('MONGO_PORT')}/?authSource={getenv('MONGO_INITDB_DATABASE')}"

    # client = MongoClient(mongodb_url)
    # db = client.get_database(getenv('MONGO_INITDB_DATABASE'))
    # return db.command('ping').get('ok') == 1.0

    # Issue the serverStatus command and print the results
    # pprint(db.list_collection_names())
    # serverStatusResult=db.command("serverStatus")


if __name__ == '__main__' :
    if mongo_connection() :
        sys.exit(0)
    else :
        sys.exit(1)
