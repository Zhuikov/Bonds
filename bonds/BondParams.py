import datetime

class BondParams:
    def __init__(self) -> None:
        self.name = ""
        self.faceValue = 0
        self.marketPrice = 0
        self.accruedInt = 0
        self.couponValue = 0
        self.couponNext = datetime.date(1970, 1, 1)
        self.couponPeriod = 0
        self.matdate = datetime.datetime(1970, 1, 1)
        self.duration = 0

    def __str__(self) -> str:
        return f"{self.name} -- {self.marketPrice}% ({self.faceValue}), coupon: {self.couponValue}"
