import enum

from .BondParams import BondParams
from .BondParamsGetters import ParamsGetterType


class BondGroup(enum.Enum):
    IN_STOCK = enum.auto()
    PLANNED = enum.auto()

    @classmethod
    def fromString(cls, s):
        try:
            return cls[s.upper()]
        except KeyError:
            print("Unknown BondGroup: %s" % s)
            return None

    def __str__(self):
        return self.name.lower()


class Bond:

    def __init__(self, secid, number=0, bondGroup=BondGroup.IN_STOCK, description=""):
        self.secid = secid
        self.number = number
        self.bondGroup = bondGroup
        self.description = description
        self.params = BondParams()

        self.paramsInitialized = False

    async def initializeBondParams(self, getterType=ParamsGetterType.MOEX_GETTER):
        if self.paramsInitialized:
            return
        try:
            self.params = await getterType.getParamGetterFunction()(self.secid)
            self.paramsInitialized = True
        except Exception as e:
            print("Error while bond params initialization")
            raise e

    def __eq__(self, o):
        return self.secid == o.secid and self.bondGroup == o.bondGroup

    def __hash__(self):
        return hash((self.secid, self.bondGroup))

    def __add__(self, o):
        if self != o:
            raise ValueError("To add bonds they must be equal")
        return Bond(self.secid, self.number + o.number, self.bondGroup, o.description)

    def __str__(self) -> str:
        s = "%s: '%s' (%s)\n  " % (self.secid, self.description, self.number)
        s += str(self.params) if self.paramsInitialized else "not initialized"
        return s
