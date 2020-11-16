from setuptools import setup, find_packages

# pyinstaller -F --name SqlDiff --icon=gui\resources\icons\sql_diff_program_icon.ico --noupx main.spec

setup(name='sql_diff',
      version='0.0.1',
      packages=find_packages()
)