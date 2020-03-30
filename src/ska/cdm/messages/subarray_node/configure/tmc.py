from datetime import timedelta


class TMCConfiguration:
    def __init__(self, scan_duration: timedelta):
        self.scan_duration = scan_duration
