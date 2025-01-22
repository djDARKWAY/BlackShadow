import os

def getDomain():
    try:
        if os.environ['USERDOMAIN'] == os.environ['COMPUTERNAME']:
            return "No domain"
        return os.environ['USERDOMAIN']
    except KeyError:
        return "Domain not found"
