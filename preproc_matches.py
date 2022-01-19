import pandas as pd


def preproc_matches():
    matches = pd.read_excel("data.xlsx", engine="openpyxl")
    matches.drop(columns=["Serie", "Num.", "Jour"])
    return matches


if __name__ == "__main__":
    preproc_matches()
