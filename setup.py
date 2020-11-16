from setuptools import setup, find_packages

# pyinstaller -F --name SqlDiff --icon=gui\resources\icons\sql_diff_program_icon.ico main.py

setup(name='sql_diff',
      version='0.1.0',
      packages=find_packages()
)