from .BondRepository import BondRepository

import bonds
import json
import os

class BondRepositoryJson(BondRepository):

    def __init__(self, jsonpath):
        self._jsonpath = jsonpath
        super().__init__()

    def _initBonds(self) -> set:
        if not os.path.isfile(self._jsonpath) or os.stat(self._jsonpath).st_size == 0:
            return set()

        with open(self._jsonpath, "r") as inp:
            _bonds = json.load(inp)

        if not isinstance(_bonds, list):
            raise ValueError("Object in %s must be a 'list'" % self._jsonpath)

        return set((self.__bondFromObj(b) for b in _bonds))

    def commit(self):
        bondsObjects = [self.__bondToObj(b) for b in self._bonds]
        with open(self._jsonpath, "w") as outp:
            json.dump(bondsObjects, outp)

    @staticmethod
    def __bondFromObj(obj) -> bonds.Bond:
        # TODO check obj keys
        secid = obj["secid"]
        descr = obj["description"]
        number = obj["number"]
        group = bonds.BondGroup.fromString(obj["group"])
        return bonds.Bond(secid, number, group, descr)

    @staticmethod
    def __bondToObj(bond: bonds.Bond):
        return {
            "secid": bond.secid,
            "description": bond.description,
            "number": bond.number,
            "group": str(bond.bondGroup)
        }
