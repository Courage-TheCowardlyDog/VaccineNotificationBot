# VaccineNotificationBot

A bot that scrapes the government's portal https://www.cowin.gov.in/home, checks for the availability of the vaccine in centres near you and mails you as soon as the website data gets updated.    

============================================================================  
Code:  
* __Basic_Pincode.py__: *for private/individual implementation.* Uses the area Pincode to make a list of centres with vaccines & mails it to the mentioned mail-id.  
* __Packed.py__: *to be used with a mailing list (Contacts.csv)* Builds upon the private implementation to send the notification mail to everyone in the mailing list.
* __Contacts.csv__: *Mailing List* Commma Separated Value file which contains: Name, Email, Pincode, AgeGroup, MailLastSent (date), MailCount.  
* __DataPacketRecieved.json__: Sample data packet received from the website.  
  
============================================================================  
  
Created my mailing list using google forms, and saved the data in the form of a CSV that could be accessed by the program. I then scheduled the code to be run every hour, to prevent increasing constant load on the website and yet be updated incase of any changes in the availability. The code has also been hosted on pythonanywhere.com, which runs once everyday at 08:00 IST - incase the main server shuts down for some reason.
  
