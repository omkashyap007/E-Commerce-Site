from django.core.mail import send_mail
import requests
from django.contrib import messages

def createEmailActivationLink(auth_token , user_id , *args , **kwargs) : 
    return "http://localhost:8000/account/authentication/verify-email/{}/{}".format(user_id , auth_token)

def createActivationEmailHtmlMessage(link) :
    ACTIVATION_HTML_MESSAGE = """
    <html>
    <body>
        <p style="color: black; font-family: cambria; font-size: 1.2rem">
        Hello User , You have created an accout in our Website , we request you to verify the email . For security purpose this has to be done . This mail is sent from Ecomsite Team to verify your account . Kindly click the button below to activate the account or click the link at the bottom to activate
        </p>

        <center>
        <a href="{0}">
            <button
            style="
                color: white;
                background-color: #00ced1;
                padding: 10px;
                border-radius: 5px;
                text-shadow: 2px 2px 2px black;
                box-shadow: 0px 0px 0px white;
                cursor : pointer; 
            "
            >
            Activate Account
            </button>
        </a>
        </center>
        <br>
        <br>
        <a href="{0}">{0}</a>
    </body>
    </html>
    """.format(link)
    return ACTIVATION_HTML_MESSAGE


def checkInternetConnection() :
    try : 
        url = "https://www.google.com/"
        status_code = requests.get(url ,
            timeout = 2).status_code
        if status_code == 200 : 
            return True
    except Exception as e :
        return False
    return False

def sendActivationEmail(email , auth_token , user_id , *args , **kwargs) : 
    is_connected = checkInternetConnection()
    if is_connected :
        activation_link = createEmailActivationLink(auth_token , user_id )
        html_message = createActivationEmailHtmlMessage(activation_link)
        try : 
            send_mail(
                subject = "Activation Link !",
                message = "Actiavtion Link Mail !" , 
                from_email = "" , 
                recipient_list = ["{}".format(email)] , 
                html_message = html_message 
            )
            return "Mail sent"
        except Exception as e : 
            return "Something Unexpected Occured !"
    else : 
        return "Internet connection Error"
    
def checkMailSent(mail_sent , request , *args , **kwargs):
    if mail_sent == "Mail sent" : 
        return messages.success(request , "Your email activation link has been sent successfully . Kindly check your email and verify it !")
    if mail_sent == "Internet connection Error" :
        return messages.error(request , "You don't have an actvie Internet connection in your device . Kindly check your connection !")
    if mail_sent == "Something Unexpected Occured !": 
        return messages.error(request , "Something unexpected Error has occured !")