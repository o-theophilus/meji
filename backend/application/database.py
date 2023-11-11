from flask import current_app
from deta import Deta
import os


def base(db_name):
    if not db_name:
        db_name = "main"
    if current_app.config["DEBUG"]:
        db_name = f"{db_name}_test"

    return Deta(os.environ["DETA_KEY"]).Base(db_name)


def database(inp=None, delete=False, db=None, db_name=None):
    if not inp:
        res = base(db_name).fetch()
        items = res.items

        while res.last:
            res = base(db_name).fetch(last=res.last)
            items += res.items

        return items

    if delete:
        if type(inp) is str:
            return base(db_name).delete(inp)

        elif type(inp) is dict:
            return base(db_name).delete(inp["key"])

        elif type(inp) is list:
            resp = []
            for i in inp:
                resp.append(database(i, True, db_name=db_name))
            return resp

    if type(inp) is str:
        if not db:
            db = database(db_name=db_name)
        for x in db:
            if x["key"] == inp:
                return x
        return None

    if type(inp) is dict:
        return base(db_name).put(inp)

    if type(inp) is list:
        resp_ = []
        while len(inp) > 0:
            resp = base(db_name).put_many(inp[:25])
            resp_.append(resp)
            inp = inp[25:]

        return resp_


def query(inp, many=False, db=None, db_name=None):
    output = []
    if not db:
        db = database(db_name=db_name)

    for x in db:
        if "type" not in x:
            database(x["key"], True, db_name=db_name)
            continue

        add = True
        for key in inp:
            if key not in x or x[key] != inp[key]:
                add = False
                break

        if add:
            if not many:
                return x

            output.append(x)

    return output if many else None
