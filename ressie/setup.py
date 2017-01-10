from setuptools import setup

setup(name='ressie',
      version='0.1.0',
      packages=['project'],
      entry_points={
          'console_scripts': [
              'project = project.__main__:main'
          ]
      },
      )


#https://chriswarrick.com/blog/2014/09/15/python-apps-the-right-way-entry_points-and-scripts/