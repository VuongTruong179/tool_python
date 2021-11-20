import os
import threading
import tkinter.messagebox as tkmsg
from time import sleep
from base.model.ChromeProfile import ChromeProfile
from base.seleniumManager import SeleniumManager
from base.utils import Utils
from modules.BaseController import BaseController
from modules.seleniumIDE.autoSeleView import AutoSeleView
from modules.seleniumIDEConfig.configModel import ProfileExcel


def getLinkChrome(posProfile, chromePath):
    listSub = os.listdir(chromePath)
    total = len(listSub)
    pos = posProfile % total
    return chromePath + "/" + listSub[pos] + "/App/Chrome-bin/chrome.exe"


def openNewChrome(linkWeb, configInfo, profileInfo, posThread, numThreads):
    linkChrome = getLinkChrome(int(profileInfo.get("STT")), configInfo["chromePath"])
    chromeProfile = ChromeProfile()
    chromeProfile.chromePath = linkChrome
    chromeProfile.webRtcPath = configInfo["webRtcPath"]
    chromeProfile.profilePath = configInfo["profilePath"] + "/" + profileInfo.get("Profile")
    chromeProfile.ipaddress = profileInfo.get("Proxy")
    chromeProfile.urlOpen = linkWeb
    chromeDriver = SeleniumManager.createNewChrome(chromeProfile, posThread, numThreads)
    try:
        chromeDriver.get(chromeProfile.urlOpen)
        chromeDriver.switch_to.window(chromeDriver.current_window_handle)
    except Exception as ex:
        Utils.writeError("Thong tin: " + str(profileInfo))
        Utils.writeError(str(ex))
        try:
            chromeDriver.close()
        except Exception:
            Utils.writeError("Error Close chrome")
        finally:
            try:
                chromeDriver.quit()
                return ""
            except Exception:
                Utils.writeError("Error Exit chrome")

    return chromeDriver


def getValueFromKey(keyword, profileInfo, listKeywords):
    key = listKeywords.get(keyword)
    value = profileInfo.get(key)
    return str(value)


def runScript(configInfo, profileInfo, listKeywords, listLock, views, posThread, numThreads):
    isSuccess = True
    listStatusScript = list()
    listScript = Utils.readFileJson(configInfo["scriptPath"])
    listLock.acquire()
    try:
        views.setValueForItemScript(posThread, "lbIp", profileInfo.get("Proxy"))
        views.setValueForItemScript(posThread, "lbEmail", profileInfo.get("Email"))
        chromeDriver = openNewChrome(listScript[0]["target"], configInfo, profileInfo, posThread, numThreads)
    except StopIteration:
        return
    finally:
        # release the Lock, so other thread can gain the Lock to access list_num
        listLock.release()
    if chromeDriver == "":
        return
    try:
        chromeDriver.switch_to.window(chromeDriver.window_handles[0])
        for scriptInfo in listScript:
            valueSend = scriptInfo["value"]
            scriptResult = {
                "type": scriptInfo["command"],
                "code": scriptInfo["target"],
                "status": True
            }
            if scriptInfo["command"] == "open":
                continue
            elif scriptInfo["command"] == "scroll":
                SeleniumManager.scrollTo(chromeDriver)
            elif scriptInfo["command"] == "sleep":
                sleep(int(valueSend))
            elif scriptInfo["command"] == "open_tab":
                SeleniumManager.openWindow(chromeDriver, valueSend)
            elif scriptInfo["command"] == "switch_tab":
                SeleniumManager.switchToPage(chromeDriver, int(valueSend))
            elif scriptInfo["command"] == "StartAuto":
                SeleniumManager.StartAutoTimeOnSite(chromeDriver, listLock)
            elif scriptInfo["command"] == "close_tab":
                listPos = valueSend.split(",")
                if len(listPos) > 1:
                    SeleniumManager.closePage(chromeDriver, int(listPos[0]), int(listPos[1]))
            else:
                element = SeleniumManager.findElementByInfo(chromeDriver, scriptInfo["target"])
                if element != "":
                    if scriptInfo["command"] == "click":
                        SeleniumManager.clickButton(element)
                    elif scriptInfo["command"] == "type":
                        valueInput = getValueFromKey(valueSend, profileInfo, listKeywords)
                        scriptResult["code"] = valueInput
                        SeleniumManager.setValueInput(element, valueInput)
                    else:
                        isSuccess = False
                        Utils.writeError(str(scriptInfo))

                    # Update list script
                    if len(listStatusScript) > views.getMaxLine():
                        listStatusScript.pop(0)
                    listStatusScript.append(scriptResult)
                    views.updateListResultStatus(posThread, listStatusScript)
                    # End
                else:
                    isSuccess = False

            # Update list script
            scriptResult["status"] = isSuccess
            if len(listStatusScript) > views.getMaxLine():
                listStatusScript.pop(0)
            listStatusScript.append(scriptResult)
            views.updateListResultStatus(posThread, listStatusScript)
            if isSuccess:
                SeleniumManager.Sleep(int(configInfo["timeDelay"]))
            else:
                break
            # End
    except Exception as ex:
        isSuccess = False
        scriptResult = {
            "type": "Exception",
            "code": str(ex),
            "status": False
        }
        if len(listStatusScript) > views.getMaxLine():
            listStatusScript.pop(0)
        listStatusScript.append(scriptResult)
        views.updateListResultStatus(posThread, listStatusScript)
        Utils.writeError(str(ex))
    finally:
        try:
            chromeDriver.close()
        except Exception:
            Utils.writeError("Error Close chrome")
        finally:
            try:
                chromeDriver.quit()
            except Exception:
                Utils.writeError("Error Exit chrome")
            finally:
                return isSuccess


class RunSelenium(threading.Thread):

    def __init__(self, configInfo, listProfile, listLock, listKeywords, view, posThread, numThreads):
        threading.Thread.__init__(self)
        self._listKeywords = listKeywords
        self._configInfo = configInfo
        self._listProfile = listProfile
        self._list_lock = listLock
        self._view = view
        self._posThread = posThread
        self._numThreads = numThreads

    def run(self):
        TotalRun = 0
        SuccessRun = 0
        self._view.setValueForItemScript(self._posThread, "status", "Đang chạy", "green")

        while True:

            # request to access shared resource
            # if there are many threads acquiring Lock, only one thread get the Lock
            # and other threads will get blocked
            self._list_lock.acquire()
            try:
                profileInfo = next(self._listProfile)
            except StopIteration:
                self._view.setValueForItemScript(self._posThread, "status", "Kết thúc", "black")
                return
            finally:
                # release the Lock, so other thread can gain the Lock to access list_num
                self._list_lock.release()
            TotalRun += 1
            self._view.resetListResultStatus(self._posThread)
            isSuccess = runScript(self._configInfo, profileInfo, self._listKeywords, self._list_lock, self._view,
                                  self._posThread, self._numThreads)
            if isSuccess:
                SuccessRun += 1
            self._view.setValueForItemScript(self._posThread, "rate", str(SuccessRun) + "/" + str(TotalRun))


class AutoSeleController(BaseController):
    def __init__(self) -> None:
        self.view = None
        self.isRunning = False
        self.isRunningRetweet = False
        self.entriesConfigValues = None
        self.model = ProfileExcel()
        self.listProfile = iter([])
        self.ListKeywords = {}

    def bind(self, view: AutoSeleView):
        self.view = view
        self.view.initView(None)
        self.btnRunAuto()

    def validateEntries(self):
        isvalid = False
        if self.entriesConfigValues["profilePath"] == "" or self.entriesConfigValues["profilePath"] is None:
            tkmsg.showerror(
                title="Validation Error", message=f"Vui lòng nhập đường dẫn lưu Profile"
            )
        elif self.entriesConfigValues["proxyPath"] == "" or self.entriesConfigValues["proxyPath"] is None:
            tkmsg.showerror(
                title="Validation Error", message=f"Vui lòng nhập đường dẫn file Proxy"
            )
        elif self.entriesConfigValues["webRtcPath"] == "" or self.entriesConfigValues["webRtcPath"] is None:
            tkmsg.showerror(
                title="Validation Error", message=f"Vui lòng nhập đường dẫn thư mục Extension"
            )
        elif self.entriesConfigValues["proxySheet"] == "" or self.entriesConfigValues["proxySheet"] is None:
            tkmsg.showerror(
                title="Validation Error", message=f"Vui lòng nhập tên Sheet"
            )
        elif self.entriesConfigValues["scriptPath"] == "" or self.entriesConfigValues["scriptPath"] is None:
            tkmsg.showerror(
                title="Validation Error", message=f"Vui lòng nhập đường dẫn file Script"
            )
        elif self.entriesConfigValues["maxThread"] is None or int(self.entriesConfigValues["maxThread"]) <= 0:
            tkmsg.showerror(
                title="Validation Error", message=f"Vui lòng nhập số luồng"
            )
        elif self.entriesConfigValues["timeDelay"] is None or int(self.entriesConfigValues["timeDelay"]) <= 0:
            tkmsg.showerror(
                title="Validation Error", message=f"Vui lòng nhập thời gian chờ"
            )
        else:
            isvalid = True
        return isvalid

    def btnRunAuto(self):
        if self.isRunning:
            tkmsg.showerror(title="Đợi Em Ơi", message=f"Vui lòng đợi các luồng hoàn thành!")
        else:
            self.isRunning = True
            self.entriesConfigValues = Utils.readFileJson("./config.json")
            if self.validateEntries():
                self.ListKeywords = Utils.readFileJson(self.entriesConfigValues["keyPath"])
                self.listProfile = iter(self.model.getListDataExcel(self.entriesConfigValues["proxyPath"],
                                                                    self.entriesConfigValues["proxySheet"]))
                thread = threading.Thread(target=self.startRunAuto)
                thread.start()

    def startRunAuto(self):
        # Validate number thread
        numThreads = int(self.entriesConfigValues["maxThread"])
        listLock = threading.Lock()
        threads = []
        if numThreads is None:
            try:
                numThreads = os.cpu_count()
            except AttributeError:
                numThreads = 5

        elif numThreads < 1:
            raise ValueError('num_threads must be > 0')
        # End
        self.view.createItemScriptRun(numThreads)

        # Run multi thread
        for i in range(numThreads):
            thread = RunSelenium(self.entriesConfigValues, self.listProfile, listLock, self.ListKeywords, self.view, i, numThreads)
            threads.append(thread)
            thread.start()
            sleep(1)
        # End

        # Wait All Thread
        for thread in threads:
            thread.join()
            self.isRunning = False
        # End
