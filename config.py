class Setting:
    def __init__(self, value):
        self.value = value

    def __get__(self, instance, owner):
        return self.value


class Config:
    MAX_OFFLINE_TIME = Setting(300)
    RETRY_INTERVAL = Setting(5)
    SOCKET_TIMEOUT = Setting(300)


config = Config()
