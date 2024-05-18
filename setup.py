from setuptools import setup, find_packages
from typing import List

HYPEN_E_DOT = '-e .'

def get_requirements(file_path: str) ->List[str]:
    '''
    This function will return the list of dependencies for the project.
    '''
    requirements=[]

    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
    
    requirements=[req.replace("\n","") for req in requirements]

    if HYPEN_E_DOT in requirements:
        requirements.remove(HYPEN_E_DOT)

    return requirements

setup(
    name='First end to end project',
    version='1.0.0',
    author='Karan Sharma',
    author_email='mekaransharma18@gmail.com',
    description='My first end to end project',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)
