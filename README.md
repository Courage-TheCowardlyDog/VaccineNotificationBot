# VaccineNotificationBot

While the government has announced the vaccination drive to be opened for everyone above the age of 18, the vaccine availability has been an area of concern - as the supply fails to meet the huge demands. As the registration has been made mandatory by the government, I came up with the idea of this bot to help the people in my circle register for the vaccine as soon as it is available.

**A bot that scrapes the government's portal https://www.cowin.gov.in/home, checks for the availability of the vaccine in centres near you and mails you as soon as the website data gets updated.** 
   
============================================================================  
Code & Related Files:  
* __Basic_Pincode.py__: *for private/individual implementation.* Uses the area PINCode to make a list of centres with vaccines & mails it to the mentioned mail-id.  
* __Packed.py__: *to be used with a mailing list (Contacts.csv)* Builds upon the private implementation to send the notification mail to everyone in the mailing list.
* __Contacts.csv__: *Mailing List* Commma Separated Value file which contains: Name, Email, Pincode, AgeGroup, MailLastSent (date), MailCount.  
* __DataPacketRecieved.json__: Sample data packet received from the website.  
  
============================================================================  
Implementation:
* Created mailing list using google forms (https://forms.gle/u7xxzDsmj2sxgapq7). Automated the export to a CSV to be accessed by the code.  
* Made a Batch file to run the Python Code, linked the Batch file to a .vbs script to enable it being run in the background.  
* Used the Windows Task Scheduler to trigger the .vbs script every 10 minutes.  
* Checked the log for any error being printed.
* The code has also been hosted on pythonanywhere.com, which runs once everyday at 08:00 IST - incase the main server shuts down for some reason.
  

