from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import date
import ssl,smtplib,requests,json

today = date.today()
d1 = today.strftime("%d-%m-%Y")

headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
           'content-type': 'application/json; charset=UTF-8'}

pin = "110001" #enter your area pin code here
params = {"pincode": pin, "date":d1}

start_url = 'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin'
response = requests.get(start_url, params = params, headers = headers, timeout = 20)
page = BeautifulSoup(response.content, 'html.parser')
data = response.json()

v = "COVAXIN"
alert = []

centres = data["centers"]

for centre in centres:
    for session in centre["sessions"]:
        if session["available_capacity"]>0 and session["min_age_limit"] == 18: #session["vaccine"] == v and
            name = centre["name"]
            address = centre["address"]
            date = session["date"]
            dump = {"Name":name,"Address":address,"Date":date,"Vaccine":v,"Capacity":session["available_capacity"]}
            alert.append(dump)

if alert != []:
    text = ""
    for dumped in alert:
        pretty_dict_str = json.dumps(dumped, indent=4)
        text = text + pretty_dict_str + "\n"

    port = 465
    context = ssl.create_default_context()

    smtp_server = "smtp.gmail.com"
    sender_email = "me@gmail.com"  # Enter your address
    receiver_email = "you@gmail.com"  # Enter receiver address
    password = "" #enter your password here
    
    message = MIMEMultipart("alternative")
    message["Subject"] = "Your Friendly Vaccine Availability Reminder"
    message["From"] = sender_email
    message["To"] = receiver_email

    message_body = """\
    Hi !
    The vaccine is now available at the following centres for the 18+ Age Group:\n"""+text
    
    part1 = MIMEText(message_body, "plain")
    message.attach(part1)

    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message.as_string())
    #print(message.as_string())
else:
    print("Vaccine not yet available in your area for the 18+ age group")



