from invoke import task

@task
def queries(c, docs=False):
    c.run("PYTHONPATH='src' nodemon --watch src --exec python src/helpers/sample_queries.py")
    if docs:
        c.run("sphinx-build docs docs/_build")

@task
def correctJsons(c, docs=False):
    c.run("PYTHONPATH='src:scripts' nodemon --watch scripts --exec python scripts/add_semicolons_to_corrupt_jsons.py")

@task
def buildCorpus(c, docs=False):
    c.run("PYTHONPATH='src:scripts' nodemon --watch scripts --exec python scripts/build_corpus.py")


# @task
# def clean(c, docs=False, bytecode=False, extra=''):
#     patterns = ['build']
#     if docs:
#         patterns.append('docs/_build')
#     if bytecode:
#         patterns.append('**/*.pyc')
#     if extra:
#         patterns.append(extra)
#     for pattern in patterns:
#         c.run("rm -rf {}".format(pattern))

