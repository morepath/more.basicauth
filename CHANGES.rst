CHANGES
*******

1.0.0 (unreleased)
------------------

- Add type annotations and integrate ``mypy`` and ``pyright``.

- Switch to ``pyproject.toml`` based project setup.

- Switch to ``src-layout`` based file structure.

- Switch to native namespace package defined in PEP 420.

- Add support for Python 3.11 - 3.15.

- Drop support for Python below 3.11.

- Support Pypy 3.12.

- Add tests for 100% coverage.

- Switch from black, flake8, isort and pyupgrade to Ruff_ linter and formatter.

  .. _Ruff: https://docs.astral.sh/ruff

- Replace ``pre-commit`` integration with our custom tracked
  pre-commit git hook for Ruff checks on staged Python files.

- Fix linting and formatting errors.

- Update ``README.rst``.

- Remove coveralls integration.

- Use GitHub Actions for CI.

- Adjust the deployment strategy:

  * Move the Pypi upload from ``zest.release`` to ``gh-actions``.

  * Use ``v`` + version as release tags like ``v1.0.0``.

  * So we still use ``zest.release`` but without publishing to Pypi.
    The Pypi upload is triggered by pushing the new release tag to GitHub.
    This happens in the Release workflow in ``.github/workflows/release.yml``.
    With this workflow we get Trusted Publishing with short-lived OIDC tokens
    that PyPI issues to one specific repository, workflow file and environment (``pypi``).
    We also get PEP 740 provenance and can set required reviewers for the environment
    and a ruleset who can create release tags and trigger releases.

- Make an overall cleanup.


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
