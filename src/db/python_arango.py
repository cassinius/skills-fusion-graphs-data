import os
from dotenv import load_dotenv
from arango import ArangoClient

load_dotenv() # if this fails or is missing
a_user  = os.getenv('ARANGO_USER') # those will return 'None'
a_pwd   = os.getenv('ARANGO_PWD')
a_url   = os.getenv('ARANGO_URL')
a_db    = os.getenv('ARANGO_DB')

client = ArangoClient()
db = None


def getDB():
  global db
  if db is not None:
    print(f'Database {db} already instantiated.')
    return db

  db = client.db(a_db, username=a_user, password=a_pwd)
  print(f'Loaded database `{db.name}`')

  # print(db.collections())
  # print(db.views())

  # ------------- NODES -------------

  skills = db.collection('skills')
  jobs = db.collection('jobs')

  # print('\n====== NODES ======\n')
  # print(f'Loaded nodes `{skills.name}`')
  # print(f'Loaded nodes `{jobs.name}`')

  print('\n====== NODE COUNT ======\n')
  print(f'There are {skills.count()} `{skills.name}` in the db.')
  print(f'There are {jobs.count()} `{jobs.name}` in the db.')

  # ------------- EDGES -------------

  broader_jobs = db.collection('broaderOcc')
  broader_skills = db.collection('broaderSkill')
  related_skills = db.collection('relatedSkill')
  job_skills = db.collection('jobSkills')

  print('\n====== EDGE COUNT ======\n')
  print(f'There are {broader_jobs.count()} `{broader_jobs.name}` in the db.')
  print(f'There are {broader_skills.count()} `{broader_skills.name}` in the db.')
  print(f'There are {related_skills.count()} `{related_skills.name}` in the db.')
  print(f'There are {job_skills.count()} `{job_skills.name}` in the db.')

  # ------------- GRAPHS -------------

  graph = db.graph('escoGraph')

  print('\n====== GRAPHS ======\n')
  print(f'Loaded graph `{graph.name}`.')

  # ------------- VIEWS --------------

  allView = db.view('allView')
  jobsView = db.view('jobsView')
  skillsView = db.view('skillsView')
  userTeamsView = db.view('userTeamsView')

  print('\n====== VIEWS ======\n')
  print(f'Loaded search view `{allView["name"]}`.')
  print(f'Loaded search view `{jobsView["name"]}`.')
  print(f'Loaded search view `{skillsView["name"]}`.')
  print(f'Loaded search view `{userTeamsView["name"]}`.')

  return db


if __name__ == "__main__":
  getDB()
