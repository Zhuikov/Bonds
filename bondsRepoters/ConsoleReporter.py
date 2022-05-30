from itertools import chain


class ConsoleReporter:
    # TODO check lists in set*
    # TODO add translated field names

    def __init__(self):
        self._bondParamsFieldsList = ["name", "marketPrice", "accruedInt", "couponNext", "matdate"]
        self._bondFiledsList = ["bondGroup", "number", "description"]

    def report(self, bonds, sortBy="couponNext"):
        # TODO implement 'sortBy'
        allFields = list(chain(self._bondParamsFieldsList, self._bondFiledsList))
        if sortBy not in allFields:
            raise ValueError(f"'sortBy = {sortBy}' not found in bondFiledsList and in bondParamsFieldsList")
        cellsLengths = [tuple(map(len, allFields))]
        rows = []
        for b in bonds:
            bondRowDict = self.__getRowFromBond(b)
            rows.append(bondRowDict)
            cellsLengths.append(tuple(map(len, (str(bondRowDict[k]) for k in allFields))))
        maxLengths = tuple(map(max, zip(*cellsLengths)))
        formatStr = "|%s" * len(allFields) + "|"
        header = formatStr % tuple(paramName.center(l) for paramName, l in zip(allFields, maxLengths))
        print("=" * len(header))
        print(header)
        print("+%s+" % ("-" * (len(header) - 2)))
        for r in rows:
            row = formatStr % tuple(str(v).center(l) for v, l in zip(r.values(), maxLengths))
            print(row)
        print("+%s+" % ("-" * (len(header) - 2)))

    def setBondFieldsList(self, l):
        self._bondFiledsList = l

    def setBondParamsFieldsList(self, l):
        self._bondParamsFieldsList = l

    def __getRowFromBond(self, bond):
        res = {}
        for field in self._bondParamsFieldsList:
            res[field] = getattr(bond.params, field)
        for field in self._bondFiledsList:
            res[field] = getattr(bond, field)
        return res
