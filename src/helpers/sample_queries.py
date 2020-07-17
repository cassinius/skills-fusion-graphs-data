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


def like_query(db):
    print('\n===== LIKE query =====\n')
    query = """
      FOR d IN skills
      FILTER
        LOWER(d.preferredLabel) LIKE 'javascript%' OR
        LOWER(d.preferredLabel) LIKE 'typescript%' OR
        LOWER(d.preferredLabel) LIKE 'python%'
      RETURN DISTINCT d.preferredLabel
    """
    cursor = db.aql.execute(query)
    for skill in cursor:
        print(skill)


def search_view_query(db):
    print('\n===== SEARCH query =====\n')
    search = 'javascript,python,ruby,rust'
    boost = 'javascript'
    query = """
      LET keywords = TOKENS(@search, 'text_en')
      LET importantKeyword = TOKENS(@boost, 'text_en')[0]
      
      FOR d IN skillsView
      SEARCH ANALYZER(
        d.description IN keywords
        OR BOOST(d.description == importantKeyword, 3)
        , 'text_en'
      )
      SORT BM25(d) DESC
      LIMIT 30
      RETURN DISTINCT d.preferredLabel
    """
    cursor = db.aql.execute(
        query, bind_vars={'search': search, 'boost': boost})
    for skill in cursor:
        print(skill)


def graph_traversal_query(db):
    print('\n===== GRAPH traversal query =====\n')
    query = """
      FOR d IN skills
      FILTER d.preferredLabel == 'skills'
      LIMIT 1
      
      FOR target, edge, path IN 3..3 INBOUND
      d
      GRAPH 'escoGraph'
      FILTER LOWER(target.preferredLabel) LIKE '%plant%'
      COLLECT skills = {
        label: target.preferredLabel
      }
      RETURN skills
    """
    cursor = db.aql.execute(query)
    # print(cursor)
    for skill in cursor:
        print(skill['label'])


def search_graph_query(db):
    print('\n===== GRAPH search query =====\n')
    input_text = 'javascript python'
    important = 'graph'
    query = """
      LET keywords = TOKENS(@input_text, 'text_en')      

      FOR d IN skillsView
      SEARCH ANALYZER(
        d.description IN keywords
        OR BOOST(d.description == @important, 3)
        , 'text_en'
      )
      SORT BM25(d) DESC
      LIMIT 10
      
      FOR o,e,p IN 1..1 INBOUND 
      d
      jobSkills 
      FILTER p.edges[*].relType ANY == 'essential'
      
      COLLECT label = o.preferredLabel INTO jobs
      SORT LENGTH(jobs[*].p.vertices[*]) DESC
      LET ULA = UNIQUE(jobs[*].p.vertices[*].preferredLabel[** FILTER CURRENT != label])
      RETURN {
        jobs: label, 
        skills: ULA
      }
    """
    cursor = db.aql.execute(query, bind_vars={'input_text': input_text, 'important': important})
    for jobs in cursor:
      print(jobs)


def run_sample_queries(db):
    first_5_jobs(db)
    first_5_skills(db)
    like_query(db)
    search_view_query(db)
    graph_traversal_query(db)
    search_graph_query(db)


def test_aql(db):
    test_query = 'FOR d IN skills LIMIT 1 RETURN d'
    db.aql.explain(test_query)
    db.aql.validate(test_query)


if __name__ == "__main__":
    db = getDB()
    test_aql(db)
    run_sample_queries(db)
