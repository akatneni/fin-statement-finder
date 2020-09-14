from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as expected_conditions
import app.config
#

lastCIK=0

def getTable(CIK,page):
    #CIK=1326801
    global lastCIK
    if CIK=="":
        CIK=lastCIK
    lastCIK=CIK
    url=f"https://www.sec.gov/cgi-bin/browse-edgar?CIK={CIK}&type=10-K&dateb=&owner=include&count=40"
    options = Options()
    options.headless = True
    #url = "https://www.sec.gov/cgi-bin/viewer?action=view&cik=1326801&accession_number=0001326801-20-000013&xbrl_type=v#"
    driver = webdriver.Remote(command_executor=app.config.ec2_address, options=options)
    #driver=webdriver.Chrome(options=options)
    driver.get(url)
    try:
        WebDriverWait(driver,10).until(expected_conditions.title_is("EDGAR Search Results"))
        driver.find_element_by_id("interactiveDataBtn").click()
    except:
        return "<h1>Invalid CIK Value</h1>"
    WebDriverWait(driver,10).until(expected_conditions.title_is("View Filing Data"))
    # print(rows[0].get_attribute("href"))
    # rows[0].trigger("click")
    driver.execute_script(f"loadReport({page});")
    elem = driver.find_element_by_id("reportDiv").get_attribute("innerHTML")
    driver.quit()
    return elem
