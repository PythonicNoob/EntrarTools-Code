from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import requests
from PIL import Image
import time
from selenium.common.exceptions import NoSuchElementException, WebDriverException, InvalidElementStateException
from googlesearch import search
from urllib.parse import urlencode
import sys
import pytesseract
from io import BytesIO
import re
try:
    import pkg_resources.py2_warn
except ImportError:
    pass

try:

    with open("required_data.txt", "r") as file:
        x = file.readlines()
        username = x[0].rstrip("\r\n")
        password = x[1].rstrip("\r\n")
        pytesseract.pytesseract.tesseract_cmd = x[2].rstrip("\r\n")  # r'C:\Program Files\Tesseract-OCR\tesseract.exe'


    def get_question():
        while 1 == 1:
            try:
                for image_element in driver.find_elements_by_tag_name("img"):
                    if "click here to view large" in image_element.get_attribute("title"):
                        print("found question")
                        question_element = image_element
                        r = requests.get(question_element.get_attribute("src"))
                        if r.status_code != 404:
                            img = Image.open(BytesIO(r.content))
                            pytess_txt = pytesseract.image_to_string(img)
                            return pytess_txt
                print("Taking text")
                question = driver.find_element_by_xpath(Question_xpath).text
                return question

            except NoSuchElementException:
                pass
                # question = driver.find_element_by_xpath(Question_xpath).text
                # return question
            except Exception as e:
                print("Could not find question due to:")
                print(e)

            # if question == "":

        return "Hello? This not the question this is random stuff error error error error error error error error error error error error error error error erroer error"


    def solve_captcha():
        driver.get(answers_repo_site)
        # while driver.title != blocked_title:
        #     driver.get(answers_repo_site)
        #     time.sleep(0.1)
        while driver.title == blocked_title:
            time.sleep(0.1)
        print("Solved Captcha")


    def open_links(question):
        serachresult = search(question, num=no_of_results - 2, stop=no_of_results - 2)

        google_query = "https://www.google.com/search?q="[:-2] + urlencode({"q": question})
        driver.execute_script("window.open(arguments[0])", google_query)

        answer_repo_query = answer_repo_q[:-2] + urlencode({"q": question})
        driver.execute_script("window.open(arguments[0])", answer_repo_query)
        #
        # for link in serachresult:
        #     driver.execute_script("window.open(arguments[0])", link)


    def close_links():
        for handle in driver.window_handles[1:]:
            driver.switch_to.window(handle)
            # driver.close()
            driver.find_element_by_tag_name("body").send_keys(Keys.CONTROL + 'W')
        driver.switch_to.window(driver.window_handles[0])


    sleep_time = 3

    no_of_results = 5

    join_text = "Start"
    join_page = "https://entrar.in/online_assessment_student_test/index"
    Question_xpath = "//td[@class='text-wrap']//b"
    blocked_title = "You have been blocked"
    answers_repo_site = "https://www.brainly.in"
    answer_repo_q = answers_repo_site + "/app/ask?entry=hero&q="

    driver = webdriver.Chrome()
    solve_captcha()
    driver.get("https://www.entrar.in/login/login")
    time.sleep(sleep_time)
    driver.find_element_by_name("username").send_keys(username)
    driver.find_element_by_name("password").send_keys(password)
    driver.find_element_by_class_name("login100-form-btn").click()
    time.sleep(sleep_time)

    driver.get(join_page)

    # def get_question():
    #     while 1 == 1:
    #         try:
    #             question = driver.find_element_by_xpath(Question_xpath).text
    #             return question
    #             break
    #         except NoSuchElementException:
    #             time.sleep(0.1)
    #         except Exception as e:
    #             print("Error occured hile trying to get the question:")
    #             print(e)
    #
    #     return "Hello? This not the question this is random stuff error error error error error error error error error error error error error error error erroer error"

    type_file = open("questions.txt", "a")

    while 1 == 1:
        try:
            join_button = driver.find_element_by_link_text(join_text)
            if join_button is not None:
                join_button.click()
                break
        except NoSuchElementException:
            driver.get(join_page)
            print("Join not found")
            time.sleep(sleep_time)

    time.sleep(1)
    curr_question = ""


    def main():
        global curr_question
        while True:
            question_raw = get_question()
            # question = unidecode(unicode(question, encoding = "utf-8"))
            question_raw_2 = question_raw.encode(sys.stdout.encoding, errors='replace').decode('utf-8')
            question = re.sub("['\"?]+?", "", question_raw_2)
            if question != curr_question:
                print("Beginning Question: ", question)
                # close_links()
                type_file = open("questions.txt", "a")
                type_file.write(question + "\n")
                type_file.close()
                open_links(question)
                curr_question = question

            else:
                time.sleep(0.2)


    main()


except Exception as e:
    print("exception :")
    print(e)
    with open("debuglog.log", "w") as logfile:
        logfile.write("Could not do shit.....  cos of:\n")
        logfile.write(str(e))
