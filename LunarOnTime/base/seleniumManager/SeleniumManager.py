import pyautogui
import undetected_chromedriver.v2 as uc
from time import sleep
import os
from pyoptions import options
# from pyoption import option
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import random
from base.model import ChromeProfile
from base.utils import Utils
from win32api import GetFileVersionInfo, HIWORD

TimeOut = 30


def createNewChrome(chromeProfile: ChromeProfile, posThread, numThreads):
    options = uc.ChromeOptions()
    # Profile
    if not os.path.exists(chromeProfile.profilePath):
        os.makedirs(chromeProfile.profilePath)
    if chromeProfile.chromePath != "":
        options.binary_location = f'{chromeProfile.chromePath}'
    options.user_data_dir = chromeProfile.profilePath
    # End
    # Chrome file exe

    if chromeProfile.chromePath != "":
        options.binary_location = chromeProfile.chromePath

    chrome_version =  HIWORD(GetFileVersionInfo(options.binary_location, "\\").get('FileVersionMS'))
    if chrome_version == 95:
        chrome_driver = './chromedriver95.exe'
    elif chrome_version == 85:
        chrome_driver = './chromedriver85.exe'
    else:
        chrome_driver = './chromedriver93.exe'

    # End
    chrome_locale = 'en-us'
    options.add_argument("--lang={}".format(chrome_locale))
    # Dis
    options.add_argument('--disable-session-crashed-bubble')
    options.add_argument('--disable-application-cache')
    # Pop-up
    options.add_argument('--disable-popup-blocking')
    # End

    # Extension
    if chromeProfile.ipaddress != "":
        options.add_argument(f'--proxy-server={chromeProfile.ipaddress}')

    exPath = getListExtension(chromeProfile.webRtcPath)
    extension_path = f'{exPath}'
    options.add_argument('--disable-extensions')
    options.add_argument(f'--disable-extensions-except={extension_path}')
    options.add_argument(f'--load-extension={extension_path}')
    # End

    # User Agent
    options.add_argument(f'user-agent=={chromeProfile.userAgent}')
    # End

    # With. Height
    options.add_argument(f'--window-size={chromeProfile.width},{chromeProfile.height}')
    # End
    options.add_argument('--no-first-run --no-service-autorun --password-store=basic')
    driver = uc.Chrome(executable_path=chrome_driver, options=options)
    if numThreads >= 3:
        try:
            width, height = pyautogui.size()
            width_window = width / numThreads
            index_window = posThread * width_window
            driver.set_window_rect(index_window, 0, width_window, 1000)
        except:
            pass
    return driver


def FindCoin(chromeDriver):
    goToWebsite(chromeDriver, "https://lunarcrush.com/search")
    Sleep(2)
    listRandomText = ['btc', 'pre', 'sol']
    coinInput = random.choices(listRandomText)
    inputCoin = findElementByXpath(chromeDriver, "//input[@type='text']")
    setValueInput(inputCoin, coinInput)
    setValueInput(inputCoin, Keys.ENTER)
    Sleep(60)


def readMarket(chromeDriver):
    Sleep(3)
    goToWebsite(chromeDriver, "https://lunarcrush.com/markets")
    Sleep(60)


def checkTimeoutSite(chromeDriver):
    goToWebsite(chromeDriver, 'https://lunarcrush.com/account')
    Sleep(10)
    notification = ''
    try:
        notification = WebDriverWait(chromeDriver, 5).until(EC.presence_of_element_located(
            (By.XPATH, '//div[text()="There was an error getting data for this section. Try again shortly."]')))
    except:
        pass
    countnotification = 0
    while True:
        if notification == '':
            break
        elif notification != '':
            goToWebsite(chromeDriver, 'https://lunarcrush.com/account')
            sleep(2)
            countnotification += 1
            try:
                notification = WebDriverWait(chromeDriver, 5).until(EC.presence_of_element_located(
                    (By.XPATH,
                     '//div[text()="There was an error getting data for this section. Try again shortly."]')))
            except:
                break
            if notification == 20:
                break
    Sleep(3)
    btnViewPoint = findElementByInfo(chromeDriver, 'xpath=//div[text()="View points"]')
    Sleep(5)
    clickButton(btnViewPoint)
    Sleep(10)
    timeOnSite = findElementsByXpath(chromeDriver, '//div[@class="css-901oao r-1q4o75h r-gs8g7 r-1b43r93 r-1vr29t4"]')
    if timeOnSite != "":
        try:
            time = int(timeOnSite[6].text)
        except:
            return 3
        if time == 120:
            print("Đủ")
            return 0
        else:
            return 3
    return 3


def clickShares(chromeDriver):
    listLinkPost = []
    try:
        goToWebsite(chromeDriver, "https://lunarcrush.com/")
        allElement = findElementsByXpath(chromeDriver, "//a[@href]")
        allRef = []
        for i in allElement:
            if i.get_attribute('href').startswith("https://lunarcrush.com/feeds/news"):
                allRef.append(i.get_attribute('href'))
        for i in allRef:
            try:
                if i.startswith("https://lunarcrush.com/feeds/news"):
                    id = i[i.rfind('-') + 1:i.rfind('?')]
                    listLinkPost.append('https://lunarcrush.com/share?ctx=feeds&share=Feed&item=news-' + str(id))
            except:
                pass
        return listLinkPost
    except:
        return listLinkPost


def StartAutoTimeOnSite(chromeDriver, listLock):
    while True:
        status = checkTimeoutSite(chromeDriver)
        listLinkPost = clickShares(chromeDriver)
        if status == 0:
            return
        else:
            if len(listLinkPost) > 1:
                index = random.randint(0, (len(listLinkPost)-1))
                sleep(1)
                goToWebsite(chromeDriver, listLinkPost[index])
                sleep(3)
                btnShare = findElementsByXpath(chromeDriver, '//div[@data-cssclass="iconTop"]')
                if btnShare != "":
                    Sleep(3)
                    try:
                        clickButton(btnShare[0])
                    except:
                        continue
                    sleep(8)
                    if len(chromeDriver.window_handles) >= 2:
                        switchToPage(chromeDriver, 1)
                        Sleep(1)
                        chromeDriver.close()
                        Sleep(2)
                        switchToPage(chromeDriver, 0)
                sleep(2)
            FindCoin(chromeDriver)
            readMarket(chromeDriver)


def getListExtension(exPath: str):
    listSub = os.listdir(exPath)
    listPath = ""
    total = len(listSub)
    for index, folder in enumerate(listSub):
        listPath = listPath+exPath+"/"+folder
        if index < total-1:
            listPath = listPath + ","
    return listPath


def switchToPage(chromeDriver, posPage):
    allHandles = chromeDriver.window_handles
    if posPage < len(allHandles):
        chromeDriver.switch_to.window(allHandles[posPage])
    sleep(1)


def goToWebsite(chromeDriver, link):
    chromeDriver.get(link)
    while chromeDriver.execute_script('return document.readyState') != 'complete':
        Sleep(2)


def closePage(chromeDriver, posClose, posGo):
    allHandles = chromeDriver.window_handles
    if posClose < len(allHandles):
        chromeDriver.switch_to.window(allHandles[posClose])
        chromeDriver.close()
    if posGo < len(allHandles):
        chromeDriver.switch_to.window(allHandles[posGo])
    sleep(1)


def dragAndDrop(chromeDriver, elem1, elem2):
    action_chains = ActionChains(chromeDriver)
    action_chains.drag_and_drop(elem1, elem2).perform()


def openWindow(chromeDriver, openURL):
    chromeDriver.execute_script("window.open('" + openURL + "', 'new_window')")


def openNewTab(chromeDriver, urlOpen):
    body = findElementByTagName(chromeDriver, "body")
    if body != "":
        body.send_keys(Keys.CONTROL + 't')
        body.send_keys(Keys.CONTROL + Keys.TAB)
        chromeDriver.get(urlOpen)


def moveToElement(chromeDriver, element):
    chromeDriver.execute_script("arguments[0].scrollIntoView();", element)


def scrollTo(chromeDriver):
    chromeDriver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


def executeScript(chromeDriver, scriptRun):
    chromeDriver.execute_script(scriptRun)


def waitPagetoLoad(chromeDriver):
    while chromeDriver.execute_script('return document.readyState') != 'complete':
        Sleep(2)


def moveToElementAndClick(chromeDriver, elem):
    if elem != "":
        actions = ActionChains(chromeDriver)
        actions.move_to_element(elem).click().perform()
    else:
        Utils.writeError("moveToElement: Element null")


def setValueInput(elem, dataInput):
    if elem != "":
        elem.send_keys(dataInput)
    else:
        Utils.writeError("setValueInput: Element null")


def clickButton(elem):
    if elem != "":
        elem.click()
    else:
        Utils.writeError("clickButton: Element null")


def findElementByTagName(chromeDriver, tagName):
    element = ""
    # 0.5s
    try:
        element = WebDriverWait(chromeDriver, TimeOut).until(
            EC.presence_of_element_located((By.TAG_NAME, tagName))
        )
    except NoSuchElementException as noE:
        Utils.writeError(noE.__class__)
    except TimeoutException as tE:
        Utils.writeError(tE.__class__)
    except Exception as ex:
        Utils.writeError(ex.__class__)
    return element


def findElementsByTagName(chromeDriver, tagName):
    element = ""
    # 0.5s
    try:
        element = WebDriverWait(chromeDriver, TimeOut).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, tagName))
        )
    except NoSuchElementException as noE:
        Utils.writeError(noE.__class__)
    except TimeoutException as tE:
        Utils.writeError(tE.__class__)
    except Exception as ex:
        Utils.writeError(ex.__class__)
    return element


def findElementById(chromeDriver, typeName):
    element = ""
    try:
        element = WebDriverWait(chromeDriver, TimeOut).until(
            EC.presence_of_element_located((By.ID, typeName))
        )
    except NoSuchElementException as noE:
        Utils.writeError(noE.__class__)
    except TimeoutException as tE:
        Utils.writeError(tE.__class__)
    except Exception as ex:
        Utils.writeError(ex.__class__)
    return element


def findElementsById(chromeDriver, typeName):
    element = ""
    try:
        element = WebDriverWait(chromeDriver, TimeOut).until(
            EC.presence_of_all_elements_located((By.ID, typeName))
        )
    except NoSuchElementException as noE:
        Utils.writeError(noE.__class__)
    except TimeoutException as tE:
        Utils.writeError(tE.__class__)
    except Exception as ex:
        Utils.writeError(ex.__class__)
    return element


def findElementByClass(chromeDriver, typeName):
    element = ""
    try:
        element = WebDriverWait(chromeDriver, TimeOut).until(
            EC.presence_of_element_located((By.CLASS_NAME, typeName))
        )
    except NoSuchElementException as noE:
        Utils.writeError(noE.__class__)
    except TimeoutException as tE:
        Utils.writeError(tE.__class__)
    except Exception as ex:
        Utils.writeError(ex.__class__)
    return element


def findElementsByClass(chromeDriver, typeName):
    element = ""
    try:
        element = WebDriverWait(chromeDriver, TimeOut).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, typeName))
        )
    except NoSuchElementException as noE:
        Utils.writeError(noE.__class__)
    except TimeoutException as tE:
        Utils.writeError(tE.__class__)
    except Exception as ex:
        Utils.writeError(ex.__class__)
    return element


def findElementByName(chromeDriver, typeName):
    element = ""
    try:
        element = WebDriverWait(chromeDriver, TimeOut).until(
            EC.presence_of_element_located((By.TAG_NAME, typeName))
        )
    except NoSuchElementException as noE:
        Utils.writeError(noE.__class__)
    except TimeoutException as tE:
        Utils.writeError(tE.__class__)
    except Exception as ex:
        Utils.writeError(ex.__class__)
    return element


def findElementsByName(chromeDriver, typeName):
    element = ""
    try:
        element = WebDriverWait(chromeDriver, TimeOut).until(
            EC.presence_of_all_elements_located((By.TAG_NAME, typeName))
        )
    except NoSuchElementException as noE:
        Utils.writeError(noE.__class__)
    except TimeoutException as tE:
        Utils.writeError(tE.__class__)
    except Exception as ex:
        Utils.writeError(ex.__class__)
    return element


def findElementByXpath(chromeDriver, typeName):
    element = ""
    try:
        element = WebDriverWait(chromeDriver, TimeOut).until(
            EC.presence_of_element_located((By.XPATH, typeName))
        )
    except NoSuchElementException as noE:
        Utils.writeError(noE.__class__)
    except TimeoutException as tE:
        Utils.writeError(tE.__class__)
    except Exception as ex:
        Utils.writeError(ex.__class__)
    return element


def findElementsByXpath(chromeDriver, typeName):
    element = ""
    try:
        element = WebDriverWait(chromeDriver, TimeOut).until(
            EC.presence_of_all_elements_located((By.XPATH, typeName))
        )
    except NoSuchElementException as noE:
        Utils.writeError(noE.__class__)
    except TimeoutException as tE:
        Utils.writeError(tE.__class__)
    except Exception as ex:
        Utils.writeError(ex.__class__)
    return element


def findElementByLink(chromeDriver, linkName):
    element = ""
    try:
        element = WebDriverWait(chromeDriver, TimeOut).until(
            EC.presence_of_element_located((By.LINK_TEXT, linkName))
        )
    except NoSuchElementException as noE:
        Utils.writeError(noE.__class__)
    except TimeoutException as tE:
        Utils.writeError(tE.__class__)
    except Exception as ex:
        Utils.writeError(ex.__class__)
    return element


def findElementsByLink(chromeDriver, linkName):
    element = ""
    try:
        element = WebDriverWait(chromeDriver, TimeOut).until(
            EC.presence_of_all_elements_located((By.LINK_TEXT, linkName))
        )
    except NoSuchElementException as noE:
        Utils.writeError(noE.__class__)
    except TimeoutException as tE:
        Utils.writeError(tE.__class__)
    except Exception as ex:
        Utils.writeError(ex.__class__)
    return element


def findElementByCssSelector(chromeDriver, typeName):
    element = ""
    try:
        element = WebDriverWait(chromeDriver, TimeOut).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, typeName))
        )
    except NoSuchElementException as noE:
        Utils.writeError(noE.__class__)
    except TimeoutException as tE:
        Utils.writeError(tE.__class__)
    except Exception as ex:
        Utils.writeError(ex.__class__)
    return element


def findElementsByCssSelector(chromeDriver, typeName):
    element = ""
    try:
        element = WebDriverWait(chromeDriver, TimeOut).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, typeName))
        )
    except NoSuchElementException as noE:
        Utils.writeError(noE.__class__)
    except TimeoutException as tE:
        Utils.writeError(tE.__class__)
    except Exception as ex:
        Utils.writeError(ex.__class__)
    return element


def findElementByInfo(chromeDriver, target):
    element = ""
    if target.find("xpath") >= 0:
        xpath = target.replace("xpath=", "")
        element = findElementByXpath(chromeDriver, xpath)
    elif target.find("link") >= 0:
        link = target.replace("link=", "")
        element = findElementByLink(chromeDriver, link)
    if element != "":
        actions = ActionChains(chromeDriver)
        actions.move_to_element(element).perform()
    return element


def Sleep(timeSleep):
    sleep(timeSleep + random.randint(10, 200) / 1000)
