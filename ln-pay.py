#!/usr/bin/env python3

import rpc_pb2 as ln
import rpc_pb2_grpc as lnrpc
import grpc
import sys
import os
from time import sleep

if not sys.stdout.isatty():
    from gi.repository import Gtk
    import notify2

#Autopay setting
MAX_AUTOPAY_AMT = 0.05 #Maximum amount of mBTC that will be automatically paid
MIN_AUTOPAY_BALANCE = 2 #Minimum channel amount in mBTC for autopaying LN transaction
whitelist = [] #Whitelist of public keys that will be automatically paid by ln-pay

ICON_SUCCESS = os.path.expanduser('~/.local/share/applications/lightning-128x128.png')
ICON_FAILURE = os.path.expanduser('~/.local/share/applications/Gnome-dialog-error.svg')


#RPC settings
RPC_ADDR = 'localhost:10009'
CERT = open(os.path.expanduser('~/.lnd/tls.cert')).read()
CREDS = grpc.ssl_channel_credentials(CERT)
channel = grpc.secure_channel(RPC_ADDR, CREDS)
stub = lnrpc.LightningStub(channel)

#print(sys.argv)


def pay_cb(n, action):
    assert action == "pay"
    PAYMENT = stub.SendPaymentSync(ln.SendRequest(payment_request=LN_INVOICE))
    if PAYMENT.payment_error:
        notify2.Notification("Lightning Pay", "Transaction to \n{}\nfailed with \n{}".format(DEST,PAYMENT.payment_error),icon=ICON_FAILURE).show()
    else:
        notify2.Notification("Lightning Pay","Transaction to \n{}\nis successful".format(DEST),icon=ICON_SUCCESS).show()
    n.close()

def cancel_cb(n, action):
    assert action == "cancel"
    n.close()

def closed_cb(n):
    Gtk.main_quit()

try:
    if sys.argv[1][:10] == 'lightning:':
        LN_INVOICE = sys.argv[1][10:]
    else:
        LN_INVOICE = sys.argv[1]
except IndexError:
    LN_INVOICE = input('Paste your Lightning Network invoice here: ')
    if LN_INVOICE == '':
        _ = input("No Lightning Network invoice entered, press enter to exit")
        raise

try:
    DECODED_PAYREQ = stub.DecodePayReq(ln.PayReqString(pay_req=LN_INVOICE))
except grpc._channel._Rendezvous:
    if sys.stdout.isatty():
        _ = input("Invalid Lightning Network invoice, press enter to exit")
        raise ValueError
    else:
        notify2.init("LN-Pay")
        notify2.Notification("Invalid Lightning Network invoice").show()
        sys.exit(1)


MBTC = DECODED_PAYREQ.num_satoshis/100000
DEST = DECODED_PAYREQ.destination
DESC = DECODED_PAYREQ.description
BALANCE = stub.ChannelBalance(ln.ChannelBalanceRequest()).balance * 100000


if sys.stdout.isatty():
    print("{} mBTC in Lightning Network".format(BALANCE))
    if DEST in whitelist and MBTC <= MAX_AUTOPAY_AMT and BALANCE >= MIN_AUTOPAY_BALANCE :
        print("Paying to {} for {} with {}".format(DEST,DESC,MBTC))
        PAYMENT = stub.SendPaymentSync(ln.SendRequest(payment_request=LN_INVOICE))
        if PAYMENT.payment_error:
            _ = input("Transaction to {} failed with {}, press any key to exit".format(DEST,PAYMENT.payment_error))
        else:
            print("Transaction to {} is successful".format(DEST))
            sleep(1)
    else:
        CMD = input("Pay to {} for {} with {} mBTC y/n: ".format(DEST,DESC,MBTC))
        if CMD == 'y':
            PAYMENT = stub.SendPaymentSync(ln.SendRequest(payment_request=LN_INVOICE))
            if PAYMENT.payment_error:
                _ = input("Transaction to {} failed with {}, press any key to exit".format(DEST,PAYMENT.payment_error))
            else:
                print("Transaction to {} is successful".format(DEST))
                sleep(1)

        else:
            _ = input("Transaction to {} is cancelled, press any key to exit".format(DEST))

else:
    if not notify2.init("Multi Action Test", mainloop='glib'):
        sys.exit(1)
    SERVER_CAPS = notify2.get_server_caps()
    if 'actions' in SERVER_CAPS:
        if DEST in whitelist and MBTC <= MAX_AUTOPAY_AMT and BALANCE >= MIN_AUTOPAY_BALANCE :
            notify2.Notification("Lightning Pay", "Autopaying to \n{}\n for {}\nwith {} mBTC".format(DEST,DESC,MBTC),icon=ICON_SUCCESS).show()
            PAYMENT = stub.SendPaymentSync(ln.SendRequest(payment_request=LN_INVOICE))
            if PAYMENT.payment_error:
                notify2.Notification("Lightning Pay", "Transaction to \n{}\nfailed with \n{}".format(DEST,PAYMENT.payment_error),icon=ICON_FAILURE).show()
                sys.exit(1)
            else:
                notify2.Notification("Lightning Pay","Transaction to \n{}\nis successful".format(DEST),icon=ICON_SUCCESS).show()
                sys.exit(0)

    else:
        notify2.Notification("Lightning Pay","Your notification server doesn't support actions\nUse CLI interface only").show()
        sys.exit(1)


    n = notify2.Notification("Lightning Pay", "Pay to \n{}\nfor {}\nwith {} mBTC".format(DEST,DESC,MBTC),icon=ICON_SUCCESS)
    n.add_action("pay", "Pay", pay_cb)
    n.add_action("cancel", "Cancel", cancel_cb)
    n.connect('closed', closed_cb)
    n.show()
    Gtk.main()
