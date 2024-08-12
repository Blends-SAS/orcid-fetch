# Overview

This Python package is designed to retrieve the ORCID (Open Researcher and Contributor ID) of an author by using multiple methods to ensure accuracy. It takes the author's full name
and optionally a DOI (Digital Object Identifier) of a publication, or the author's affiliation to increase the chances of finding the correct ORCID. The program first attempts to match the provided details with records in the OpenAlex database, where it looks for ORCID information linked to the author. If multiple matches are found, it further refines the search by comparing details such as the author's co-authors and affiliations to find the best match.

The program employs a step-by-step approach, starting with the most reliable matching method (like directly matching a DOI) and proceeding to less direct methods if needed. The program assigns a confidence level to the match (e.g., "High," "Medium," or "Low") and reports the method used to achieve the result. This layered approach ensures that even if the most straightforward matching methods fail, the program can still provide a reliable ORCID based on other available information.

Right now, the program matches the author to his ORCID with a success rate of 77%. Among this matches more than 70%  are high confidence matches. It is hightly advised to always provide a DOI and a affiliation in order to increase the changes of finding the right ORCID with the most realiable methods.

# Instalation guide

This package is avaliable in PyPI. You can easily install it by running

```
pip install orcidfetch
```

## Steps

###  1. Querying OpenAlex Database

The function first queries the OpenAlex database, a comprehensive and open catalog of scholarly authors and their works, using the author’s name.
The search returns a list of possible author matches, including their ORCID if available, along with other relevant information such as affiliations and the number of works published by each author.

### 2. Filtering Results

The function filters out any authors from the OpenAlex results who do not have an ORCID.
If no authors with ORCIDs are found, the function returns None, indicating that no match could be made.

### 3. Matching Using ORCID API

For each author who has an ORCID in the filtered results, the function attempts to verify the match using the ORCID API. This is the most reliable method as it directly checks the ORCID database.
DOI Matching: It checks if the provided DOI matches any of the works associated with the ORCID. If a match is found, the ORCID is returned with a "High" confidence level.
Affiliation Matching: If no DOI match is found, the function checks if the provided affiliation matches any of the affiliations associated with the ORCID. If a match is found, it is returned with a "High" confidence level.
Fallback: If neither a DOI nor an affiliation match is found, the function moves to less reliable methods.

### 4. Crossref API collaborator Matching

If the ORCID API fails to provide a match, the function attempts to find a collaborator of the author using the provided DOI. It uses Crossref API to compare the co-authors of the work associated with the DOI to the list of possible authors from OpenAlex. If a match is found through this method, the ORCID is returned with a "High" confidence level.

### 5. Affiliation Matching Without ORCID API

If the DOI or collaborator match fails, the function tries to match the author based on their affiliation by comparing it with the affiliations of the authors in the OpenAlex results.
If one author clearly matches, the ORCID is returned with "Medium" confidence. If multiple authors match, the author with the most works is chosen, but the confidence level is lower.

### 6. Final Fallback to OpenAlex

Last Resort: If all else fails, the function simply returns the ORCID of the most likely author from OpenAlex, with a "Low" confidence level. This ensures that the program will almost always returns a result if any possible ORCID is found, but it signals that the result might not be reliable.


# Example of usage


```
from orcidfetch import Orcid

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
