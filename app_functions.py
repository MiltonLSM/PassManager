

import random
import smtplib 
import ssl
from email.message import EmailMessage

def send_email(receiver_email, link):
    
    sender_email = 'projectsmiltonix@gmail.com'
    email_password = 'ywzcjapviguwjfhs'
    body = f"""Please click on the following link to reset your password: 
    
    {link}
    
Best wishes, 
MySafeSpot team"""

    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = "My safe spot - Reset password"
    msg['From'] = sender_email
    msg['To'] = receiver_email

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(sender_email, email_password)
        smtp.send_message(msg)


def create_pass():

    characters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 
                't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '~', '!', 
                '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '-', '+', '=', '?', 'A', 'B', 'C', 'D', 'E', 
                'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 
                'Y', 'Z']

    lowerc = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    upperc = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '-', '+', '=', '?']


    password_length = 15
    new_password = ""

    char_types = [lowerc, upperc, numbers, symbols]

    for t in char_types:
        random_index = random.randint(0, len(t) - 1)
        random_char = t[random_index]
        new_password += random_char

    count = len(new_password)
    
    while count < password_length:
        random_index = random.randint(0, len(characters) - 1)
        random_char = characters[random_index]
        new_password += random_char
        count += 1

    new_password = ''.join(random.sample(new_password, len(new_password)))
    return new_password


def create_token():

    characters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 
                't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 
                'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 
                'V', 'W', 'X', 'Y', 'Z']
    
    token_length = 24
    token = ""

    count = 0
    
    while count < token_length:
        random_index = random.randint(0, len(characters) - 1)
        random_char = characters[random_index]
        token += random_char
        count += 1

    return token


