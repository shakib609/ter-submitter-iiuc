from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import time


def login(browser, matric, password, url):
    browser.get(url)
    assert "IIUC Students Panel" in browser.title

    username_field = browser.find_element_by_css_selector(
        'input[name="studentID"]')
    password_field = browser.find_element_by_css_selector(
        'input[name="password"]')
    username_field.send_keys(matric)
    password_field.send_keys(password)
    password_field.send_keys(Keys.ENTER)
    try:
        logged_in_element = browser.find_element_by_id('uwp-user')
        assert 'logged in' in logged_in_element.text
    except Exception as e:
        print('Wrong username or password! Login Failed!')
        browser.quit()
        raise e


def rate_teacher(browser):
    time.sleep(10)
    radios = browser.find_elements_by_css_selector('input[value="5"]')
    for r in radios:
        r.click()
    submit = browser.find_elements_by_css_selector('input[type="submit"]')[0]
    submit.click()
    time.sleep(10)


def process_ter_page(browser, url, section):
    browser.get(url)
    while True:
        select_element = browser.find_elements_by_tag_name('select')
        if select_element:
            s = Select(select_element[0])
            options = list(filter(lambda x: section in x.text, s.options))
            if len(options) > 1:
                print('\nWhich one is your Course?')
                i = 1
                for x in options:
                    print(i, x.get_attribute('value'))
                    i += 1
                answer = int(input('Enter your choice(Integer): '))
                if answer > i:
                    print('Stop joking around!')
                    browser.quit()
                o = options[answer - 1]
            s.select_by_value(o.get_attribute('value'))
            button = browser.find_elements_by_css_selector(
                'input[value="Load TER Form"]')[0]
            button.click()
            rate_teacher(browser)
        else:
            break


if __name__ == '__main__':
    MATRIC = input('Enter your matric number: ').strip().upper()
    PASSWORD = input('Enter your password: ').strip()
    SECTION = input('Enter your section(ex.5AM):').strip().upper()
    LOGIN_URL = 'http://upanel.iiuc.ac.bd:81'
    TER_URL = 'http://upanel.iiuc.ac.bd:81/terindex.php'
    browser = webdriver.Chrome("chromedriver_linux64/chromedriver")
    login(browser, MATRIC, PASSWORD, LOGIN_URL)
    process_ter_page(browser, TER_URL, SECTION)
    browser.quit()
    print('TER submitted successfully!')
