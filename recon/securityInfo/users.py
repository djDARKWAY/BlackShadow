import subprocess

def getUsers():
    try:
        command = "powershell -Command \"Get-LocalUser | Format-List *\""
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)

        if not result.strip():
            return {"error": "No user account data returned from PowerShell."}

        userAccounts = []
        accountData = result.split("\n\n")

        # Mapeamento de chaves mais legíveis
        label_mapping = {
            "Accountexpires": "Account Expires",
            "Description": "Description",
            "Enabled": "Enabled",
            "Fullname": "Full Name",
            "Passwordchangeabledate": "Password Changeable Date",
            "Passwordexpires": "Password Expiry Date",
            "Usermaychangepassword": "User May Change Password",
            "Passwordrequired": "Password Required",
            "Passwordlastset": "Password Last Set",
            "Lastlogon": "Last Logon",
            "Sid": "SID",
            "Principalsource": "Principal Source",
            "Objectclass": "Object Class"
        }

        for account in accountData:
            userInfo = {}
            lines = account.splitlines()

            for line in lines:
                if ':' in line:
                    key, value = line.split(":", 1)
                    key = key.strip()
                    value = value.strip()

                    key = label_mapping.get(key, key)
                    userInfo[key] = value if value else "N/A"

            if 'Enabled' in userInfo and userInfo.get('Enabled') == 'True':
                userAccounts.append(userInfo)

        return userAccounts

    except subprocess.CalledProcessError as e:
        return {"error": f"Error calling PowerShell: {e.output}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {str(e)}"}

def getActiveUserAccounts():
    userAccounts = getUsers()

    if isinstance(userAccounts, list) and userAccounts:
        return userAccounts
    else:
        return {"error": userAccounts.get("error", "Unknown error")}
