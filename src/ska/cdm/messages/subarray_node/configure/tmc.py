from datetime import timedelta


class TMCConfiguration:
    def __init__(self, scan_duration: timedelta):
        self.scan_duration = scan_duration

    def __eq__(self, other):
        if not isinstance(other, TMCConfiguration):
            return False
        return self.scan_duration == other.scan_duration