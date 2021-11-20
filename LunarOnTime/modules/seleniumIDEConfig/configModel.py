class Profile:
    stt = 0
    email = ""
    emailPass = ""
    fullName = ""
    profile = ""
    proxy = ""
    proxyUser = ""
    proxyPass = ""
    phone = ""
    twitterAccount = ""
    twitterPassword = ""
    telegramAccount = ""
    telegramPassword = ""
    walletAddress = ""
    discordAccount = ""
    discordPass = ""
    insAccount = ""
    insPass = ""
    cmcName = ""
    cmcPass = ""


from base.utils import ExcelManager


class ProfileExcel(object):
    def __init__(self) -> None:
        self.listProfile = []

    def getListProfile(self, path: str, sheet: str):
        self.listProfile = []
        listData = ExcelManager.readFileExcel(path, sheet)
        listEmail = listData["Email"]
        listEmailPass = listData["Pass"]
        listFullName = listData["Full name"]
        listProfile = listData["Profile"]
        listProxy = listData["Proxy"]
        listProxyUser = listData["Proxy User"]
        listProxyPass = listData["Proxy Pass"]
        listPhone = listData["Phone"]
        listTwitterAccount = listData["Twitter Account"]
        listTwitterPass = listData["TW pass"]
        listTelegramAccount = listData["Telegram"]
        listWalletAddress = listData["BEP-20 Wallet Address"]
        listDiscordAccount = listData["Discord Account"]
        listDiscordPass = listData["Discord Pass"]
        listInsAccount = listData["Ins Account"]
        listInsPass = listData["Ins Pass"]
        listCmcAccount = listData["CMC Name"]
        listCmcPass = listData["CMC Pass"]
        for index, item in enumerate(listEmail):
            profile = Profile()
            profile.email = listEmail[index]
            profile.emailPass = listEmailPass[index]
            profile.fullName = listFullName[index]
            profile.profile = listProfile[index]
            profile.proxy = listProxy[index]
            profile.proxyUser = listProxyUser[index]
            profile.proxyPass = listProxyPass[index]
            profile.phone = str(listPhone[index])
            profile.twitterAccount = listTwitterAccount[index]
            profile.twitterPassword = listTwitterPass[index]
            profile.telegramAccount = listTelegramAccount[index]
            profile.walletAddress = listWalletAddress[index]
            profile.discordAccount = listDiscordAccount[index]
            profile.discordPass = listDiscordPass[index]
            profile.insAccount = listInsAccount[index]
            profile.insPass = listInsPass[index]
            profile.cmcName = listCmcAccount[index]
            profile.cmcPass = listCmcPass[index]
            self.listProfile.append(profile)
        return self.listProfile

    def getListDataExcel(self, path: str, sheet: str):
        listData = ExcelManager.readFileExcel(path, sheet)
        self.listProfile = listData.to_dict('records')
        return self.listProfile
