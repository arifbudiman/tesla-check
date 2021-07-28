import re
import os
from requests import Session
from bs4 import BeautifulSoup as bs
from dotenv import load_dotenv

load_dotenv(verbose=True)
myEmail = os.getenv("EMAIL")
myCredential = os.getenv("CREDENTIAL")

userAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"

urlLoginForm = "https://auth.tesla.com/oauth2/v1/authorize?redirect_uri=https://www.tesla.com/teslaaccount/owner-xp/auth/callback&response_type=code&client_id=ownership&scope=openid%20email&audience=https%3A%2F%2Fownership.tesla.com%2F"

urlManage = "https://www.tesla.com/teslaaccount/profile?rn=RN115201757"

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
    
    pattern = re.compile(r'\"EstimateDelivery\":{([^}]+)}')
    
    edd = homepage_content.find("script", text=pattern)

    if edd:
        match = pattern.search(edd.string)
        if match:
            print(match.group(1))
