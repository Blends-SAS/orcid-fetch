from setuptools import find_packages, setup

setup(
    name='orcidfetch',
    packages=find_packages(include=['orcidfetch']),
    version='0.1',
    description="The Orcid class takes an author's name, DOI (Digital Object Identifier), and affiliation to attempt to find the author's ORCID ID. It employs a multi-step process, using external APIs like Orcid API, OpenAlex and CrossRef, to provide a confidence score and the method used to identify the author's ORCID.",
    author='Juan Camilo Lopez',
    install_requires=['requests', 'pyalex', 'crossrefapi', 'Unidecode'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests'
)