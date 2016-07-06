from invoke import task, run


@task
def test():
    run('py.test test_flask_redislite.py', pty=True)


@task
def coverage():
    run('py.test --cov=flask_redislite test_flask_redislite.py', pty=True)


@task
def pep8():
    run('py.test --pep8 test_flask_redislite.py', pty=True)


@task
def full():
    run('py.test --pep8 --cov=flask_redislite test_flask_redislite.py', pty=True)


@task
def travisci():
    run('py.test --pep8 --cov=flask_redislite test_flask_redislite.py')
