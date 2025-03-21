import shelve
from crossref.restful import Works
from typing import Optional, List, Union, Dict

works = Works()


def doi2author(doi: str) -> Optional[List[Dict[str, Union[str, List[Dict[str, str]]]]]]:
    try:
        res: dict = works.doi(doi)
        authors = res.get("author", [])
        return authors
    except Exception:
        return None


def shelved_doi2author(
    doi: str, fname: str = "doi2author"
) -> Optional[List[Dict[str, Union[str, List[Dict[str, str]]]]]]:
    with shelve.open(fname) as db:
        cur = db.get(doi, None)
        if cur is None:
            cur = doi2author(doi)
            db[doi] = cur
    return cur
