from threading import Timer


class Alerts:
    '''
    This is a simple utility that generate the variables "alert" and "alert_type"
    and resets itself after 3 seconds.
    '''
    def __init__(self) -> None:
        self.__alert = ''
        self.__alert_type = ''

    def new_alert(self, alert: str, alert_type: str) -> None:
        if alert_type not in ['success', 'warning']:
            return
        self.__alert = alert
        self.__alert_type = alert_type
        Timer(3.6, self.__reset).start()

    def get_alert(self) -> tuple[str, str]:
        return self.__alert, self.__alert_type

    def __reset(self):
        self.__alert = ''
        self.__alert_type = ''