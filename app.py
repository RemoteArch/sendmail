from flask import Flask , jsonify , request , make_response
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Paramètres du compte Gmail

app = Flask(__name__)

def envoyer_email(email_sender , password, email_receiver,message , smtp_server = 'smtp.gmail.com' , smtp_port = 587):

    # Création de l'objet MIMEMultipart
    msg = MIMEMultipart()
    msg['From'] = email_sender
    msg['To'] = email_receiver
    msg['Subject'] = "test"

    # Ajout du corps du message
    msg.attach(MIMEText(message, 'plain'))

    # Connexion au serveur SMTP de Gmail
    smtp = smtplib.SMTP(smtp_server, smtp_port)
    smtp.starttls()
    smtp.login(email_sender, password)

    # Envoi de l'e-mail
    smtp.send_message(msg)

    # Fermeture de la connexion SMTP
    smtp.quit()


@app.route('/' , methods=['GET'])
def home():
    data = open(os.path.join(os.path.dirname(__file__),"v2",'index.html'), "rb").read()
    res = make_response(data)
    return res

@app.route("/<file>" , methods=["GET"])
def file(file):
    print(file)
    data = open(os.path.join(os.path.dirname(__file__),"v2",file),"rb").read()
    print(len(data))
    res = make_response(data)
    match file.split('.')[-1]:
        case 'js':
            res.headers['Content-Type'] = "application/javascript"
        case 'css':
            res.headers['Content-Type'] = "text/css"
        case 'ico':
            res.headers['Content-Type'] = "images/png"
    return res

@app.route('/sendmail' , methods=['POST'])
def send_mail():
    try:
        dat = request.get_json()
        email = dat["email"]
        message = dat["message"]
        email_sender = dat["semail"]
        password = dat["password"]
        envoyer_email(email_sender , password,email , message)
        return jsonify({"message":"email envoyer avec succes"})
    except smtplib.SMTPAuthenticationError as e:
        return jsonify({'error':e.smtp_code , "message":e.smtp_error.decode()})
    except Exception as e:
        return jsonify({'error':"Erreur Inconnue" , "message":str(e)})

if __name__ == "__main__":
    app.run()
