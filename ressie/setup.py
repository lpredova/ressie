from setuptools import setup

setup(name='ressie',
      version='0.1.0',
      packages=['ressie'],
      entry_points={
          'console_scripts': [
              'ressie = ressie.__main__:main'
          ]
      }, requires=['mailgun2', 'slackclient', 'requests', 'whoosh', 'elasticsearch>=5.0.0,<6.0.0', 'pymysql']
      )
