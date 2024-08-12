# Overview

The Orcid class takes an author's name, DOI (Digital Object Identifier), and affiliation to attempt to find the author's ORCID. It employs a multi-step process, using external APIs like Orcid API, OpenAlex and CrossRef, to provide a confidence score and the method used to identify the author's ORCID.

Note: The reliability of the search is greatly increased by providing a DOI and a affiliation of an author, even though they are optional parameters it is highly encuraged to provide them. 


# Example of usage


```
from NAME_OF_THE_PACKAGE import Orcid

# Initialize with author name and additional information
results = Orcid(
    author_name="Jane Smith",
    doi="10.5678/example-doi", # Optional
    affiliation= "OpenAI Research Lab"] # Optional
)

# Print the results
print(results)

# Access specific attributes
print("ORCID:", results.orcid)
print("Confidence Level:", results.confidence)
print("Search Method:", results.method)
print("Execution Time:", results.time, "seconds")

```


# Attributes

The Orcid class has several attributes that store the results of the search:

author_name: The name of the author being searched for.\
doi: The DOI of the author's work (optional).\
affiliation: An affiliation associated with the author (optional).\
orcid: The ORCID ID of the author if found.\
confidence: The confidence level of the ORCID match (e.g., 'High', 'Medium', 'Low').\
method: The method used to find the ORCID ID (e.g., 'orcid API match', 'collaborator match').\
time: The execution time for the search.\



# Methods

The Orcid class provides a clean and human-readable representation of its attributes:

```
__repr__(): Returns a detailed string representation of the Orcid object, suitable for debugging.
__str__(): Returns a user-friendly string representation of the Orcid object, outlining the available attributes and their values.
```
