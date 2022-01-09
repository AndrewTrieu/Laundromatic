from selenium import webdriver
from time import sleep


def Booking():
    weeks = int(input('Weeks? '))
    browser = webdriver.Edge(
        "/Users/Dell/AppData/Local/Programs/Python/Python39/msedgedriver.exe")
    browser.get("http://extranet.oppilastalo.fi/")
    browser.find_element_by_xpath(
        '/html/body/div/form/table/tbody/tr[3]/td[2]/input').send_keys('10126/3005')
    browser.find_element_by_xpath(
        '/html/body/div/form/table/tbody/tr[4]/td[2]/input').send_keys('clouE1c1')
    browser.find_element_by_xpath(
        '/html/body/div/form/table/tbody/tr[5]/td[1]/input').click()
    sleep(3)
    path = {1: '/html/body/blockquote/table/tbody/tr[16]/td[4]/input',
            2: '/html/body/blockquote/table/tbody/tr[17]/td[4]/input',
            3: '/html/body/blockquote/table/tbody/tr[16]/td[8]/input',
            4: '/html/body/blockquote/table/tbody/tr[17]/td[8]/input'}
    week = 0
    while week <= weeks:
        for i in range(1, 5):
            browser.find_element_by_xpath('/html/body/code/a[4]').click()
            sleep(3)
            while True:
                try:
                    browser.find_element_by_xpath(path[i]).click()
                    browser.find_element_by_xpath(
                        '/html/body/blockquote/submenu/blockquote/input[1]').click()
                    break
                except:
                    try:
                        browser.find_element_by_xpath(
                            '/html/body/blockquote/table/tbody/tr[1]/td[7]/input').click()
                        sleep(5)
                        continue
                    except:
                        print('Ei näe enempää viikkoja.')
        week += 1


if __name__ == '__main__':
    Booking()
