import shelve
import requests
from typing import List, Optional


def doi2citing(doi: str) -> Optional[List[str]]:
    """
    Input: doi of a paper
    Output: list of dois citing the paper
        or None if Exception occurs
    """
    try:
        resp = requests.get(
            f"https://opencitations.net/index/coci/api/v1/citations/{doi}"
        )
        result = []
        for i in resp.json():
            citing = i.get("citing", None)
            if citing is None:
                continue
            result.append(citing)

        return result
    except Exception:
        return None


def shelved_doi2citing(doi: str, fname: str = "doi2citing") -> Optional[List[str]]:
    with shelve.open(fname) as db:
        cur = db.get(doi, None)
        if cur is None:
            cur = doi2citing(doi)
            db[doi] = cur
    return cur


if __name__ == "__main__":
    doi = "10.1109/TNET.2023.3294803"
    print(doi2citing(doi))
