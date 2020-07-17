from invoke import task


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


@task
def queries(c, docs=False):
    c.run("PYTHONPATH='src' nodemon --watch src --exec python src/helpers/sample_queries.py")
    if docs:
        c.run("sphinx-build docs docs/_build")
