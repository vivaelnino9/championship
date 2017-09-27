import logging
import requests
import os
import json
import paypalrestsdk
from django.core.urlresolvers import reverse

from .models import *

from paypalrestsdk import Sale
from paypalrestsdk.resource import Resource
logging.basicConfig(level=logging.INFO)

def get_payment_link(request,tournament):
    team = request.user.team
    payment = check_for_existing_payment(team,tournament)
    link = {}
    if not payment: return create_payment(request,team.name,tournament)
    if payment.paid: return {'link':'#','error':True}
    else: return {'link':payment.approval_url,'error':False}

def check_for_existing_payment(team,tournament):
    if team.get_payment(tournament).exists():
        payment = team.get_payment(tournament).first()
        return payment
    return False

def create_payment(request,team_name,tournament):
    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": request.build_absolute_uri(reverse('tournament_signup',kwargs={'tournament_id':tournament.id,'team_name':team_name,'action':'add'})),
            "cancel_url": request.build_absolute_uri(reverse('tournament_page',kwargs={'tournament_id':tournament.id}))},
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": tournament.full,
                    "sku": "item",
                    "price": tournament.cost,
                    "currency": "USD",
                    "quantity": 1}]},
            "amount": {
                "total": str(tournament.cost),
                "currency": "USD"},
            "description": tournament.full,
            "custom": request.user.email}]
    })
    if payment.create():
        ID = payment['id']
        approval_url = payment['links'][1]['href']
        Payment.objects.create(
            team=request.user.team,
            ID=ID,
            amount=tournament.cost,
            paid=False,
            approval_url=approval_url,
            tournament=tournament
        )
        return {'link':approval_url,'error':False}
    return {'link':'#','error':True}

def refund_payment(p):
    sale = Sale.find(p.sale_id)
    refund = sale.refund({
    "amount": {
        "total": p.amount,
        "currency": "USD"}
    })
    if refund.success():
        print("Refund[%s] Success" % (refund.id))
    else:
        print("Unable to Refund")
        print(refund.error)
