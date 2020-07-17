from db.python_arango import getDB


def first_5_jobs(db):
  print('\n===== First 5 jobs =====\n')
  query = 'FOR d IN jobs LIMIT 5 RETURN d'
  cursor = db.aql.execute(query)
  for job in cursor:
    print(job['preferredLabel'])


def first_5_skills(db):
  print('\n===== First 5 skills =====\n')
  query = 'FOR d IN skills LIMIT 5 RETURN d'
  cursor = db.aql.execute(query)
  for skill in cursor:
    print(skill['preferredLabel'])




def run_sample_queries(db):
	first_5_jobs(db)
	first_5_skills(db)


def test_aql(db):
  test_query = 'FOR d IN skills LIMIT 1 RETURN d'
  db.aql.explain(test_query)
  db.aql.validate(test_query)


if __name__ == "__main__":
  db = getDB()
  test_aql(db)
  run_sample_queries(db)
