from flask import current_app
from deta import Deta
import os


def base():
    name = "live"
    if current_app.config["DEBUG"]:
        name = "test"
    return Deta(os.environ["DETA_KEY"]).Base(name)


def database(x=None, delete=False, db=None):
    if not x:
        res = base().fetch()
        items = res.items

        while res.last:
            res = base().fetch(last=res.last)
            items += res.items

        return items

    if delete:
        if type(x) == str:
            return base().delete(x)

        elif type(x) == dict:
            return base().delete(x["key"])

        elif type(x) == list:
            resp = []
            for i in x:
                resp.append(database(i, True))
            return resp

    if type(x) == str:
        if not db:
            db = database()
        for row in db:
            if row["key"] == x:
                return row
        return None

    if type(x) == dict:
        return base().put(x)

    if type(x) == list:
        resp_ = []
        while len(x) > 0:
            resp = base().put_many(x[:25])
            resp_.append(resp)
            x = x[25:]

        return resp_


def query(_query, many=False, db=None):
    output = []
    if not db:
        db = database()

    for row in db:
        if "type" not in row:
            database(row["key"], True)
            continue

        add = True
        for key in _query:
            if key not in row or row[key] != _query[key]:
                add = False
                break

        if add:
            if not many:
                return row

            output.append(row)

    return output if many else None
