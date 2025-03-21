import pandas as pd
from typing import List, Tuple, Dict
from more_itertools import flatten


def name_tuple(name: str, is_chinese: bool = False) -> Tuple[str, ...]:
    if is_chinese:
        if len(name.split()) == 3:
            name = "{}{} {}".format(*name.split())
        else:
            return ""
    return tuple(
        sorted(
            set(
                name.replace("Prof.", "")
                .replace("Dr.", "")
                .replace("Professor", "")
                .replace("HonFREng", "")
                .replace("HonFRS", "")
                .replace("FREng", "")
                .replace("FRS", "")
                .replace("Mr", "")
                .replace("Emeritus", "")
                .replace("Ms", "")
                .replace("Air", "")
                .replace("Chief", "")
                .replace("Marshal", "")
                .replace("Sir", "")
                .replace("Dr", "")
                .replace("FRSE", "")
                .replace("Mrs", "")
                .lower()
                .strip()
                .replace(",", " ")
                .replace("\xa0", " ")
                .replace("(", " ")
                .replace(")", " ")
                .split()
            )
        )
    )


def nametup2title(paths: List[str]) -> Dict[Tuple[str, ...], str]:
    dfs: Dict[str, List[str]] = {
        path: pd.read_csv(path)["name"].to_list() for path in paths
    }

    return dict(
        flatten(
            ((name_tuple(row, is_chinese="中国" in title), title) for row in series)
            for title, series in dfs.items()
        )
    )


if __name__ == "__main__":
    import glob

    print(nametup2title(paths=glob.glob("./名单/*")))
