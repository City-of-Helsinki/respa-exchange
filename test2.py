import datetime
import logging
from configparser import ConfigParser
from random import randint
from uuid import uuid4

from respa_exchange.ews.calendar import CreateCalendarItemRequest, DeleteCalendarItemRequest, GetCalendarItemsRequest
from respa_exchange.ews.session import ExchangeSession

logging.basicConfig(level=logging.DEBUG)

cfg = ConfigParser(default_section="respa-exchange")
cfg.read("respa-exchange.cfg")

sess = ExchangeSession(
    url=cfg.get("respa-exchange", "url"),
    username=cfg.get("respa-exchange", "username"),
    password=cfg.get("respa-exchange", "password"),
)

test_principal = cfg.get("respa-exchange", "test-principal")


def test_get():
    cir = GetCalendarItemsRequest(
        principal=test_principal,
        start_date=datetime.datetime(2016, 1, 1),
        end_date=datetime.datetime(2016, 5, 1),
    )
    for item in cir.send(sess):
        print(item)


def test_create():
    start = datetime.datetime.now() + datetime.timedelta(seconds=randint(86400, 410511))
    end = start + datetime.timedelta(seconds=randint(2, 14) * 15 * 60)

    ccir = CreateCalendarItemRequest(
        principal=test_principal,
        start=start,
        end=end,
        subject="Test %s" % uuid4()
    )
    item_id = ccir.send(sess)
    dcir = DeleteCalendarItemRequest(
        principal=test_principal,
        item_id=item_id
    )
    assert dcir.send(sess)


if __name__ == "__main__":
    test_get()
    test_create()
