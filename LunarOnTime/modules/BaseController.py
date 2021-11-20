from abc import ABC, abstractmethod

from modules.BaseView import BaseView


class BaseController(ABC):

    @abstractmethod
    def bind(view: BaseView):
        raise NotImplementedError
