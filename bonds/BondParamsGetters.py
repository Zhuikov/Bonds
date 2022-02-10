import abc
import asyncio
import datetime
import enum
import functools
import json
import requests

from .BondParams import BondParams

class ParamsGetter(metaclass=abc.ABCMeta):
    @abc.abstractstaticmethod
    async def getBondParams(secid) -> BondParams:
        "receive and return BondParams"

class ParamsGetterMoex(ParamsGetter):
    url = "https://iss.moex.com/iss/engines/stock/markets/bonds/securities/%s.json"
    queryParams = {"iss.meta": "off", "iss.only": "securities,marketdata"}

    @staticmethod
    async def getBondParams(secid) -> BondParams:
        requestUrl = ParamsGetterMoex.url % secid
        loop = asyncio.get_event_loop()
        future = loop.run_in_executor(
            None,
            functools.partial(requests.get, requestUrl, params=ParamsGetterMoex.queryParams)
        )

        response = await future
        if future.exception():
            raise future.exception()
        if response.status_code != 200:
            # TODO
            print("Bad response")
        return ParamsGetterMoex.__parseResponse(response.text)

    @staticmethod
    def __parseResponse(responseBody) -> BondParams:
        obj = json.loads(responseBody)
        securities = dict(zip(obj["securities"]["columns"], obj["securities"]["data"][0]))
        marketdata = dict(zip(obj["marketdata"]["columns"], obj["marketdata"]["data"][0]))
        bondParams = BondParams()
        bondParams.name = securities["SECNAME"]
        bondParams.faceValue = securities["FACEVALUE"]
        bondParams.marketPrice = marketdata["MARKETPRICE"]
        bondParams.accruedInt = securities["ACCRUEDINT"]
        bondParams.couponValue = securities["COUPONVALUE"]
        bondParams.couponNext = datetime.datetime.strptime(securities["NEXTCOUPON"], "%Y-%m-%d").date()
        bondParams.couponPeriod = securities["COUPONPERIOD"]
        bondParams.matdate = datetime.datetime.strptime(securities["MATDATE"], "%Y-%m-%d").date()
        bondParams.duration = marketdata["DURATION"]

        return bondParams

class ParamsGetterType(enum.Enum):
    MOEX_GETTER = enum.auto()

    def getParamGetterFunction(self, type2func={
            MOEX_GETTER: ParamsGetterMoex.getBondParams
    }):
        return type2func.get(self.value, None)
