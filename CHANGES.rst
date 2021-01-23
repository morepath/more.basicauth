CHANGES
*******

0.6 (unreleased)
================

- Fix Flake8.

- Drop support for Python 3.4 and 3.5.

- Add support for Python 3.9.

- Use GitHub Actions for CI.


0.5 (2020-04-26)
================

- **Removed**: Removed support for Python 2.
  
  You have to upgrade to Python 3 if you want to use this version.

- Dropped support for Python 3.3 and added support for Python 3.5, 3.6, 3.7 and PyPy 3.6.

- Make Python 3.7 the default testing environment.

- Add integration for the Black code formatter.


0.4 (2016-10-21)
================

- We now use virtualenv and pip instead of buildout to set up the
  development environment. A development section has been
  added to the README accordingly.


0.3 (2016-07-20)
================

- Upgrade to Morepath 0.15.
- Add testenv for Python 3.5 and make it the default test environment.
- Change author to "Morepath developers".
- Clean up classifiers.


0.2 (2016-04-25)
================

- Upgrade to Morepath 0.14.
- Some minor improvements to the buildout setup workflow.


0.1 (2016-04-16)
================

- Extract Basic Auth from Morepath.
- Return NO_IDENTITY instead of None, if user cannot identify.
- Replace class 'app' with 'App' in tests.
- Add a login test.
- Enhance documentation.
