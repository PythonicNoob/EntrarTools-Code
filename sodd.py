from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException, WebDriverException, InvalidElementStateException
import sys

sleep_time = 3
#TODO: set viewport to low so that internet consumption is reducing meaning you can put more tabs
try:
    with open("data.txt", "r") as file:
        dat = file.readlines()
        username = dat[0].rstrip("\r\n")
        password = dat[1].rstrip("\r\n")
        total_times_join = int(dat[2].rstrip("\r\n"))

except Exception as e:
    print(e)
    sys.exit()

join_text = "Join"

total_times_join = 1000


def main_func():
    times_join = 0
    op = webdriver.ChromeOptions()
    op.add_argument('headless')
    driver = webdriver.Chrome(executable_path="chromedriver.exe")#options=op, executable_path="chromedriver.exe")
    driver.get("https://www.entrar.in/login/login")
    time.sleep(sleep_time)
    driver.find_element_by_name("username").send_keys(username)
    driver.find_element_by_name("password").send_keys(password)
    driver.find_element_by_class_name("login100-form-btn").click()
    time.sleep(sleep_time)

    driver.get("https://entrar.in/classroom_creation_crm_new/s_display")

    while times_join < total_times_join+1:
        print('Joining time:'.times_join)
        try:
            join_button = driver.find_element_by_link_text(join_text)
            if join_button is not None:
                join_button.click()
                times_join += 1
        except NoSuchElementException:
            driver.get("https://entrar.in/classroom_creation_crm_new/s_display")
            print("Join not found")
            time.sleep(sleep_time)
        time.sleep(2)


main_func()

while True:
    print("DOne now waiting")
    time.sleep(1)