import os
from dotenv import load_dotenv
from typing import List
from pydantic import BaseModel

load_dotenv()

HOST = os.environ.get("MAIL_HOST", 'smtp.gmail.com')
USERNAME = os.environ.get("MAIL_USERNAME", 'razaskdbalti99@gmail.com')
PASSWORD = os.environ.get("MAIL_PASSWORD", 'xfcb hozo pgbg mxun')
PORT = os.environ.get("MAIL_PORT", 587)


class MailBody(BaseModel):
    to: List[str]
    subject: str
    body: str

class MailBodyFrom(MailBody):
    from_email: str
    