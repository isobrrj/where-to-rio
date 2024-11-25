import abc


class ScreenTemplate(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def show_window(self):
        pass
