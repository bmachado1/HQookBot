from selenium import webdriver
from selenium.webdriver.common.keys import Keys

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--incognito")

driver = webdriver.Chrome('C:\\Program Files (x86)\\Google\\chromedriver_win32\\chromedriver.exe',chrome_options=chrome_options)  # Optional argument, if not specified will search path.
driver.get('https://www.textnow.com/signup')

elem = driver.find_elements_by_name("email")[1]
elem.send_keys("NadiaLenterb@gmail.com")

elem = driver.find_elements_by_name("password")[1]
elem.send_keys("ofcouseima12345gooddd")



