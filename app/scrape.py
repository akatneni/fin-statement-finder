from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import os

GOOGLE_CHROME_PATH = '/app/.apt/usr/bin/google_chrome'
CHROMEDRIVER_PATH = "/app/.chromedriver/bin/chromedriver"
chrome_bin = os.environ.get("GOOGLE_CHROME_BIN", "chromedriver")
ERROR_MESSAGE="<h1>CIK cannot be found!</h1>"
DEFAULT_WAIT=5

def getTable(CIK,page):

    url=f"https://www.sec.gov/cgi-bin/browse-edgar?CIK={CIK}&type=10-K&dateb=&owner=include&count=40"
    options = webdriver.ChromeOptions()
    options.binary_location = chrome_bin
    options.add_argument(" — disable-gpu")
    options.add_argument(" — no-sandbox")
    options.add_argument(" — headless")
    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=options)
    #url = "https://www.sec.gov/cgi-bin/viewer?action=view&cik=1326801&accession_number=0001326801-20-000013&xbrl_type=v#"
    #driver = webdriver.Remote(command_executor=app.config.ec2_address, options=options)
    #driver=webdriver.Chrome(options=options)
    driver.get(url)
    try:
        WebDriverWait(driver,DEFAULT_WAIT).until(EC.title_is("EDGAR Search Results"))
        driver.find_element_by_id("interactiveDataBtn").click()
    except:
        return ERROR_MESSAGE
    WebDriverWait(driver,DEFAULT_WAIT).until(EC.title_is("View Filing Data"))
    reportButtons = driver.find_elements_by_class_name("xbrlviewer")
    found = False
    for b in reportButtons:
        if b.get_attribute("innerHTML") in page:
            script=b.get_attribute("href")
            driver.execute_script(script)
            found=True
    if not(found):
        return ERROR_MESSAGE
    elem = driver.find_element_by_id("reportDiv").get_attribute("innerHTML")
    driver.quit()
    return elem
