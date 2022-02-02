try:
    from selenium import webdriver
except ImportError:
    import os
    os.system('pip install selenium')
    from selenium import webdriver
from time import sleep
timetable = ['/html/body/blockquote/table/tbody/tr[3]/td[*]/input',
             '/html/body/blockquote/table/tbody/tr[4]/td[*]/input',
             '/html/body/blockquote/table/tbody/tr[5]/td[*]/input',
             '/html/body/blockquote/table/tbody/tr[6]/td[*]/input',
             '/html/body/blockquote/table/tbody/tr[7]/td[*]/input',
             '/html/body/blockquote/table/tbody/tr[8]/td[*]/input',
             '/html/body/blockquote/table/tbody/tr[9]/td[*]/input',
             '/html/body/blockquote/table/tbody/tr[10]/td[*]/input',
             '/html/body/blockquote/table/tbody/tr[11]/td[*]/input',
             '/html/body/blockquote/table/tbody/tr[12]/td[*]/input',
             '/html/body/blockquote/table/tbody/tr[13]/td[*]/input',
             '/html/body/blockquote/table/tbody/tr[14]/td[*]/input',
             '/html/body/blockquote/table/tbody/tr[15]/td[*]/input',
             '/html/body/blockquote/table/tbody/tr[16]/td[*]/input',
             '/html/body/blockquote/table/tbody/tr[17]/td[*]/input']


def chooseTime():
    print('\n Choose a time:')
    print('7AM-8AM            1')
    print('8AM-9AM            2')
    print('9AM-10AM           3')
    print('10AM-11AM          4')
    print('11AM-12PM          5')
    print('12PM-1PM           6')
    print('1PM-2PM            7')
    print('2PM-3PM            8')
    print('3PM-4PM            9')
    print('4PM-5PM           10')
    print('5PM-6PM           11')
    print('6PM-7PM           12')
    print('7PM-8PM           13')
    print('8PM-9PM           14')
    print('9PM-10PM          15')
    while True:
        choiceTime = input('\nYour choice: ')
        if choiceTime in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15']:
            return int(choiceTime)-1
        else:
            print("\nInvalid choice.")
            continue


def chooseDay(x):
    slots = []
    for i in range(x):
        print('\n Choose a day:')
        print('Sunday            1')
        print('Monday            2')
        print('Tuesday           3')
        print('Wednesday         4')
        print('Thursday          5')
        print('Friday            6')
        print('Saturday          7')
        while True:
            choiceDay = input('\nYour choice: ')
            if choiceDay in ['1', '2', '3', '4', '5', '6', '7']:
                if choiceDay == '1':
                    period = timetable[chooseTime()].replace('*', '8')
                    slots.append(period)
                    break
                else:
                    period = timetable[chooseTime()].replace('*', choiceDay)
                    slots.append(period)
                    break
            else:
                print("\nInvalid choice.")
                continue
    slots = [i for n, i in enumerate(slots) if i not in slots[:n]]
    return slots


def Booking():

    weeks = int(input('Number of weeks to book: '))
    days = int(input('Number of slots in a week to book: '))
    final = chooseDay(days)

    user = str(input('Username: '))
    password = str(input('Password: '))
    browser = webdriver.Edge()
    browser.get("http://extranet.oppilastalo.fi/")
    browser.find_element_by_xpath(
        '/html/body/div/form/table/tbody/tr[3]/td[2]/input').send_keys(user)
    browser.find_element_by_xpath(
        '/html/body/div/form/table/tbody/tr[4]/td[2]/input').send_keys(password)
    browser.find_element_by_xpath(
        '/html/body/div/form/table/tbody/tr[5]/td[1]/input').click()
    sleep(3)
    week = 0
    while week <= weeks:
        for i in range(len(final)):
            browser.find_element_by_xpath('/html/body/code/a[4]').click()
            sleep(3)
            while True:
                try:
                    browser.find_element_by_xpath(final[i]).click()
                    browser.find_element_by_xpath(
                        '/html/body/blockquote/submenu/blockquote/input[1]').click()
                    break
                except:
                    try:
                        browser.find_element_by_xpath(
                            '/html/body/blockquote/table/tbody/tr[1]/td[7]/input').click()
                        sleep(5)
                    except:
                        browser.close()
                        return
        week += 1
    browser.close()


if __name__ == '__main__':
    Booking()
