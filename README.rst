more.basicauth: HTTP Basic Authentication integration for Morepath
==================================================================

Overview
--------

This is a Morepath_ authentication extension for HTTP Basic Authentication.
It was originally part of Morepath, but since basic auth is almost always what
you don't want we decide to move it to a separate extension.

Some Pros and Cons:

*  This argues against basic auth:
   http://adrianotto.com/2013/02/why-http-basic-auth-is-bad
*  But this argues *for* basic auth:
   https://www.rdegges.com/2015/why-i-love-basic-auth

Alternative authentication extensions for morepath are:

* `more.jwtauth`_:
  A token based authentication sytem using JSON Web Token (JWT).
* `more.isdangerous`_:
  A cookie based identity policy using isdangerous.

.. _Morepath: http://morepath.readthedocs.org
.. _more.jwtauth: https://github.com/morepath/more.jwtauth
.. _more.isdangerous: https://github.com/morepath/more.itsdangerous


Introduction
------------

Basic authentication is special in a number of ways:

* The HTTP response status that triggers basic auth is Unauthorized
  (401), not the default Forbidden (403). This needs to be sent back
  to the browser each time login fails, so that the browser asks the
  user for a username and a password.

* The username and password combination is sent to the server by the
  browser automatically; there is no need to set some type of cookie
  on the response. Therefore ``remember_identity`` does nothing.

* With basic auth, there is no universal way for a web application to
  trigger a log out. Therefore ``forget_identity`` does nothing
  either.

To trigger a ``401`` status when time Morepath raises a ``403`` status,
we can use an exception view, something like this::

  from webob.exc import HTTPForbidden

  @App.view(model=HTTPForbidden)
  def make_unauthorized(self, request):
      @request.after
      def set_status_code(response):
          response.status_code = 401
      return "Unauthorized"

For the login code, as ``remember_identity`` is not an option,
you can just check the password::

    # check whether user has password, using password hash and database
    if not user_has_password(username, password):
        return "Sorry, login failed" # or something more fancy

Note that ``user_has_password`` stands in for whatever method you use
to check a user's password; it's not part of Morepath.


Usage
-----

Here a full example for a basic setup::

    import morepath
    from more.basicauth import BasicAuthIdentityPolicy
    from webob.exc import HTTPForbidden


    class App(morepath.App):
        pass


    @App.identity_policy()
    def get_identity_policy():
        return BasicAuthIdentityPolicy()


    @App.verify_identity()
    def verify_identity(identity):
        # Do the password validation.
        return user_has_password(identity.username, identity.password)


    @App.view(model=HTTPForbidden)
    def make_unauthorized(self, request):
        @request.after
        def set_status_code(response):
            response.status_code = 401

        return "Unauthorized"


The login form could look like::

    from webob.exc import HTTPProxyAuthenticationRequired


    class Login(object):
        pass


    @App.path(model=Login, path='login')
    def get_login():
        return Login()


    @App.view(model=Login, request_method='POST')
    def login(self, request):
        username = request.POST['username']
        password = request.POST['password']

        # Do the password validation.
        if not user_has_password(username, password):
            raise HTTPProxyAuthenticationRequired('Invalid username/password')

        return "You're logged in."  # or something more fancy


Requirements
------------

-  Python (2.7, 3.3, 3.4, 3.5)
-  morepath (>= 0.16.1)


Developing more.basicauth
=========================

Install more.basicauth for development
--------------------------------------

.. highlight:: console

Clone more.basicauth from github::

  $ git clone git@github.com:morepath/more.basicauth.git

If this doesn't work and you get an error 'Permission denied (publickey)',
you need to upload your ssh public key to github_.

Then go to the more.basicauth directory::

  $ cd more.basicauth

Make sure you have virtualenv_ installed.

Create a new virtualenv for Python 3 inside the more.basicauth directory::

  $ virtualenv -p python3 env/py3

Activate the virtualenv::

  $ source env/py3/bin/activate

Make sure you have recent setuptools and pip installed::

  $ pip install -U setuptools pip

Install the various dependencies and development tools from
develop_requirements.txt::

  $ pip install -Ur develop_requirements.txt

For upgrading the requirements just run the command again.

If you want to test more.basicauth with Python 2.7 as well you can create a
second virtualenv for it::

  $ virtualenv -p python2.7 env/py27

You can then activate it::

  $ source env/py27/bin/activate

Then uprade setuptools and pip and install the develop requirements as
described above.

.. note::

   The following commands work only if you have the virtualenv activated.

Running the tests
-----------------

You can run the tests using `py.test`_::

  $ py.test

To generate test coverage information as HTML do::

  $ py.test --cov --cov-report html

You can then point your web browser to the ``htmlcov/index.html`` file
in the project directory and click on modules to see detailed coverage
information.

.. _`py.test`: http://pytest.org/latest/

Various checking tools
----------------------

flake8_ is a tool that can do various checks for common Python
mistakes using pyflakes_, check for PEP8_ style compliance and
can do `cyclomatic complexity`_ checking. To do pyflakes and pep8
checking do::

  $ flake8 more.basicauth

To also show cyclomatic complexity, use this command::

  $ flake8 --max-complexity=10 more.basicauth

Tox
---

With tox you can test Morepath under different Python environments.

We have Travis continuous integration installed on Morepath's github
repository and it runs the same tox tests after each checkin.

First you should install all Python versions which you want to
test. The versions which are not installed will be skipped. You should
at least install Python 3.5 which is required by flake8, coverage and
doctests and Python 2.7 for testing Morepath with Python 2.

One tool you can use to install multiple versions of Python is pyenv_.

To find out which test environments are defined for Morepath in tox.ini run::

  $ tox -l

You can run all tox tests with::

  $ tox

You can also specify a test environment to run e.g.::

  $ tox -e py35
  $ tox -e pep8
  $ tox -e coverage


.. _github: https://help.github.com/articles/generating-an-ssh-key
.. _virtualenv: https://pypi.python.org/pypi/virtualenv
.. _flake8: https://pypi.python.org/pypi/flake8
.. _pyflakes: https://pypi.python.org/pypi/pyflakes
.. _pep8: http://www.python.org/dev/peps/pep-0008/
.. _`cyclomatic complexity`: https://en.wikipedia.org/wiki/Cyclomatic_complexity
.. _pyenv: https://github.com/yyuu/pyenv
