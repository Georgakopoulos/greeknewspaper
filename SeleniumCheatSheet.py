#-*- coding: utf-8 *-*

import os
import datetime
from os.path import expanduser
import json
import time
from selenium import webdriver
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException, StaleElementReferenceException, ElementNotVisibleException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import pprint

from driver_builder import DriverBuilder

pp = pprint.PrettyPrinter(indent=4)
download_dir = os.path.join(os.sep, expanduser("~"), 'Downloads')

def vpn_fox():
    profile_path=r"C:\Users\PavloLysytsya\AppData\Roaming\Mozilla\Firefox\Profiles\nsc5bj6c.default"
    profile = webdriver.FirefoxProfile(profile_path)
    # set FF preference to socks proxy
    profile.set_preference("network.proxy.type", 1)
    profile.set_preference("network.proxy.socks", "127.0.0.1")
    profile.set_preference("network.proxy.socks_port", 9050)
    profile.set_preference("network.proxy.socks_version", 5)
    profile.update_preferences()
    global driver
    driver = webdriver.Firefox(firefox_profile=profile)

def fox(download_directory):
    fp = webdriver.FirefoxProfile()
    fp.set_preference("browser.download.folderList",2)
    fp.set_preference("browser.download.manager.showWhenStarting", False)
    fp.set_preference("browser.download.dir", download_directory)
    fp.set_preference("browser.preferences.instantApply",True)
    fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/plain, application/octet-stream, application/binary, text/csv, application/csv, application/excel, text/comma-separated-values, text/xml, application/xml, text/csv")


    global driver
    driver = webdriver.Firefox(firefox_profile=fp)
    driver.maximize_window()

def chrome(download_default_directory):
    chrome_path = os.path.join(
        os.sep, expanduser("~"), 'Dokumente', 'my_python_modules', 'chromedriver')
    caps = DesiredCapabilities.CHROME
    caps['loggingPrefs'] = {'performance': 'ALL'}

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    prefs = {
        "profile.default_content_settings.popups": 0,
        "download.default_directory": download_default_directory,
        "directory_upgrade": True}
    options.add_experimental_option("prefs", prefs)
    options.add_argument('log-level=3')
    global driver
    driver = webdriver.Chrome(chrome_options=options,
                                desired_capabilities=caps,
                                executable_path=chrome_path)
    #driver.maximize_window()

def headless_chrome(download_default_directory):
    driver_builder = DriverBuilder()
    global driver
    driver = driver_builder.get_driver(download_default_directory, headless=True)

# Apply xpath on a webelement:
def xse(element, xpath):
    return element.find_element_by_xpath(xpath)

# Apply xpath on a webelements (plural):
def xse(element, xpath):
    return element.find_elements_by_xpath(xpath)

def iframe(xpath):
    global driver
    iframe = xs(xpath)
    driver.switch_to_frame(iframe)

def switch2frame(xpath):
    global driver
    driver.switch_to.frame(driver.find_element_by_xpath(xpath))

def default_frame():
    global driver
    driver.switch_to_default_content()

def current_url():
    global driver
    return driver.current_url

def close():
    global driver
    driver.close()

def get(url):
    global driver
    try:
        driver.get(url)
    except TimeoutException:
        print 'Timed out. Retrying.'
        driver.get(url)

def xs(xpath):
    global driver
    return driver.find_element_by_xpath(xpath)

def xp(xpath):
    global driver
    return driver.find_elements_by_xpath(xpath)

def ts(tag_name):
    global driver
    return driver.find_element_by_tag_name(tag_name)

def tp(tag_name):
    global driver
    return driver.find_elements_by_tag_name(tag_name)

def ccs(string):
    xs("//*[contains(@class, '%s')]" % string)

def ids(id):
    global driver
    return driver.find_element_by_xpath('//*[@id="%s"]' % id)

def idp(id):
    global driver
    return driver.find_element_by_xpath('//*[@id="%s"]' % id)

def cls(classname):
    global driver
    return driver.find_element_by_xpath('//*[@class="%s"]' % classname)

def clp(id):
    global driver
    return driver.find_element_by_xpath('//*[@class="%s"]' % classname)

def ics(string):
    xs("//*[contains(@id, '%s')]" % string)

def ccp(string):
    xp("//*[contains(@class, '%s')]" % string)

def icp(string):
    xp("//*[contains(@id, '%s')]" % string)

def ects(string): # element contains text
    xs("//*[contains(text(), '%s')]" % string)

def ectp(string): # element contains text
    xp("//*[contains(text(), '%s')]" % string)

def wait(xpath, timeout):
    global driver
    tabelle = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((By.XPATH, xpath)))

def wait_for_pageload(keywords, timeout, msg=True):
    starttime = datetime.datetime.now()
    timeout = datetime.timedelta(seconds=timeout)
    while True:
        html = xs('/html').get_attribute('outerHTML')
        if any(kwd in html for kwd in keywords):
            break
        elif datetime.datetime.now() > starttime + timeout:
            if msg == True:
                print 'timed out'
            break

def js(javascript):
    global driver
    driver.execute_script(javascript)

def select(xpath, string):
    global driver
    Select(driver.find_element_by_xpath(xpath)).select_by_visible_text(string)
    

def page_has_loaded():
    while True:
        page_state = driver.execute_script('return document.readyState;')
        print page_state
        if page_state == 'complete':
            break

def quit():
    global driver
    driver.quit()

def check_download_status(directory, filename, timeout=120):
    starttime = datetime.datetime.now()
    timeout = datetime.timedelta(seconds=timeout)
    while True:
        current_filecount = len(os.listdir(directory))
        if filename in os.listdir(directory):
            break
        now = datetime.datetime.now()
        if now > starttime + timeout:
            print 'Timed out'
            return False

def check_download_status2(directory, filename_snippet, timeout=120):
    starttime = datetime.datetime.now()
    timeout = datetime.timedelta(seconds=timeout)
    while True:
        current_filecount = len(os.listdir(directory))
        for i in os.listdir(directory):
            if filename_snippet in i and 'crdownload' not in i:
                return True
        now = datetime.datetime.now()
        if now > starttime + timeout:
            print 'Timed out'
            return False

def check_download_status3(directory):
    while True:
        current_filecount = len(os.listdir(directory))
        folder = os.listdir(directory)
        str_folder = ''.join(folder)
        if 'crdownload' not in str_folder \
        and '.csv' in str_folder:
            return True

def hit_enter():
    global driver
    webdriver.ActionChains(driver).send_keys(Keys.RETURN).perform()

def scroll2bottom():
    global driver
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

def scroll2element(xpath):
    global driver
    element = driver.find_element_by_xpath(xpath)
    actions = ActionChains(driver)
    actions.move_to_element(element).perform()

def clickout(xpath):
    global driver
    element = xs(xpath)
    webdriver.ActionChains(driver).click(element).perform()

def hover(xpath):
    global driver
    element = xs(xpath)
    webdriver.ActionChains(driver).move_to_element(element).perform()

def select_option(xpath, by, value_or_text):
    global driver
    select = Select(driver.find_element_by_xpath(xpath))
    if by == 'text':
        select.select_by_visible_text(value_or_text)
    elif by == 'value':
        select.select_by_value(value_or_text)

def get_current_url():
    global driver
    url = driver.current_url
    return url

def get_response_status():
    global driver
    codes = []
    for entry in driver.get_log('performance'):
        if 'statusText' in entry['message']:
            msg = entry['message']
            code = msg.split(',"statusText"')[0].split('"status":')[-1]
            codes.append(code)
    codes = ', '.join(list(set(codes)))
    if len(codes) > 360:
        return ''
    else:
        return codes

def wait_until_clickable(xpath):
    global driver
    element = WebDriverWait(driver, 60).until(
    EC.element_to_be_clickable((By.XPATH, xpath)));

def switch_to_tab(tabnum):
    global driver
    driver.switch_to.window(driver.window_handles[tabnum])

def switch_to_popup():
    global driver
    driver.switch_to_alert()

def new_tab(url):
    global driver
    driver.execute_script('''window.open("'''+url+'''","_blank");''')

def find_by_visible_text(text):
    global driver
    xpath = "//*[contains(text(), '%s')]" % text
    return driver.find_element_by_xpath(xpath)

def disableById(ID, html=False):
    if html == False:
        html = xs('/html').get_attribute('innerHTML')
    if ID in html:
        try:
            js('''document.getElementById("%s").outerHTML = "";''' % ID)
        except Exception as e:
            if "Cannot set property 'outerHTML' of null" in e:
                pass
            #print 'Cannot disble element with Id = %s' % ID

def disableByClassName(ClassName):
    try:
        js('''document.getElementsByClassName("%s")[0].outerHTML = "";''' % ClassName)
    except Exception as e:
        print 'Cannot disble element with ClassName = %s' % ClassName

def restart(d, download_dir=download_dir):
    global driver
    driver.close()
    time.sleep(5)
    if d == 'fox':
        print 'Starting Firefox'
        fp = webdriver.FirefoxProfile()
        fp.set_preference("browser.download.folderList", 2)
        fp.set_preference("browser.download.manager.showWhenStarting", False)
        fp.set_preference("browser.download.dir", download_dir)
        fp.set_preference("browser.preferences.instantApply",True)
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/plain, application/octet-stream, application/binary, text/csv, application/csv, application/excel, text/comma-separated-values, text/xml, application/xml, text/csv")
        global driver
        driver = webdriver.Firefox(firefox_profile=fp)
        driver.maximize_window()
    elif d == 'chrome':
        print 'Starting Chrome'
        caps = DesiredCapabilities.CHROME
        caps['loggingPrefs'] = {'performance': 'ALL'}

        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        prefs = {
            "profile.default_content_settings.popups": 0,
            "download.default_directory": download_dir,
            "directory_upgrade": True}
        options.add_experimental_option("prefs", prefs)
        options.add_argument('log-level=3')
        global driver
        driver = webdriver.Chrome(
            chrome_options=options, desired_capabilities=caps)
    elif d == 'headless_chrome':
            print 'Starting headless Chrome'
            driver_builder = DriverBuilder()
            global driver
            driver = driver_builder.get_driver(download_dir, headless=True)