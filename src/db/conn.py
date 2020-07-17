import os
from dotenv import load_dotenv
from pyArango.connection import *

load_dotenv()
a_user  = os.getenv('ARANGO_USER')
a_pwd   = os.getenv('ARANGO_PWD')
a_url   = os.getenv('ARANGO_URL')
a_db    = os.getenv('ARANGO_DB')

conn = Connection(username=a_user, password=a_pwd, arangoURL=a_url)
print(f'ArangoDB connection: {conn}')

db = conn[a_db]
print(db)

# NODES
skills = db['skills']
jobs = db['jobs']

# EDGES
broader_jobs = db['broaderOcc']
broader_skills = db['broaderSkill']
related_skills = db['relatedSkill']
job_skills = db['jobSkills']

# VIEWS
allView = db['allView']


print('\n====== NODE COUNT ======\n')
print(f"There are {skills.count()} '{skills.name}' in the db.")
print(f"There are {jobs.count()} '{jobs.name}' in the db.")


print('\n====== EDGE COUNT ======\n')
print(f"There are {broader_jobs.count()} '{broader_jobs.name}' in the db.")
print(f"There are {broader_skills.count()} '{broader_skills.name}' in the db.")
print(f"There are {related_skills.count()} '{related_skills.name}' in the db.")
print(f"There are {job_skills.count()} '{job_skills.name}' in the db.")


aql = "FOR x IN skills RETURN COUNT(x)"
skills_cnt = db.AQLQuery(aql, rawResults=True, batchSize=100)
# for key in skills_cnt:
#   print(skills_cnt)

