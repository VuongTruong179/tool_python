from modules.BaseController import BaseController
from modules.guide.guideView import GuideView


class GuideController(BaseController):
    def __init__(self) -> None:
        self.view = None

    def bind(self, view: GuideView):
        self.view = view
        self.view.initView(None)
