import os
from dotenv import load_dotenv
from arango import ArangoClient

load_dotenv() # if this fails or is missing
a_user  = os.getenv('ARANGO_USER') # those will return 'None'
a_pwd   = os.getenv('ARANGO_PWD')
a_url   = os.getenv('ARANGO_URL')
a_db    = os.getenv('ARANGO_DB')

client = ArangoClient()
db = client.db(a_db, username=a_user, password=a_pwd)
print(db)



print(db.views())

