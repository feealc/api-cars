import datetime


class Generic:

    @staticmethod
    def get_current_date():
        return int(datetime.datetime.now().strftime('%Y%m%d'))
