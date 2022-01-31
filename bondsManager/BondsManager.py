import asyncio
import json
import bonds
from bonds.BondParamsGetters import ParamsGetterType

class CorruptedBondRepresentation(Exception):
    def __init__(self, msg, errors) -> None:
        super().__init__(msg)
        self.errors = errors

class BondManager:

    def __init__(self, bondRepository):
        self._repository = bondRepository
        self._bonds = self._repository.getAll() # ???

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
