from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time
from selenium.common.exceptions import NoSuchElementException, WebDriverException, InvalidElementStateException
import urllib.request
import requests
import os
import pdfkit
import winsound
import easygui
import random
#rom multiprocessing import Process
import threading
import sys
import shutil
import re
import configparser
import ctypes
from git.repo import Repo
from cryptography.fernet import Fernet

VERSION = 1.3
def isAdmin():
    try:
        is_admin = (os.getuid() == 0)
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return is_admin

for rm_no in range(1,100):
    try:
        if os.path.isfile("chromedriver_old.exe"):
            os.remove("chromedriver_old.exe")
        if os.path.isdir("wkhtmltox_old"):
            shutil.rmtree("wkhtmltox_old")
        if os.path.isfile("EntrarAttender_old.exe"):
            os.remove("EntrarAttender_old.exe")
        try:
            shutil.rmtree("tmp", ignore_errors=True)
        except Exception as e:
            print("Could not remove tmp folder due to:")
            print(e)
    except Exception as e:
        print("Could not remove old files")
        print(e)

while os.path.isdir("tmp"):
    easygui.msgbox("Please remove the 'tmp' folder in the directory of this app and then click ok.")

def update():
    try:
        ver = requests.get("https://raw.githubusercontent.com/ansh850/EntrarAttender/master/version.txt")
        if float(ver.text) > VERSION:
            easygui.msgbox("Updating the app please wait!")
            if isAdmin() == False:
                easygui.msgbox(
                    "Please run this app as an administrator to update!. right click EntrarAttender.exe and run as administrator! This app cannot update without administrator permissions!")
                sys.exit()
            os.rename("EntrarAttender.exe", "EntrarAttender_old.exe")
            try:
                os.rename("chromedriver.exe", "chromedriver_old.exe")
                os.rename("wkhtmltox", "wkhtmltox_old")
            except Exception as e:
                print("Could not rename old files due to:")
                print(e)
            Repo.clone_from("https://github.com/ansh850/EntrarAttender.git", "tmp")
            source_files = []
            to_copy_files = []
            for x, y, z in os.walk("tmp"):
                for filename in z:
                    source_files.append(os.path.join(x,filename))
            for fl in source_files:
                if fl.split('\\')[1] != ".git":
                    to_copy_files.append(fl)
            for fle in to_copy_files:
                try:
                    if len(fle.split('\\')) <= 2:
                        shutil.copy(fle, '\\'.join( fle.split("\\")[1:] ) )
                    else:
                        shutil.copytree('\\'.join(fle.split("\\")[:2]), fle.split('\\')[1])
                except Exception as e:
                    print("Exception occured while copying file", fle)
                    print(e)


            for rm_no in range(1,100):
                try:
                    shutil.rmtree("tmp")
                except Exception as e:
                    print("Could not remove tmp folder due to:")
                    print(e)

            try:
                os.remove("EntrarAttender_old.exe")
                os.remove("chromedriver_old.exe")
                shutil.rmtree("wkhtmltox_old")
            except Exception as e:
                print("Exception occured while removing old files")
                print(e)

            os.system("EntrarAttender.exe")
            sys.exit()

    except Exception as e:
        print("Could not update due to:")
        print(e)

update()

#TODO: Clean Code
#TODO: Starting Text
#TODO: Device Choice
#TODO: Option to store SVG files which are downloaded

def save_existing_pres():
    with open(download_preps, "w") as file:
        print("Saving existing presentation")
        for pres_name in [str(x)+"\n" for x in existing_presentations]:
            file.write(pres_name)
            print("pres_name: ",pres_name)

def save_existing_pres_d2():
    with open("downloaded_presentation2.txt", "w") as file:
        print("Saving existing presentation")
        for pres_name in [str(x)+"\n" for x in existing_downloaded_presentations]:
            file.write(pres_name)
            print("pres_name_from_button_download: ",pres_name)
def gettheval(command):
    localval = None
    while localval is None:
        localval = eval(command)
    return localval

def getvalinrange(keyword, command, range, valuetype):
    value = config["Entrar Attender"][keyword]
    if valuetype == 'int':
        try:
            value = int(value)
        except:
            pass
    elif valuetype == 'bool':
        try:
            value = config["Entrar Attender"].getboolean(keyword, fallback=None)
        except:
            pass
    elif valuetype == 'float':
        try:
            value = config["Entrar Attender"].getfloat(keyword,fallback=None)
        except:pass
    if value in range: return value
    else:
        while (value not in range):
            try:
                value = eval(command)
                # print("Value while trying: ", value)
                # print("Value not in range: ", value not in range)
            except:
                pass
        # print("Keyword to be used: ", keyword)
        # print("Value to be recorded: ", value)
        # print("Range to be used: ", range)
        # print("Is value in range: ", value in range)
        config["Entrar Attender"][keyword] = str(value)
        with open('config.ini', 'w') as file:
                config.write(file)
        return value

easygui.msgbox("This app is made by Ansh Tulsyan")
#easygui.msgbox("Hello! So you decided classes were boring!! This program can get you through your online classes! If you want to close this application just close the chrome app! ")
easygui.msgbox("This app will help you during entrar. Download and sort presentations automatically! Now you can only focus on classes!")

config = configparser.ConfigParser()

if os.path.isfile('config.ini'):
    config.read('config.ini')
else:
    config_speakGM = gettheval(
        'easygui.boolbox("Do you want the app to write Good Morning ma\'am in public chat when class starts?")')
    config_downloadpresentations = gettheval(
        'easygui.boolbox("Do you want the app to download presentations shown in the class?")')
    config_answerQuestions = gettheval('easygui.boolbox("Do you want the app to answer polling questions with random answers?")')
    config_usedefaultname = gettheval(
        'easygui.boolbox("Do you want to type the name of presentations downloaded by this app or use default name? Say yes to use default values or no to type")')

    config_username = gettheval('easygui.enterbox("Entrar username")')
    config_password = gettheval('easygui.passwordbox("password")')
    config_noofclasses = gettheval(
        'easygui.integerbox("Enter the number of classes per day.", default=3, lowerbound=1, upperbound=9)')
    while 1 == 1:
        try:
            yesnoconf = gettheval(
                'easygui.enterbox("Enter a value from 0 to 1. This decides during poll which answer would be more chosen. type 1 for only yes or 0 for only no. Recommended is 0.8")')
            yesnoconf = float(yesnoconf)
            if yesnoconf < 0 or yesnoconf > 1:
                easygui.msgbox("Please enter a value between 0 and 1")
            else:
                break
        except ValueError:
            easygui.msgbox("Please enter a valid value")
    config_classduration = gettheval(
        'easygui.integerbox("Enter the duration of one class in seconds. 1 hour = 3600 seconds", default=3600, lowerbound=600, upperbound=7200)')
    config_internetspeed = gettheval(
        'easygui.integerbox("On a scale of 2 to 5 rate your Internet speed. 2 is average and 5 is very very slow. ", default=2, lowerbound=2, upperbound=5)')

    config["Entrar Attender"] = {
        "Username": config_username,
        "Password": config_password,
        "Number of Classes": config_noofclasses,
        "Yes or No probability": yesnoconf,
        "Class Duration": config_classduration,
        "Internet Speed": config_internetspeed,
        "Type GM": config_speakGM,
        "Download Presentations": config_downloadpresentations,
        "Answer Questions": config_answerQuestions,
        "Use Default Name": config_usedefaultname,
        "wkhtml path": 'wkhtmltox/bin/wkhtmltopdf.exe',
        "chromedriver path": "chromedriver.exe"
    }

    with open('config.ini' , 'w') as file:
        config.write(file)


# no_of_classes = 3
# yes_no_confidence = 0.8
# class_duration = 3600 #In seconds
# sleep_time = 2 #Minimum 2 Maximum 5 How much do you need to wait before a page is loadded completely. Used at time.sleep
# speakGoodMorning = True
# download_presentations_bool = True
# answer_random_questions = True
# use_default_presentation_name = False
username = config["Entrar Attender"]["Username"]
password = config["Entrar Attender"]["Password"]
no_of_classes = getvalinrange("Number of Classes", 'easygui.integerbox("Please enter the number of classes.",default=3, lowerbound=1, upperbound=9)',  list(range(1,9)), 'int')
yes_no_confidence = getvalinrange("Yes or No probability", 'float(easygui.enterbox("Enter a value from 0 to 1. This decides during poll which answer would be more chosen. type 1 for only yes or 0 for only no. Recommended is 0.8"))', [y/10 for y in list(range(0,11))], 'float')
class_duration = getvalinrange("Class Duration", 'easygui.integerbox("Enter the duration of one class in seconds. 1 hour = 3600 seconds", default=3600, lowerbound=600, upperbound=7200)', list(range(600,7200)),'int')
sleep_time = getvalinrange("Internet Speed",'easygui.integerbox("On a scale of 2 to 5 rate your Internet speed. 2 is average and 5 is very very slow. ", default=2, lowerbound=2, upperbound=5)', list(range(2,5)), 'int')
speakGoodMorning = getvalinrange("Type GM", 'easygui.boolbox("Do you want the app to download presentations shown in the class?")', [True, False], 'bool')
download_presentations_bool = getvalinrange("Download Presentations", 'easygui.boolbox("Do you want the app to download presentations shown in the class? ")', [True, False], 'bool')
answer_random_questions = getvalinrange("Answer Questions", 'easygui.boolbox("Do you want the app to answer polling questions with random answers?")', [True, False], 'bool')
use_default_presentation_name = getvalinrange("Use Default Name", 'easygui.boolbox("Do you want to type the name of presentations downloaded by this app or use default value? Say yes to use default values or no to type")', [True,False], 'bool')


#Wait here
#input("Waiting here to stop?")

wkhtml_path = config["Entrar Attender"]["wkhtml path"]
chromedriver_path = config["Entrar Attender"]["chromedriver path"]

continue_PresDownloading = False
continue_ButtonPressing = False

heroku_domain = " https://trialrun01.herokuapp.com/"#"https://trialrun01.herokuapp.com/"
encryption_key = b'aPOnGhpG378vPzKueY94migAlZT4jxEJIyoK3brNGYc='
sending_auth_key = "aEHCIG2GQA5PzA4rvL2x5odWm34uKHtc"
sending_auth_pass = "B8Dq0S3f3uSK7zZkTIimDmpqvJpGOduP"
userdetails_post_address = "f6lsHfFHJB1Dj/"

manual_check_time = 300 #In seconds
last_time_manual_check = 0
class_start_time = 0
download_preps = "downloaded_presentation.txt"
existing_presentations = []
existing_downloaded_presentations = []

while 1 == 1:
    try:
        pdfkit_config = pdfkit.configuration(wkhtmltopdf=wkhtml_path)
        config["Entrar Attender"]['wkhtml path'] = wkhtml_path
        with open("config.ini", "w") as file:
            config.write(file)
        break
    except OSError:
        easygui.msgbox("Please select the folder of name \"wkhtmltox\" ")
        wk_folderpath = easygui.diropenbox()
        print(wk_folderpath)
        for root, dirs, files in os.walk(wk_folderpath, topdown=False):
            for name in files:
                if name.endswith("wkhtmltopdf.exe"):
                    wkhtml_path = os.path.join(root, name)
                    print("wkhtml_path: ", wkhtml_path)

try:
    with open("downloaded_presentation.txt", "r+") as get_downloaded_text:
        readfiles = get_downloaded_text.readlines()
        if len(readfiles) != 0 and readfiles is not None:
            existing_presentations = [x.rstrip('\n') for x in readfiles]
        get_downloaded_text.close()
except FileNotFoundError:
    existing_presentations = []

try:
    with open("downloaded_presentation2.txt", "r+") as get_downloaded_text:
        readfiles = get_downloaded_text.readlines()
        if len(readfiles) != 0 and readfiles is not None:
            existing_downloaded_presentations = [x.rstrip('\n') for x in readfiles]
        get_downloaded_text.close()
except FileNotFoundError:
    existing_downloaded_presentations = []
#download_preps_file = open( "downloaded_presentation.txt", "a+" )

ILLEGAL_NTFS_CHARS = "[<>:/\\|?*\"]|[\0-\31]"
def removeIllegalChars(name):
    # removes characters that are invalid for NTFS
    return re.sub(ILLEGAL_NTFS_CHARS, "", name)

def download_presentation_svg(main_url, output_file_name):
    print("Getting svg of files")
    i = 0
    image_links = []
    while 1 == 1:
        i += 1
        this_url = main_url + str(i)
        if requests.get(this_url).status_code != 404:

            # pass
            urllib.request.urlretrieve(this_url, "presentation_svg\\"+title+"\\"+output_file_name+"\\"+output_file_name+"_"+str(i)+".svg")
            image_links.append(this_url)
        else:
            print("Slide Count: ", i - 1)
            break
    pdfkit.from_url(image_links, "presentation\\" + title + "\\" + output_file_name + "\\" + output_file_name + ".pdf", configuration=pdfkit_config)


def download_presentations_function():
    global continue_PresDownloading
    print("Download presentation function called")
    while continue_PresDownloading:
        print("Function in a loop of download presentation")
        try:
            image = driver.find_element_by_tag_name("image")
            url = image.get_attribute("xlink:href")
            url_parts = url.split('/')
            main_url = '/'.join(url_parts[:5]+["download",url_parts[5], url_parts[7]+"?presFilename="+url_parts[7] ])
            presentation_name = url_parts[7].split('-')[0]
            file_extensions = ["docx", "doc", "ppt", "pptx", "pdf", "docx", "doc"]
            for x in driver.find_elements_by_tag_name("i"):
                if x.get_attribute("class") == "icon--2q1XXw icon-bbb-template_download":
                    if presentation_name not in existing_downloaded_presentations:
                        for extension in file_extensions:
                            r = requests.get(main_url + "." + extension)
                            if r.status_code == 200:
                                pres_filename = url_parts[7]
                                try:
                                    os.makedirs("presentation_downloaded\\" + title + "\\" + pres_filename)
                                except:
                                    pass
                                urllib.request.urlretrieve(main_url + "." + extension, "presentation_downloaded\\" + title + "\\" + pres_filename+"\\"+pres_filename+"."+extension)

                                existing_downloaded_presentations.append(presentation_name)
                                save_existing_pres_d2()
        except Exception as e:
            print("Exception while downloading presentation directly")
            print(e)

        try:
            image = driver.find_element_by_tag_name("image")
            url = image.get_attribute("xlink:href")
            main_url = '/'.join(url.split('/')[:-1]) + '/'
            presentation_name = main_url.split("/")[-3]
            presentation_name = presentation_name.split('-')[0]

            if presentation_name not in existing_presentations:
                pres_filename = ''
                if use_default_presentation_name == True:
                    pres_filename = removeIllegalChars(main_url.split("/")[-3])[:64]
                else:
                    winsound.PlaySound("SystemQuestion", winsound.SND_ALIAS)
                    pres_filename = easygui.enterbox("Prsentation has beeen detetcted. Please enter the file name.")
                    pres_filename = removeIllegalChars(pres_filename)
                    pres_filename = pres_filename[:64]
                try:
                    os.makedirs("presentation\\" + title+"\\"+ pres_filename)
                    os.makedirs("presentation_svg\\" + title + "\\" + pres_filename)
                except:
                    pass

                download_presentation_svg(main_url, pres_filename)
                existing_presentations.append(presentation_name)
                save_existing_pres()
        except Exception as e:
            print("Exception while capturing svg pictures:")
            print(e)

def button_presser_function():
    global continue_ButtonPressing
    print("Button presser function called")
    while continue_ButtonPressing:
        try:
            yes_button = driver.find_element_by_xpath('//button[normalize-space()="Yes"]')
            no_button = driver.find_element_by_xpath('//button[normalize-space()="No"]')
            prob = random.random()
            if prob > yes_no_confidence:
                no_button.click()
            else:
                yes_button.click()
            print("Pressed button for you")
        except NoSuchElementException:
            pass
        except Exception as e:
            print("exception while trying to get yes or no")
            print(e)
        try:
            a_button = driver.find_element_by_xpath('//button[normalize-space()="A"]')
            b_button = driver.find_element_by_xpath('//button[normalize-space()="B"]')
            prob = random.choice([0,1])
            if prob == 0:
                a_button.click()
            if prob == 1:
                b_button.click()
            else:
                print("No Choice found")
                a_button.click()
            print("Pressed button for you")
        except NoSuchElementException:
            pass
        except Exception as e:
            print("exception while trying to get A or B")
            print(e)

def say_GoodMorning():
    #Say Good Morning If public chat is enabled
    time.sleep(5)
    while time.time() - class_start_time < 600:
        try:
            driver.find_element_by_id("message-input").send_keys("Good Morning ma'am")
            driver.find_element_by_id("message-input").send_keys(Keys.RETURN)
            break
        except Exception as e:
            print("Could not type gm:")
            print(e)

def start_class():
    print("Class started")
    global title
    driver.get("https://entrar.in/classroom_creation_crm_new/s_display")
    time.sleep(sleep_time)
    time.sleep(sleep_time)
    while 1 == 1:
        try:
            join_button = driver.find_element_by_link_text("Join")
            if join_button is not None:
                join_button.click()
                break
        except NoSuchElementException:
            driver.get("https://entrar.in/classroom_creation_crm_new/s_display")
            print("Join not found")
            time.sleep(sleep_time)
    time.sleep(sleep_time)
    driver.switch_to.window(driver.window_handles[-1])
    global class_start_time
    class_start_time = time.time()
    time.sleep(sleep_time)
    time.sleep(20)
    try:
        title = driver.find_element_by_class_name("presentationTitle--1LT79g").text
    except NoSuchElementException:
        title = easygui.enterbox("The Title of this class:")
        title = removeIllegalChars(title)

    print("Staring name main")
    print("setting variables to true")

    global continue_ButtonPressing
    global continue_PresDownloading
    #global continue_sayGm
    continue_PresDownloading = True
    continue_ButtonPressing = True
    if __name__ == '__main__':
        if download_presentations_bool == True:
            print("Starting downloader daemon")
            global presentation_downloader_daemon
            presentation_downloader_daemon = threading.Thread(target=download_presentations_function, daemon=True)
            presentation_downloader_daemon.start()
            print("Done")
        if answer_random_questions == True:
            print("Starting Presentation downloader daemon")
            global button_presser_daemon
            button_presser_daemon = threading.Thread(target=button_presser_function, daemon=True)
            button_presser_daemon.start()
            print("Done")
        if speakGoodMorning == True:
            print("Starting GM daemon")
            global say_GM_daemon
            say_GM_daemon = threading.Thread(target=say_GoodMorning(), daemon=True)
            say_GM_daemon.start()
            print("Done")


def has_class_ended():
    #TODO: Function to check session ended forward to homepage
    try:
        buttons = driver.find_elements_by_tag_name("button")
        for button in buttons:
            if button.get_attribute("description") == "Logs you out of the meeting":
                button.click()
                return True
    except Exception as e:
        print("Exception while trying to find ecit button:")
        print(e)
    global last_time_manual_check
    if time.time() - class_start_time > 3600:
        if time.time() - last_time_manual_check > manual_check_time:
            last_time_manual_check = time.time()
            winsound.PlaySound("SystemQuestion", winsound.SND_ALIAS)
            if easygui.ynbox('Has the Class ended?', 'Class Ended', ('Yes', 'No')): return True


    return False #TODO: Proper Check for classes ended. Also check every 5 minutes after 1 hour of class if class has ended

def end_class():
    global title
    global continue_ButtonPressing
    global continue_PresDownloading
    #Stop All daemons
    # if download_presentations_bool == True:
    #     presentation_downloader_daemon.terminate()
    # if answer_random_questions == True:
    #     button_presser_daemon.terminate()
    continue_ButtonPressing = False
    continue_PresDownloading = False
    try:
        if presentation_downloader_daemon:
            presentation_downloader_daemon.join()
        if button_presser_daemon:
            button_presser_daemon.join()
        if say_GM_daemon:
            say_GM_daemon.join()
    except Exception as e:
        print("Error while joining threads")
        print(e)
    title = '' #Change the title  to none so that it raises error in case no title is given
    driver.get("https://entrar.in/classroom_creation_crm_new/s_display")
    time.sleep(sleep_time)
    time.sleep(5)

#chromedriver_path = config["Entrar Attender"]["chromedriver path"]
while 1==1:
    try:
        driver = webdriver.Chrome(executable_path=chromedriver_path)
        config["Entrar Attender"]["chromedriver path"] = chromedriver_path
        with open("config.ini","w") as file:
            config.write(file)
        break
    except WebDriverException:
        easygui.msgbox("Please select the chromedriver file")
        chromedriver_path = easygui.fileopenbox(filetypes=[(".exe")])


driver.get("https://www.entrar.in/login/login")
time.sleep(sleep_time)
driver.find_element_by_name("username").send_keys(username)
driver.find_element_by_name("password").send_keys(password)
driver.find_element_by_class_name("login100-form-btn").click()
time.sleep(sleep_time)

while driver.current_url == "https://entrar.in/login/authenticate/":
    winsound.PlaySound("SystemQuestion", winsound.SND_ALIAS)
    #easygui.msgbox("Invalid Username and / or Password. Please write correct username and password and try again")
    username, password = easygui.multpasswordbox("Invalid Username and / or Password. Please write correct username and password and try again", fields=["Username", 'Password'])
    driver.find_element_by_name("username").send_keys(username)
    driver.find_element_by_name("password").send_keys(password)
    driver.find_element_by_class_name("login100-form-btn").click()
    config["Entrar Attender"]["Username"] = username
    config["Entrar Attender"]["Password"] = password
    with open("config.ini","w") as file:
        config.write(file)
    time.sleep(sleep_time)
    #driver.quit()
    #sys.exit()

driver.get("https://entrar.in/classroom_creation_crm_new/s_display")
time.sleep(sleep_time)
title = ''



for class_number in range(0, no_of_classes):
    time.sleep(3)
    print("Started class", class_number)
    start_class()
    class_ended = False
    while class_ended == False:
        class_ended = has_class_ended()
    end_class()
    time.sleep(30)
