# SPDX-License-Identifier: CC0-1.0
# Copyright (c) 12021-12021 HE, Scott McCallum <https://github.com/scott91e1>
# To the extent possible under law, Scott McCallum has waived all copyright and 
# related or neighboring rights to [ fungeit EMPORIA ]. This work is published
# from <https://what3words.com/enablers.aromas.import> Australia & New Zealand.
#

import os, re, rich, trio, toml, arrow, redio

from hypercorn.trio import serve
from hypercorn.config import Config

from quart import Quart
from quart_trio import QuartTrio
from quart_schema import QuartSchema, validate_request, validate_response

from pydantic import BaseModel
from pydantic.dataclasses import dataclass

from typing import Any, IO, Optional, List

from dotenv import load_dotenv
load_dotenv(verbose=True)

hypercorn_config = Config()
hypercorn_config.bind = [os.getenv("EMPORIA_BIND", "localhost:10000")]

app = QuartTrio("EMPORIA")
QuartSchema(app, version="0.42.10", title="fungeit EMPORIAv1-CORE")

redis = redio.Redis("redis://localhost/")

#from env_guard import *
#from key_guard import load_keyguard, print, Guard
#load_keyguard()

import toml
env_guard_db = toml.load(os.getenv("ENV-GUARD", "C:\\ENV-GUARD.toml"))

env_guard_re = []
def setup_guard_re():
    for k in env_guard_db.keys():
        v = env_guard_db[k]
        if isinstance(v, dict):
            for k2, v2 in v.items():
                env_guard_re.append((re.escape(v2),"[red][r]"+k2+"[/r][/red]"))
        else:
            env_guard_re.append((re.escape(v),"[red][r]"+k+"[/r][/red]"))

setup_guard_re()

def print(*objects: Any, sep=" ", end="\n", file: IO[str] = None, flush: bool = False):
    guarded = []
    for o in objects:
        if isinstance(o, str):
            for k, v in env_guard_re:
                o = re.sub(k, v, o)
        guarded.append(o)
    rich.print(*guarded, sep=sep, end=end, file=file, flush=flush)

#print(env_guard_db)

def env_guard(secret):
    for k in env_guard_db.keys():
        v = env_guard_db[k]
        if isinstance(v,dict) and k == os.getcwd() and secret in v:
            return v[secret]

    if secret in env_guard_db:
        return env_guard_db[secret]

    return secret


#print("DATABASE_URL=", "FOO"+DATABASE_URL+"BAR")

@dataclass
class Schema_APIvX0:
    name: str

@dataclass
class Schema_DATAvX0:
    epoch: str


@dataclass
class Enter_APIvX0:
    name: str

@dataclass
class Enter_DATAvX0:
    epoch: str

@dataclass
class Offer_APIvX0:
    name: str

@dataclass
class Offer_DATAvX0:
    epoch: str

@dataclass
class Leave_APIvX0:
    name: str

@dataclass
class Leave_DATAvX0:
    epoch: str

class Emporium:

    def __init__(self, name, **kw):

        self.name = name

        for k, v in kw.items():
            self.__dict__[k] = v

        self.epoch = None
        self.cache = {}

    async def maintain(self, stop:bool=False):

        if stop:
            self.stop = True
            return

        sleep_time = 0.33

        #db = redis()
        #db.set(self.name, count)
        #await db

        self.stop = False
        while not self.stop:
            utcnow = arrow.utcnow()
            print(utcnow)
            await trio.sleep(sleep_time)

    async def route_SCHEMAvX0(self, api: Schema_APIvX0, **kw) -> Schema_DATAvX0:
        data = {}
        data["epoch"] = ""
        await trio.sleep(0)
        return Schema_DATAvX0(**data)

    async def route_ENTERvX0(self, api: Enter_APIvX0, **kw) -> Enter_DATAvX0:
        data = {}
        data["epoch"] = ""
        await trio.sleep(0)
        return Enter_DATAvX0(**data)

    async def route_OFFERvX0(self, api: Offer_APIvX0, **kw) -> Offer_DATAvX0:
        data = {}
        data["epoch"] = ""
        await trio.sleep(0)
        return Offer_DATAvX0(**data)

    async def route_LEAVEvX0(self, api: Leave_APIvX0, **kw) -> Leave_DATAvX0:
        data = {}
        data["epoch"] = ""
        await trio.sleep(0)
        return Leave_DATAvX0(**data)


emporia = {}
emporia["0"] = Emporium("0") 

@app.route("/e10/SCHEMA", methods=["POST"])
@validate_request(Schema_APIvX0)
@validate_response(Schema_DATAvX0, 200)
async def e10_Query_Rules(data: Schema_APIvX0) -> Schema_DATAvX0:
    """
    
"Plan and prepare for every possibility, and you will never act. 
It is nobler to have courage as we stumble into half the things
we fear than to analyse every possible obstacle and begin nothing.
Great things are achieved by embracing great dangers."

    """
    # Do something with data, e.g. save to the DB
    return Schema_DATAvX0(epoch="?")

@app.route("/e10/Apparatus/0.ENTER", methods=["POST"])
@validate_request(Enter_APIvX0)
@validate_response(Schema_DATAvX0, 200)
async def app_ENTER(data: Schema_APIvX0) -> Schema_DATAvX0:
    """

Traders call this API to signal they want to join the next round.

The server responds with a token and the time they should sleep
before calling the next stage with the offer details.

    """
    try:
        await emporia[data.name].route_ENTERvX0(api=data)
    except:
        abort(400)


@app.route("/e10/Apparatus/1.OFFER", methods=["POST"])
@validate_request(Offer_APIvX0)
@validate_response(Offer_DATAvX0, 200)
async def app_OFFER(data: Offer_APIvX0) -> Offer_DATAvX0:
    """

Offers contain retroforth programs that act on behalf of account hoders
to buy and sell items in the emporia.  These offers are binding and are
executed in a very specific order.  You cannot sell things you dont own
and you cannot make bids with more funds than you have on record at the
exchange.

A single POST may contain thousands of programs where the account holder
has been given permission to act on behalf of someone.

The reply again contains a sleep time that the client must wait before
calling the final API to leave the round and download the results.

    """
    try:
        await emporia[data.name].route_OFFERvX0(api=data)
    except:
        abort(400)


@app.route("/e10/Apparatus/2.LEAVE", methods=["POST"])
@validate_request(Leave_APIvX0)
@validate_response(Leave_DATAvX0, 200)
async def app_LEAVE(data: Leave_APIvX0) -> Leave_DATAvX0:
    """

After the matching engine has run, the results are made available for
download over various systems.  As the size of the market increases it
the size of the completed round is expected to be significant.

This request also contains details of how the programs performed and
the contents of the virtual "screen" that may contain information
useful to the customer.

    """
    try:
        await emporia[data.name].route_LEAVEvX0(api=data)
    except:
        abort(400)


async def app_worker():
    while True:
        async with trio.open_nursery() as nursery:
            for name, emporium in emporia.items():
                nursery.start_soon(emporium.maintain)

async def app_serve(*args):
    async with trio.open_nursery() as nursery:
        nursery.start_soon(serve, *args)
        nursery.start_soon(app_worker)

trio.run(app_serve, app, hypercorn_config)