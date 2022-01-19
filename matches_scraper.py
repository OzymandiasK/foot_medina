from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.firefox import GeckoDriverManager
from pathlib import Path


def matches_to_csv():
    cwd = str(Path.cwd())

    options = Options()

    firefox_profile = FirefoxProfile()

    firefox_profile.set_preference("browser.download.folderList", 2)
    firefox_profile.set_preference("browser.download.manager.showWhenStarting", False)
    firefox_profile.set_preference("browser.download.dir", cwd)
    firefox_profile.set_preference(
        "browser.helperApps.neverAsk.openFile",
        "text/csv,application/x-msexcel,application/excel,application/x-excel,application/vnd.ms-excel,image/png,image/jpeg,text/html,text/plain,application/msword,application/xml",
    )
    firefox_profile.set_preference(
        "browser.helperApps.neverAsk.saveToDisk",
        "text/csv,application/x-msexcel,application/excel,application/x-excel,application/vnd.ms-excel,image/png,image/jpeg,text/html,text/plain,application/msword,application/xml",
    )
    firefox_profile.set_preference("browser.helperApps.alwaysAsk.force", False)
    firefox_profile.set_preference("browser.download.manager.alertOnEXEOpen", False)
    firefox_profile.set_preference("browser.download.manager.focusWhenStarting", False)
    firefox_profile.set_preference("browser.download.manager.useWindow", False)
    firefox_profile.set_preference("browser.download.manager.showAlertOnComplete", False)
    firefox_profile.set_preference("browser.download.manager.closeWhenDone", True)

    # options.headless = True
    options.profile = firefox_profile

    driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=options)
    driver.get(
        "https://www.lffs.eu/competitions-bruxelles-brabant-wallon/?season_id=5&organization_id=1&start_date=2022-01-17&end_date=2022-01-23&serie_id=468&serie_tab=fullCalendar"
    )

    WebDriverWait(driver, timeout=20).until(
        lambda d: d.find_element(by="xpath", value='//*[@id="__BVID__620___BV_tab_button__"]')
    )

    full_calendar_tab = driver.find_element(
        by="xpath", value='//*[@id="__BVID__620___BV_tab_button__"]'
    )
    full_calendar_tab.click()

    dl_button = driver.find_element(
        by="xpath",
        value="/html/body/div[3]/div/div/div/div/article/div/div/div/div[2]/div/div/div[2]/div[3]/div/div/div/div[1]/div/table/thead/tr/th[12]/div/button",
    )
    dl_button.click()
    driver.quit()


if __name__ == "__main__":
    matches_to_csv()
