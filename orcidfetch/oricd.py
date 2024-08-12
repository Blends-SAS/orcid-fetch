from typing import List, Dict, Any, Optional
from pyalex import Authors
import os
import time
import requests
from typing import List, Dict, Optional
import difflib
from crossref.restful import Works
from pyalex import Works as OAWorks
import time
from unidecode import unidecode
import logging


import logging

# Set the logging level to DEBUG
logging.basicConfig(level=logging.INFO)


# MEMBER TOKEN
auth = {'access_token': 'e2e455e1-8fc3-4fbf-aad5-9b7d8891e7dc',
 'token_type': 'bearer',
 'refresh_token': 'a63b7578-d587-46b8-9019-85fb2a8eb52b',
 'expires_in': 631138518,
 'scope': '/read-public',
 'orcid': None}


# PUBLIC TOKEN
# auth = {'access_token': '791c6a8a-f2f4-4d75-a932-59826063c71b',
#  'token_type': 'bearer',
#  'refresh_token': '674dcb57-1e6d-4ad5-b3ec-c440ac86cf51',
#  'expires_in': 631138518,
#  'scope': '/read-public',
#  'orcid': None}


# Fetch works of a record
def orcid_search_works(orcid_id):
    # ORCID API endpoint for the record in XML format
    url = f"https://pub.orcid.org/v3.0/{orcid_id}/works"

    # Headers for the request
    headers = {
        "Accept": "application/vnd.orcid+json",
        "Authorization": f"Bearer {auth['access_token']}"  # Bearer token authentication
    }

    # Make the GET request
    response = requests.get(url, headers=headers)


    if response.status_code == 200:
        return(response.json())
    else:
        logging.info(f"Error {response.status_code}: {response.json()}")


# Fetch works of a record
def orcid_search(orcid_id):
    # ORCID API endpoint for the record in XML format
    url = f"https://pub.orcid.org/v3.0/{orcid_id}"

    # Headers for the request
    headers = {
        "Accept": "application/vnd.orcid+json",
        "Authorization": f"Bearer {auth['access_token']}"  # Bearer token authentication
    }
    # Make the GET request
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return(response.json())
    else:
        logging.info(f"Error {response.status_code}: {response.json()}")


# _ = orcid_search('0000-0002-7989-0311')

# dois = [external_id['external-id-value'] for work in _['activities-summary']['works']['group'] for  external_id in work['external-ids']['external-id'] if external_id['external-id-type'] == 'doi']
# employments = [organization['employment-summary']['organization']['name'] for item in _['activities-summary']['employments']['affiliation-group'] for organization in item['summaries'] ]
# education = [organization['education-summary']['organization']['name'] for item in _['activities-summary']['educations']['affiliation-group'] for organization in item['summaries'] ]

    


def name_processing(df):

    # Simple joining

    processed = df
    #Simple joining + delete special characters and accents
    def f(str_in):
        str_in = str(str_in)
        str_in = str_in.replace('-',  ' ')
        str_in = unidecode(str_in)
        return str_in

    processed = processed.apply(lambda x: f(x))

    return processed


def search_openalex_info(author_name: str)-> List[Dict]:
    res = Authors().search_filter(display_name=author_name).get()
    raw_results = []

    if res:
        for idx,author in enumerate(res):
            orcid = author['orcid']
            display_name = author['display_name']
            display_name_alternatives = author['display_name_alternatives']
            num_works = author['works_count']
            openalex_id = author['id']
            
            try:
                affiliations = [{"name": x['institution']['display_name'], "country_code": x['institution']['country_code']} for x in author["affiliations"]]
            except KeyError:
                affiliations = None

            raw_results.append({'name': author_name, 'result_rank': idx + 1, 'orcid': os.path.split(orcid)[-1] if orcid is not None else None,
                        'display_name': display_name, 'display_name_alternatives': display_name_alternatives, 'affiliations': affiliations, 'num_works': num_works, 'id': openalex_id})
                
        _ = [item for item in raw_results if item['orcid'] is not None]                

        return raw_results
    else:
        return None
    

def find_affiliation_match(author_affiliations: List[Dict], target_affiliation: str) -> bool:
    if not author_affiliations or not target_affiliation:
        return False

    target_affiliation = str(target_affiliation).lower()

    for aff in author_affiliations:
        aff_name = str(aff['name']).lower()
        if target_affiliation in aff_name:
            return True
        
        # Using difflib to find close matches
        match_ratio = difflib.SequenceMatcher(None, target_affiliation, aff_name).ratio()
        if match_ratio > 0.65:  # Adjust threshold as needed
            return True

    return False


def clean_name(name: str) -> str:
    """
    Helper function to clean and normalize author names.
    Removes middle initials and converts to lower case for comparison.
    """
    name_parts = name.split()
    if len(name_parts) > 2:
        # Assume the format is 'First M. Last' and remove the middle initial
        name = ' '.join([name_parts[0], name_parts[-1]])
    return name.lower()



def find_collaborator_match(doi: str, target_author: str, possible_authors: List[Dict]) -> Optional[str]:
    # Get all co-authors for the DOI
    works = Works()



    works_results = works.doi(doi)
    if works_results is None:
        logging.info(f' doi provided did not return results on crossref API')
        return None
    

    
    co_authors = works_results['author']
    target_author_clean = clean_name(target_author)
    
    try:
        # Remove target_author from list of coauthors
        co_authors = [co_author for co_author in co_authors if clean_name(co_author['given'] + ' ' + co_author['family']) != target_author_clean]
        
        # Get all of the authors that contributed to papers of this entry
        # Loop through each possible_authors, see the co-authors of their works and see if there is any match
        for possible_author in possible_authors:
            possible_author_works = OAWorks().filter(author={"id": possible_author['id']}).get()
            for possible_author_work in possible_author_works:
                for possible_coauthor in possible_author_work['authorships']:
                    possible_coauthor_name = clean_name(possible_coauthor['author']['display_name'])
                    for co_author in co_authors:
                        co_author_name = clean_name(co_author['given'] + ' ' + co_author['family'])
                        if possible_coauthor_name == co_author_name:
                            return possible_author['orcid']
    except:
        return None

    # Maybe also check for affiliation matches?
    return None
    


def XTREME_orcid_match(orcid: str, doi: str, affiliation: Optional[str]):

    def string_processing(in_str):

        # Convert the string to lowercase
        in_str = in_str.lower()
        # Replace underscores with spaces
        in_str = in_str.replace('-', ' ')
        # Remove extra spaces by splitting and joining the string
        in_str = ' '.join(in_str.split())
        return in_str

    confidence = None
    match = None
    

    try:
        _ = orcid_search(orcid)
    except Exception as e:
        logging.info(f'Error: {e}')
        return match, confidence
        

    # Try doi match
    try:
        doi_list = [external_id['external-id-value'] for work in _['activities-summary']['works']['group'] for  external_id in work['external-ids']['external-id'] if external_id['external-id-type'] == 'doi']
        #print(doi_list)
        if doi in doi_list: 

            logging.info('match with orcid doi')
            match, confidence = orcid, 'High'
            return match, confidence

    except:
        pass

    # If affiliations are not None, try matching with them
    if affiliation:

        # init affiliations list
        affiliations_found = []

        # try affiliation match
        try:
            education = [organization['education-summary']['organization']['name'] for item in _['activities-summary']['educations']['affiliation-group'] for organization in item['summaries'] ]
            # Add education to affiliations_found
            for item in education: affiliations_found.append(item)
        except: pass
        
        try:
            employments = [organization['employment-summary']['organization']['name'] for item in _['activities-summary']['employments']['affiliation-group'] for organization in item['summaries'] ]
            # Add employments to affiliations_found
            for item in employments: affiliations_found.append(item)
        except: pass

        # if we dont get any affiliation, we return None, None
        if affiliations_found == []: return match, confidence
        #print(affiliations_found)

        # str processing function

        processed_affiliations_found = [string_processing(str) for str in affiliations_found]
        processed_affiliation = string_processing(affiliation)

        if processed_affiliation in processed_affiliations_found:
                
            logging.info('match with orcid affiliations')
            match, confidence = orcid, 'High'
            return match, confidence    

        # TODO: string similarity

        for _ in processed_affiliations_found:
            similarity_ratio = difflib.SequenceMatcher(None, _, processed_affiliation).ratio()
        if similarity_ratio > 0.65:  # Adjust threshold as needed

            logging.info('match with orcid affiliations')
            match, confidence = orcid, 'High'
            return match, confidence    
        
    return match, confidence


def get_orcid(author_name: str, doi: str, affiliation: Optional[str]):


    def name_processing(str_in):
        str_in = str(str_in)
        str_in = str_in.replace('-',  ' ')
        str_in = unidecode(str_in)
        return str_in
    
    author_name = name_processing(author_name)

    confidence = None
    match = None
    method = None

    # Get data from openalex
    raw_results = search_openalex_info(author_name)
    
    if raw_results:
        # filter out authors without orcid
        filtered_results = [item for item in raw_results if item['orcid'] is not None]


        # If there are not authors with oricd we return None
        if len(filtered_results) == 0: 
            return confidence, match

                        
        # perform a search with orcid API
        for author in filtered_results:
            # Match with doi
            match, confidence = XTREME_orcid_match(orcid = author['orcid'], doi = doi, affiliation = affiliation)
            if match:
                return match, confidence, 'orcid API match'


        # Otherwise, let's try to get a DOI match
        if doi:
            collaborator_match = find_collaborator_match(doi, author_name, raw_results)
            if collaborator_match:
                logging.info('match collaborator match')
                confidence = 'High'
                return collaborator_match, confidence, 'collaborator match'
        
        # Otherwise, let's try to get affiliation match
        if affiliation:
            matching_affiliations = [author for author in raw_results if find_affiliation_match(author['affiliations'], affiliation)]

            if len(matching_affiliations) == 1:
                if matching_affiliations[0]['orcid'] is not None:
                    logging.info('match affiliation v1')
                    confidence = "Medium"
                    match = matching_affiliations[0]['orcid']
                    return match, confidence, 'affiliation match'

            elif len(matching_affiliations) > 1:
                matching_affiliations.sort(key=lambda x: x['num_works'], reverse=True)
                if matching_affiliations[0]['orcid'] is not None:
                    logging.info('match affilaiton v2')
                    confidence = 'Medium'
                    match = matching_affiliations[0]['orcid']
                    return match, confidence, 'affiliation match'
                    
        # Save best open alex results if orcid API failed
        if len(filtered_results) == 1:
            match = filtered_results[0]['orcid']
            confidence = 'Medium'
            return match, confidence, 'open alex match'
                
        if len(filtered_results)>1:
            match = filtered_results[0]['orcid']
            confidence = 'Low'
            return match, confidence, 'open alex match'
                    
    # Return the match
    return match, confidence


class Orcid:

    def __init__(self, author_name : str, doi: str = None, affiliation: str = None):

        self.author_name = author_name
        self.doi = doi
        self.affiliation = affiliation

        self.method = None

        self.time = None

        srt = time.time()
        try: 
            self.orcid, self.confidence, self.method  = get_orcid(author_name=author_name, doi=self.doi, affiliation=self.affiliation)
        except:
            raise
        end = time.time()


        self.time = round(end-srt, 2)

        pass


    def __repr__(self):
        
        return (f"Orcid(author_name={self.author_name!r}, orcid={self.orcid!r}, "
                f"affiliation={self.affiliation!r}, doi={self.doi!r}, "
                f"confidence={self.confidence!r}, method_used={self.method!r}, "
                f"execution_time={self.time!r})")

    def __str__(self):
        return (
            f"Orcid Information for {self.author_name}\n"
            "Available attributes:\n"
            " - results.orcid: Get the ORCID ID and confidence level.\n"
            " - results.confidence: Get the confidence level of search.\n"
            " - results.author_name: Get the author's name.\n"
            " - results.doi: Get the DOI used for the search.\n"
            " - results.affiliation: Get the affiliation used for the search.\n"
            " - results.time: Get the execution time.\n"
            " - results.method: Get the method used for retrieval.\n"
        )





# TEST FUNCTION FOR PIP


def test_function():

    return 'Function imported'