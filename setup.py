from setuptools import setup

setup(
   name='bot',
   version='1.0',
   description='Discord Bot',
   author='AlexandreSenpai',
   author_email='alexandrebsramos@hotmail.com',
   packages=['bot'],  #same as name
   install_requires=['discord.py', 'discord.py[voice]', 'python-dotenv'], #external packages as dependencies
   scripts=[]
)