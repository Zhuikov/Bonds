import asyncio
import functools
import json
from .Bond import Bond
from .BondParamsGetters import ParamsGetterType

class CorruptedBondRepresentation(Exception):
    def __init__(self, msg, errors) -> None:
        super().__init__(msg)
        self.errors = errors

class BondManager:

    def __init__(self, jsonPath) -> None:
        with open(jsonPath, "r") as inp:
            # TODO try-except json.load
            bonds = json.load(inp)

        if not isinstance(bonds, list):
            raise ValueError("Bonds must be a 'list' object")

        errors = self.__checkBonds(bonds)
        if errors:
            raise CorruptedBondRepresentation(
                "Corrupted bond representation (see exception's 'errors' field)", errors)

        self._bonds = [Bond.fromObj(o) for o in bonds]
        self._bondsPath = jsonPath

    async def initializeBondsParams(self, getterType=ParamsGetterType.MOEX_GETTER, timeout=2):
        if not self._bonds:
            print("Bonds not found in %s" % self._bondsPath)
            return False

        futures = [b.initializeBondParams(getterType) for b in self._bonds]
        done, pending = await asyncio.wait(futures, timeout=timeout)

        if pending:
            notInitBonds = ", ".join([b.secid for b in self._bonds if not b.paramsInitialized])
            print("Warning: following bonds are not initialized: %s" % notInitBonds)

        return len(done) == len(self._bonds)

    async def add(self, secid, init=False):
        

    def remove(self, secid: str):
        pass

    def getAll(self):
        pass

    def update(self, bond):
        pass

    def __checkBonds(self, bonds):
        return []
