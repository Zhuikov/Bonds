import abc

class CorruptedBondRepresentation(Exception):
    def __init__(self, msg, errors) -> None:
        super().__init__(msg)
        self.errors = errors


class BondRepository(metaclass=abc.ABCMeta):
    """ Stores uninitialized bonds """

    def __init__(self) -> None:
        self._bondStoredFields = {"bondGroup", "number", "description"}
        self._bonds = self._initBonds()

    @abc.abstractmethod
    def _initBonds(self) -> set:
        """Read and return set of bonds"""

    @abc.abstractmethod
    def commit(self):
        """Save self._bonds"""

    def add(self, *args):
        for bond in args:
            self.__add(bond)

    def __add(self, bond):
        if bond in self._bonds:
            b = next(_ for _ in self._bonds if _ == bond)
            # b.number = 0
            b += bond
        else:
            self._bonds.add(bond)

    def remove(self, secid, bondGroup):
        bondToRemove = next((b for b in self._bonds if b.secid == secid and b.bondGroup is bondGroup), None)
        self._bonds.discard(bondToRemove)

    def get(self, secid, bondGroup):
        bond = next((b for b in self._bonds if b.secid == secid and b.bondGroup is bondGroup), None)
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
