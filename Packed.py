from datetime import datetime,date,time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import ssl, smtplib, requests, json, csv, time
import pandas as pd

pd.options.mode.chained_assignment = None
start_time = time.time()

def getdata_Cowin(pin):
    today = date.today()
    d1 = today.strftime("%d-%m-%Y")

    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            'content-type': 'application/json; charset=UTF-8'}

    params = {"pincode": pin, "date":d1}

    start_url = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin'
    response = requests.get(start_url, params = params, headers = headers, timeout = 20)
    data = response.json()
    print("Data Retrieved")
    return data

def getCentres(data,age):
    alert = []

    centres = data["centers"]

    for centre in centres:
        for session in centre["sessions"]:
            if session["available_capacity"]>0 and session["min_age_limit"] == 18: #session["vaccine"] == "COVISHIELD" OR 'COVAXIN'
                name = centre["name"]
                address = centre["address"]
                date = session["date"]
                v = session["vaccine"]
                dump = {"Name":name,"Address":address,"Date":date,"Vaccine":v,"Capacity":session["available_capacity"]}
                alert.append(dump)
    return alert

def getMessage(alert, receiver_email, receiver_name):
    text = ""
    for dumped in alert:
        pretty_dict_str = json.dumps(dumped, indent=4)
        text = text + pretty_dict_str + "\n"
    
    message = MIMEMultipart("alternative")
    message["Subject"] = "Your Friendly Vaccine Availability Reminder"
    message["From"] = "notificationvaccine@gmail.com"
    message["To"] = receiver_email

    message_body = """\
    Hi {0}!
    The vaccine is now available at the following centres for the 18+ Age Group:\n""".format(receiver_name)+text
    
    part1 = MIMEText(message_body, "plain")
    message.attach(part1)
    return message.as_string()

def sendMail(alert,receiver_email,message):
    
    port = 465
    context = ssl.create_default_context()

    smtp_server = "smtp.gmail.com"
    sender_email = "my@gmail.com"  #Enter the username which you'll be using to send the mails.
    password = "" #Enter the password to authenticate the Login Request.
    
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
        print("Mail Sent")

def main():
    filepath = "Contacts.csv" #Get details from the Mailing List.
    df = pd.read_csv(filepath)
    today = date.today()
    
    for i in range(len(df.index)):
        LastSent = datetime.date(datetime.strptime(df.at[i,"LastSent"],'%Y-%m-%d'))
        count = df.at[i,"Mailcount"]
        datedifference = today-LastSent
        
        if (datedifference.days>=1) and (count < 5):
            receiver_name = df.at[i,"Name"]
            receiver_email = df.at[i,"Email"]
            pin = df.at[i,'Pincode']
            age = df.at[i,"Agegroup"]

            data = getdata_Cowin(pin) #Request Data from https://www.cowin.gov.in/home for the PinCode 
            alert = getCentres(data, age) #Filter down the data as per Age requirements

            if alert != []:
                message = getMessage(alert, receiver_email, receiver_name) #Create Message String
                sendMail(alert, receiver_email, message) #Send Mail
                df.at[i,"LastSent"] = today
                df.at[i,"Mailcount"] = int(df.at[i,"Mailcount"])+1
    
    print("This program took", time.time() - start_time, "to run")

if __name__ == '__main__':
    main()

