from setuptools import setup

setup(name='ressie',
      version='0.1.0',
      packages=['ressie'],
      entry_points={
          'console_scripts': [
              'ressie = ressie.__main__:main'
          ]
      },
      )


#https://chriswarrick.com/blog/2014/09/15/python-apps-the-right-way-entry_points-and-scripts/