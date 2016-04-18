from datetime import datetime, timedelta

import pytest
from django.utils.crypto import get_random_string

from resources.models.reservation import Reservation
from respa_exchange.ews.xml import M, NAMESPACES, T
from respa_exchange.models import ExchangeReservation, ExchangeResource
from respa_exchange.tests.session import SoapSeller


class CRUDItemHandlers(object):
    def __init__(self, item_id, change_key, update_change_key):
        self.item_id = item_id
        self.change_key = change_key
        self.update_change_key = update_change_key

    def _generate_items_fragment(self, change_key):
        return M.Items(
            T.CalendarItem(
                T.ItemId(
                    Id=self.item_id,
                    ChangeKey=change_key
                )
            )
        )

    def handle_create(self, request):
        # Handle CreateItem responses; always return success
        if not request.xpath("//m:CreateItem", namespaces=NAMESPACES):
            return  # pragma: no cover

        return M.CreateItemResponse(
            M.ResponseMessages(
                M.CreateItemResponseMessage(
                    {"ResponseClass": "Success"},
                    M.ResponseCode("NoError"),
                    self._generate_items_fragment(change_key=self.change_key)
                )
            )
        )

    def handle_delete(self, request):
        # Handle DeleteItem responses; always return success
        if not request.xpath("//m:DeleteItem", namespaces=NAMESPACES):
            return  # pragma: no cover
        return M.DeleteItemResponse(
            M.ResponseMessages(
                M.DeleteItemResponseMessage(
                    {"ResponseClass": "Success"},
                    M.ResponseCode("NoError"),
                )
            )
        )

    def handle_update(self, request):
        # Handle UpdateItem responses; return success
        if not request.xpath("//m:UpdateItem", namespaces=NAMESPACES):
            return  # pragma: no cover
        return M.UpdateItemResponse(
            M.ResponseMessages(
                M.UpdateItemResponseMessage(
                    {"ResponseClass": "Success"},
                    M.ResponseCode("NoError"),
                    self._generate_items_fragment(change_key=self.update_change_key),
                    M.ConflictResults(M.Count("0"))
                )
            )
        )


@pytest.mark.django_db
@pytest.mark.parametrize("master_switch", (False, True))
@pytest.mark.parametrize("authed_res", (False, True))
@pytest.mark.parametrize("is_exchange_resource", (False, True))
@pytest.mark.parametrize("cancel_instead_of_delete", (False, True))
@pytest.mark.parametrize("update_too", (False, True))
def test_crud_reservation(
    settings, space_resource, exchange, admin_user,
    master_switch, authed_res, is_exchange_resource, cancel_instead_of_delete, update_too
):
    settings.RESPA_EXCHANGE_ENABLED = master_switch
    delegate = CRUDItemHandlers(
        item_id=get_random_string(),
        change_key=get_random_string(),
        update_change_key=get_random_string(),
    )
    SoapSeller.wire(settings, delegate)
    if is_exchange_resource:
        ex_resource = ExchangeResource.objects.create(
            resource=space_resource,
            principal_email="test@example.com",
            exchange=exchange
        )
    # Signals are called at creation time...
    res = Reservation.objects.create(
        resource=space_resource,
        begin=datetime.now(),
        end=datetime.now() + timedelta(minutes=30),
        user=(admin_user if authed_res else None),
    )
    if master_switch and is_exchange_resource:
        # so now we should have a reservation in Exchange
        ex_resv = ExchangeReservation.objects.get(
            reservation=res
        )
        assert ex_resv.principal_email == ex_resource.principal_email
        assert ex_resv.item_id.id == delegate.item_id
        assert ex_resv.item_id.change_key == delegate.change_key
    else:
        assert not ExchangeReservation.objects.filter(reservation=res).exists()

    if update_too:
        res.end += timedelta(minutes=30)
        res.reserver_name = "John Doe"
        res.save()
        if master_switch and is_exchange_resource:
            # Our exchange reservation's change key should have changed
            ex_resv = ExchangeReservation.objects.get(reservation=res)
            assert ex_resv.item_id.change_key == delegate.update_change_key

    if cancel_instead_of_delete:  # But let's cancel it...
        res.set_state(Reservation.CANCELLED, user=None)
    else:  # But let's delete it...
        res.delete()

    # ... so our Exchange reservation gets destroyed.

    assert not ExchangeReservation.objects.filter(reservation=res).exists()
