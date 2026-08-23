class BacktestError(Exception):
    pass


class InvalidTickerError(BacktestError):
    pass


class InvalidDateRangeError(BacktestError):
    pass
