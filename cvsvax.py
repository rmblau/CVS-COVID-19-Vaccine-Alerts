#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  3 15:21:04 2021

@author: cabrown802
"""

import urllib.request
import threading
import smtplib
import ssl
from os import environ

def gather_info():
    state= input("Type the state you are from, with the first letter capitalized, and press enter: ")
    sender_email = environ["USER_EMAIL"]
    sender_password = environ["USER_PASSWORD"]
    receiver = input("Type the email that you would like to send emails TO, and press enter: ")
    # How often to refresh the page, in seconds
    UPDATE = 60.0
    # Port for SSLport 
    port= 465
    # Message in the email.
    message = "Book an appointment at CVS! https://www.cvs.com/immunizations/covid-19-vaccine"
    # Create a secure SSL context
    context = ssl.create_default_context()
    
    return state,sender_email,sender_password,receiver,UPDATE,port,message,context

state, sender_email, sender_password, receiver, UPDATE, port, message, context = gather_info()

# This function repeatedly reads the CVS website, and if any appointments are
# available in your state, it emails you.
def sendit():
    smtp_server = environ['SMTP_SERVER']
    # Initializes threading (repition / refreshing of website)
    threading.Timer(UPDATE, sendit).start()
    
    # Reads website into var 'html'
    html = urllib.request.urlopen('https://www.cvs.com/immunizations/covid-19-vaccine').read()
    
    # If not all appointments are booked...
    lookforstring = f"At this time, all appointments in {state} are booked."
    if lookforstring.encode() not in html:
        
        # Login via STMP and send email
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver, message)
   
sendit()


    

        




