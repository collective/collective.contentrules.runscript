from setuptools import setup, find_packages
import os

version = '0.5'

setup(name='collective.contentrules.runscript',
      version=version,
      description="An action for the contentrules framework to run a script on the object that triggered the rule",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone contentrules action addon',
      author='Danilo G. Botelho',
      author_email='danilogbotelho@yahoo.com',
      url='http://plone.org/products/collective.contentrules.runscript',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective', 'collective.contentrules'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      extras_require = {
          'test': [
                  'plone.app.testing',
              ]
      },
      )
