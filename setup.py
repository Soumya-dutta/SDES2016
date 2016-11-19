import sys
import subprocess
from setuptools import setup, find_packages

requires = ["numpy", "sympy", "control", "matplotlib"]
subprocess.call(["sudo", "apt-get", "install", "python-tk"])

setup(
      name='Circuit_Control_Parameters',
      version='0.1',
      description='Control Parameters of any circuit',
      url='https://bitbucket.org/sdes2016/circuit_control_parameters',
      author='Soumya Dutta, Aveek Podder',
      author_email='soumya.besuee@gmail.com, questions54@gmail.com',
      license='GPL3',
      install_requires=requires,
      packages=find_packages(),
      )
