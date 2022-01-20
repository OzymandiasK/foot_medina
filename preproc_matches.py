import pandas as pd
import numpy as np


def preproc_matches_df():
    matches = pd.read_excel("data.xlsx", engine="openpyxl")
    matches.drop(columns=["Serie", "Num.", "Jour"])
    matches = matches.convert_dtypes()
    matches = matches.rename(columns={"Visités": "Domicile", "Visiteurs": "Extérieur"})
    return matches


def week_number_column(matches):
    matches["week_number"] = matches["Date"].dt.week
    matches["week_number"] = matches["week_number"].apply(
        lambda x: x + 52 if x < matches.loc[0, "week_number"] else x
    )
    matches["week_number"] = matches["week_number"].apply(lambda x: x - 34)
    return matches["week_number"]


def pts_repartition_for_each_match_df(matches_df):
    home_win = matches_df["Score Home"] > matches_df["Score Away"]
    draw = matches_df["Score Home"] == matches_df["Score Away"]
    home_lose = matches_df["Score Home"] < matches_df["Score Away"]

    # Make sure that the conditions are of type np.array and boolean
    conditions = [
        np.array(home_win, dtype=bool),
        np.array(draw, dtype=bool),
        np.array(home_lose, dtype=bool),
    ]
    choices = [2, 1, 0]
    matches_df["PTS_home"] = np.select(conditions, choices, default=np.nan)
    matches_df["PTS_away"] = np.select(conditions, choices[::-1], default=np.nan)
    return matches_df[["PTS_home", "PTS_away"]]


def matches_played_df(matches):
    ls_teams = matches["Domicile"].unique()
    matches_played = pd.DataFrame(
        index=ls_teams, data=[[0, 0]], columns=["PTS", "matches_played"]
    )
    return matches_played


def ranking_through_time():
    matches = preproc_matches_df()
    matches = matches.dropna()
    matches.drop(columns=["Salle", "Heure", "Arbitre"])
    matches["week_number"] = week_number_column(matches)
    matches[["PTS_home", "PTS_away"]] = pts_repartition_for_each_match_df(matches)

    ls_teams = matches["Domicile"].unique()
    ranking_timeline_df = pd.DataFrame(
        index=ls_teams, columns=(np.insert(matches["week_number"].unique(), 0, 0))
    )
    ranking_timeline_df.iloc[:, 0] = 0
    matches_played = matches_played_df(matches)

    for row in matches.iterrows():

        home_team = row["Domicile"]
        away_team = row["Extérieur"]
        pts_this_match_home = row["PTS_home"]
        pts_this_match_away = row["PTS_away"]

        matches_played.at[home_team, "PTS"] += pts_this_match_home
        matches_played.at[away_team, "PTS"] += pts_this_match_away

        matches_played.at[home_team, "matches_played"] += 1
        matches_played.at[away_team, "matches_played"] += 1

        ranking_timeline_df.at[
            home_team, matches_played.at[home_team, "matches_played"]
        ] = matches_played.at[home_team, "PTS"]

        ranking_timeline_df.at[
            away_team, matches_played.at[away_team, "matches_played"]
        ] = matches_played.at[away_team, "PTS"]

    ranking_timeline_df = ranking_timeline_df.fillna(method="ffill", axis=1)

    return ranking_timeline_df


if __name__ == "__main__":
    preproc_matches_df()
