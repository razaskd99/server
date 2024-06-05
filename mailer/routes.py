from fastapi import FastAPI, APIRouter, BackgroundTasks
from mailer.config import MailBody, MailBodyFrom
from mailer.mailer import send_mail

router = APIRouter()


@router.post("/send-email" , tags=["Mailer"], summary="Send an email")
def schedule_mail(req: MailBody, tasks: BackgroundTasks):
    try:
        data = req.dict()
        tasks.add_task(send_mail, data)
        print('OK ju')
    except KeyError as e:
        print(str(e))    
    return {"status": 200, "message": "email has been scheduled"}


@router.post("/send-welcome-email", tags=["Mailer"], summary="Send welcome email on create account")
def send_welcome_email(req: MailBodyFrom, tasks: BackgroundTasks):
    try:
        data = req.dict()
        tasks.add_task(send_mail, data)
    except KeyError as e:
        print(str(e))    
    return {"status": 200, "message": "Email has been sent successfully."}



