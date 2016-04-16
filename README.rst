more.basicauth: HTTP Basic Authentication integration for Morepath
==================================================================


Overview
--------

This is a Morepath_ authentication extension for HTTP Basic Authentication.
It was originally part of Morepath, but because it's not really the best choice,
we decide to extract in in a separate extension.

Some Pros and Cons:

*  This argues against basic auth: http://adrianotto.com/2013/02/why-http-basic-auth-is-bad
*  But this argues *for* basic auth: https://www.rdegges.com/2015/why-i-love-basic-auth

Alternative authentication extensions for morepath are:

* `more.jwtauth`_, a token based authentication system using JSON Web Token (JWT)
* `more.isdangerous`_, a cookie based identity policy using isdangerous.

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

For the login code, as ``remember_identity`` is not an option, you can just check the password::

    # check whether user has password, using password hash and database
    if not user_has_password(username, password):
        return "Sorry, login failed" # or something more fancy


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


The login form could just be::

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
-  morepath (>= 0.13.2)
