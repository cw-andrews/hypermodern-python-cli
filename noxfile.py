import nox


@nox.session(python=["3.8", "3.7"])
def tests(session):
    args = session.posargs or ["-v", "--cov"]
    session.run("poetry", "install", external=True)
    session.run("pytest", *args)
