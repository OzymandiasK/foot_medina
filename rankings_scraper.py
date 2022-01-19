from typing import List
from unicodedata import name
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager


def go_to_website():
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options)
    driver.get(
        "https://www.lffs.eu/competitions-bruxelles-brabant-wallon/?season_id=5&organization_id=1&start_date=2022-01-17&end_date=2022-01-23&serie_id=468&serie_tab=ranking"
    )

    WebDriverWait(driver, timeout=20).until(
        lambda d: d.find_element(
            by="xpath",
            value="/html/body/div[3]/div/div/div/div/article/div/div/div/div[2]/div/div/div[2]/div[2]/div/div/div/div/table/thead/tr/th[1]",
        )
    )
    return driver


# rankings = driver.find_element(by="xpath", value='//*[@id="__BVID__740"]')
def scrape_rankings_headers() -> List:
    driver = go_to_website()
    ls_headers = []
    for col in range(1, 11):
        header = driver.find_element(
            by="xpath",
            value=f"/html/body/div[3]/div/div/div/div/article/div/div/div/div[2]/div/div/div[2]/div[2]/div/div/div/div/table/thead/tr/th[{col}]",
        ).text
        ls_headers.append(header)
    driver.quit()
    return ls_headers


def scrape_rankings_data() -> List:
    driver = go_to_website()
    ls_rankings_data = []
    for row in range(1, 13):
        for col in range(1, 11):
            cell = driver.find_element(
                by="xpath",
                value=f"/html/body/div[3]/div/div/div/div/article/div/div/div/div[2]/div/div/div[2]/div[2]/div/div/div/div/table/tbody/tr[{row}]/td[{col}]",
            ).text
            ls_rankings_data.append(cell)
    driver.quit()
    return ls_rankings_data


def ls_to_df(ls_headers, ls_rankings_data):
    df = pd.DataFrame()
    for i, element in enumerate(ls_headers):
        df[element] = pd.Series(ls_rankings_data[i :: len(ls_headers)])
    try:
        df = df.set_index("#")
    except:
        pass
    return df


if __name__ == "__main__":
    headers = scrape_rankings_headers()
    rankings_data = scrape_rankings_data()
    rankings_df = ls_to_df(headers, rankings_data)
    rankings_df.to_csv("ranking.csv", sep=";")
