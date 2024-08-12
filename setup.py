from setuptools import find_packages, setup
import os

# Read the README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='orcidfetch',
    packages=find_packages(include=['orcidfetch']),
    version='0.2',
    description="The Orcid class takes an author's name, DOI (Digital Object Identifier), and affiliation to attempt to find the author's ORCID ID. It employs a multi-step process, using external APIs like Orcid API, OpenAlex and CrossRef, to provide a confidence score and the method used to identify the author's ORCID.",
    author='Juan Camilo Lopez',
    install_requires=['requests', 'pyalex', 'crossrefapi', 'Unidecode'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
    long_description=long_description,
    long_description_content_type='text/markdown'

)