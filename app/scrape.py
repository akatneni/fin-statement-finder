from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC

ERROR_MESSAGE="<h1>CIK cannot be found!</h1>"
DEFAULT_WAIT=5

def getTable(CIK,page):

    url=f"https://www.sec.gov/cgi-bin/browse-edgar?CIK={CIK}&type=10-K&dateb=&owner=include&count=40"
    options = Options()
    options.add_argument("—-disable-gpu")
    options.add_argument("—-no-sandbox")
    options.headless = True
    driver = webdriver.Chrome(options=options)
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
