import requests
import json
import smtplib
import logging

URL = 'https://v2.jokeapi.dev/joke/Programming' #website to extract programming jokes from

#open the json file that contains the sender email address infomations and read it
with open('details.json', 'r') as info:
    data = json.load(info)
    info.close()

details = data["details"]
EMAIL = details['email'] #sender email address
PASSWORD = details['password'] #sender email address password
RECIPIENT = EMAIL #recepient email address
LOGFILE = 'text.log' #log file were events will be logged into


logging.basicConfig(filemode='a', filename=LOGFILE, level=logging.INFO, format='%(levelname)s - %(message)s - %(asctime)s')


#function to extract jokes from url
def jokes ():
    response = requests.get(URL) #get jokes from url
    result = response.json() #conver to json
    if result['error']:
        logging.error('Something wrong with the request API.')
    #if jokes returned by url is two part, extract the two jokes
    if result['type'] == 'twopart': 
        setup = result['setup']
        delivery = result['delivery']
        return(f'Setup: {setup} \nDelivery: {delivery}')
    #if jokes is just one joke, extract the joke
    else:
        joke = result['joke']
        return(f'Joke: {joke}')



#function to send jokes to email address
def send (joke):
    try:
        s = smtplib.SMTP('smtp.aol.com', 587) #create an smtp connection with email provider
        s.starttls() #create secure connection
    except smtplib.SMTPConnectError:
        logging.error('Connection error...could not connect to mail server.')
        exit()
    try:
        s.login(EMAIL, PASSWORD) #login to email 
    except smtplib.SMTPAuthenticationError:
        logging.error('Authentication error.')
        exit()
    try:
        s.sendmail(EMAIL, RECIPIENT, f'\n{joke}')#send joke from sender email to recepient email address
    except smtplib.SMTPException:
        logging.error('Unable to send email.')
        exit()
    s.quit()



joke = jokes() #get the jokes
logging.info('Joke retrieved successfuly...')
if joke is not None: 
    send(joke) #send joke 
    logging.info('Email sent successfuly...')