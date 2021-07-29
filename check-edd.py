import re
import os
from requests import Session
from bs4 import BeautifulSoup as bs
from dotenv import load_dotenv

import sys
from email.mime.text import MIMEText
from subprocess import Popen, PIPE

load_dotenv(verbose=True)
myEmail = os.getenv("EMAIL")
myCredential = os.getenv("CREDENTIAL")
referenceNumber = os.getenv("REFERENCE_NUMBER")
userAgent = os.getenv("USER_AGENT")
urlLoginForm = os.getenv("LOGIN_FORM_URL")
urlManage = os.getenv("MANAGE_URL") + referenceNumber
sendMail = os.getenv("EMAIL_RESULT")

headers = {"User-Agent": userAgent}

with Session() as s:
    s.headers.update(headers)
    site = s.get(urlLoginForm)
    loginform_content = bs(site.content, "html.parser")

    _csrf = loginform_content.find("input", {"name": "_csrf"})["value"]
    _process = loginform_content.find("input", {"name": "_process"})["value"]
    transaction_id = loginform_content.find("input", {"name": "transaction_id"})["value"]
    cancel = loginform_content.find("input", {"name": "cancel"})["value"]
    identity = loginform_content.find("input", {"name": "transaction_id"})["value"]

    login_data = {
        "_csrf": _csrf, 
        "_phase": "authenticate", 
        "_process": _process, 
        "transaction_id": transaction_id, 
        "cancel": cancel, 
        "identity": myEmail, 
        "credential": myCredential
    }

    loginResponse = s.post(urlLoginForm, login_data, headers={"User-Agent": userAgent, "Referer": urlLoginForm})

    homepage = s.get(urlManage)
    homepage_content = bs(homepage.content, "html.parser")

    pattern = re.compile(r'\"EstimateDelivery\"\s*:\s*{\s*\"copyOverride\"\s*:\s*\"([^\"]+)\"\s*}')
    edd = homepage_content.find("script", text=pattern)

    if edd:
        match = pattern.search(edd.string)
        if match:
            if sendMail == "False":
                print(match.group(1))
            else:
                msg = MIMEText(match.group(1))
                msg["From"] = myEmail
                msg["To"] = myEmail
                msg["Subject"] = match.group(1)
                p = Popen(["/usr/sbin/sendmail", "-t", "-oi"], stdin=PIPE)
                if sys.version_info >= (3,0):
                    p.communicate(msg.as_bytes())
                else:
                    p.communicate(msg.as_string())
