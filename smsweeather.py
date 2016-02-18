import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests

SMS_GATEWAYS = {
    "AT&T"      : "txt.att.net",
    "CRICKET"   : "mms.cricketwireless.net",
    "SPRINT"    : "pm.sprint.com",
    "TMOBILE"   : "tmomail.net",
    "VERIZON"   : "vtext.com",
    "VIRGIN"    : "vmobl.com"
}

open_weather_map_api_key = "f32ded4b7f80f31e070fff1d60439e64"

def sms_weather(zip, phone_number, carrier):
    url = "http://api.openweathermap.org/data/2.5/weather?zip=" + str(zip) + "us&APPID=" + open_weather_map_api_key
    r = requests.get(url)
    content = r.json()
    content["weather"] = content["weather"][0]
    
    description, temp = content["weather"]["description"], content["main"]["temp"]*9.0/5.0 - 459.67
    message = "We're expecting "
    message += description + ".  Today's temperature will be " + str(temp) + ".  "
    if temp > 60:
      message += "You won't need a jacket today."
    else:
      message += "You will need a jacket today."
    
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()

    server.login( SERVER_LOGIN, SERVER_PASSWORD )
    vtext = phone_number + "@" + SMS_GATEWAYS[carrier.upper()]
    msg = MIMEText(message)

    # Send text message through SMS gateway of destination number
    server.sendmail( SERVER_LOGIN, vtext, msg.as_string() )
    server.quit()

