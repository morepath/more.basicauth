import io
from setuptools import setup, find_packages

long_description = (
    io.open('README.rst', encoding='utf-8').read() + '\n' +
    io.open('CHANGES.rst', encoding='utf-8').read())

setup(
    name='more.basicauth',
    version='0.1',
    description="Basic Auth Identity Policy for Morepath",
    long_description=long_description,
    author="Henri Hulski",
    author_email="henri.hulski@gazeta.pl",
    keywords='morepath basicauth identity authentication',
    license="BSD",
    url="https://github.com/morepath/more.basicauth",
    namespace_packages=['more'],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
      "Development Status :: 4 - Beta",
      "Environment :: Web Environment",
      "Intended Audience :: Developers",
      "License :: OSI Approved :: BSD License",
      "Operating System :: OS Independent",
      "Programming Language :: Python",
      "Programming Language :: Python :: 2.7",
      "Programming Language :: Python :: 3",
      "Programming Language :: Python :: 3.3",
      "Programming Language :: Python :: 3.4",
      "Programming Language :: Python :: 3.5",
      "Topic :: Internet :: WWW/HTTP",
      "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
      "Topic :: Internet :: WWW/HTTP :: WSGI",
      "Topic :: Software Development :: Libraries :: Application Frameworks",
      "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=[
      'setuptools',
      'morepath >= 0.13.2',
    ],
    extras_require=dict(
      test=['pytest >= 2.9.1',
            'pytest-cov',
            'WebTest'],
    ),
)
