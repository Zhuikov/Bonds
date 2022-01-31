import abc

""" Stores uninitialized bonds """
class BondRepository(metaclass=abc.ABCMeta):

    def __init__(self) -> None:
        self._bondStoredFields = {"bondGroup", "number", "description"}
        self._bonds = self._initBonds()

    @abc.abstractmethod
    def _initBonds(self) -> set:
        """Read and return set of bonds"""

    @abc.abstractmethod
    def commit(self):
        """Save self._bonds"""

    def add(self, bond):
        for b in self._bonds:
            if b == bond:
                b += bond
                return
        self._bonds.add(bond)

    def remove(self, secid: str):
        bondToRemove = next((b for b in self._bonds if b.secid == secid), None)
        self._bonds.discard(bondToRemove)

    def get(self, secid):
        bond = next((b for b in self._bonds if b.secid == secid), None)
        return bond

    def getAll(self):
        # copy set
        return {b for b in self._bonds}

    def update(self, secid, **kwargs):
        bondToUpdate = next((b for b in self._bonds if b.secid == secid), None)
        if not bondToUpdate:
            raise ValueError("Bond %s not found" % secid)
        for k, v in kwargs.items():
            if k in self._bondStoredFields:
                bondToUpdate.__setattr__(k, v)
