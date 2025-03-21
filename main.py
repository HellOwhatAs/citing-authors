import json
from typing import Optional, List, Tuple, Dict, Union
import pandas as pd
from tqdm import tqdm
from collections import defaultdict
from doi2author import shelved_doi2author
from doi2citing import shelved_doi2citing
from name2titles import name_tuple, nametup2title
import glob


def names2names(
    names: List[Dict[str, Union[str, List[Dict[str, str]]]]],
) -> Optional[str]:
    res = []
    for name in names:
        name_str = "{} {}".format(
            name.get("given", "").strip(), name.get("family", "").strip()
        ).strip()

        affiliation = name.get("affiliation", [])
        if affiliation:
            affiliation = " ".join(i["name"] for i in affiliation if "name" in i)
            name_str = f"{name_str} ({affiliation})"

        if name_str:
            res.append(name_str)
    return "; ".join(res) if res else None


if __name__ == "__main__":
    df = pd.read_excel("./dblpnew.xlsx")
    pbar = tqdm(df["doi"])
    citing_dois_set = set()
    for doi in pbar:
        if not isinstance(doi, str):
            continue
        doi = doi.strip()

        citings = shelved_doi2citing(doi)
        if citings is None:
            continue

        citing_dois_set.update((citing, doi) for citing in citings)

    citing_dois: List[Tuple[str, str]] = sorted(citing_dois_set)

    nametup2titles = nametup2title(paths=glob.glob("./名单/*.csv"))

    res = defaultdict(lambda: (set(), defaultdict(list)))

    pbar = tqdm(citing_dois)
    for doi, original_doi in pbar:
        authors = shelved_doi2author(doi)
        if authors is None:
            continue

        for name in authors:
            name_str = "{} {}".format(
                name.get("given", "").strip(), name.get("family", "").strip()
            )

            title = nametup2titles.get(name_tuple(name_str), None)
            if title is not None:
                res[name_str][0].add(title)
            res[name_str][1][doi].append(original_doi)

    with open("res.json", "w", encoding="utf-8") as f:
        json.dump(
            {k: (list(title), doi_dict) for k, (title, doi_dict) in res.items()},
            f,
            ensure_ascii=False,
            indent=4,
        )
