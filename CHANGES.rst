CHANGES
*******

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
