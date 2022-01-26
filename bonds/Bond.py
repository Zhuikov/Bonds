import enum

from .BondParams import BondParams
from .BondParamsGetters import ParamsGetterMoex, ParamsGetterType


class BondLabel(enum.Enum):
    IN_STOCK = enum.auto()
    PLANNED = enum.auto()

    @classmethod
    def fromString(cls, s):
        try:
            return cls[s.upper]
        except KeyError:
            print("Unknown BondLabel: %s" % s)
            return None


class Bond:

    getterFunc = {
        ParamsGetterType.MOEX_GETTER: ParamsGetterMoex.getBondParams
    }

    def __init__(self, secid, bondLabel=BondLabel.IN_STOCK, number=0, description=""):
        self.secid = secid
        self.bondLabel = bondLabel
        self.number = number
        self.description = description
        self.params = BondParams()

        self.paramsInitialized = False

    async def initializeBondParams(self, getterType=ParamsGetterType.MOEX_GETTER):
        if self.paramsInitialized:
            return
        try:
            self.params = await self.getterFunc[getterType](self.secid)
            self.paramsInitialized = True
        except Exception as e:
            print("Error while bond params initialization")
            raise e

    @classmethod
    def fromObj(cls, obj):
        secid = obj["secid"]
        descr = obj["description"]
        number = obj["number"]
        label = BondLabel.fromString(obj["label"])
        return cls(secid, label, number, descr)


    def __str__(self) -> str:
        s = "%s: '%s' (%s)\n  " % (self.secid, self.description, self.number)
        s += str(self.params) if self.paramsInitialized else "not initialized"
        return s
