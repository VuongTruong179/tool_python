class ChromeProfile:
    chromePath = ""
    profilePath = "profiles"
    webRtcPath = "webrtcleak"
    ipaddress = ""
    posThread = 0
    maxThread = 5
    userAgent = "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19"
    language = "en"
    locale = "en"
    width = 1920
    height = 1080
    posX = 0
    posY = 0
    urlOpen = "https://browserleaks.com/ip"

    def __init__(self) -> None:
        super().__init__()

    # def __del__(self):
    #     print('Class Person được hủy')
    #     del self.profilePath, self.ipaddress, self.posThread, self.maxThread, self.userAgent, self.language, self.width, self.height
