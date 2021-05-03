import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


username = "Shashi Kant"
movie_name = "Mission Impossible"
hall_name = "starplex"
show_time = "03:15:00"
price = 110

receiver_address = "XXXXXX@gmail.com"


def mail(username,movie_name,hall_name,show_time,price,receiver_address):
    sender_address = "XXXXXX@gmail.com"
    sender_app_pass = "XXXXXXXX"
    
    body ="""Dear {},
                Thank You for booking Movie 🎫Ticket from MoviesVoom.com
                Your Ticket Details are as follow -
                Movie Name = {} 🎬
                Hall Name = {}
                Show Time = {}
                Price = {}
                
    Thank You
    MoviesVoom!!!
    """.format(username,movie_name,hall_name,show_time,price)

    msg = MIMEMultipart()
    msg['From'] = sender_address
    msg['To'] = receiver_address
    msg['Subject'] = "Ticket confirmation by MoviesVoom"
    msg.attach(MIMEText(body, 'plain'))

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(sender_address, sender_app_pass)
    body = msg.as_string()
    s.sendmail(sender_address, receiver_address, body)
    s.quit()
    return("Mail Sent!!!")

mail(username,movie_name,hall_name,show_time,price,receiver_address)

