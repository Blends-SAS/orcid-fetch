
from orcidfetch.oricd import Orcid


def test_get_orcid():

    search = Orcid(author_name='Manu forero', doi = "10.3390/mps2030056")
    assert search.orcid == '0000-0002-7989-0311'
    search = Orcid(author_name='Manu forero', affiliation= 'Uniandes')
    assert search.orcid == '0000-0002-7989-0311'

