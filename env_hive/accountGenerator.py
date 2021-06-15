import sys
import os
from twocaptcha import TwoCaptcha
import requests, re
from ProxyManager import get_random_proxy
from logFile import logFile
import json

#function to get Captcha from SneakerPolitics
def getCaptcha():
    attempt = 4
    i=0
    #attempting 5 times to do the get
    while(i<attempt):
        ++i
        sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
        api_key = os.getenv('APIKEY_2CAPTCHA', '83d169eb3b08c1d677d0a3fd617310a3')
        #use 2captcha solver
        solver = TwoCaptcha(api_key)
        try:
            #get the captcha
            result = solver.recaptcha(
                sitekey='6LeoeSkTAAAAAA9rkZs5oS82l69OEYjKRZAiKdaF',
                url='https://sneakerpolitics.com/challenge')
        except Exception as e:
            print("Exception occured, retrying.")
        else:
            #checking if key code exists
            if 'code' in result:
                return result['code']
            #No key code so retrying
            else:
                print("Didn't get the Captcha, retrying.")



def AddAccountToJson(firstName,lastName,email,password,company,address1,address2,country,province,city,zipNum,phone):
    accountJson= {
        'firstName' : firstName,
        'lastName' : lastName,
        'email' : email,
        'password' : password,
        'company' : company,
        'address1' : address1,
        'address2' : address2,
        'country': country,
        'province' : province,
        'city' : city,
        'zip' : zipNum,
        'phone' : phone

    }
    dir_path = os.path.dirname(os.path.realpath(__file__))
    pathToJson = dir_path + '/configAccounts.json'
    if(os.path.exists(pathToJson)):
        with open(pathToJson) as json_file:
            data = json.load(json_file)
            accountArray = data["accountsCreated"]
            accountArray.append(accountJson)
            json_file.close()
            accounts_dict = {
                "accountsCreated" : accountArray
            }
            with open(pathToJson, 'w') as json_file:
                json.dump(accounts_dict, json_file)
                json_file.close()
    else:
        accounts_dict = {
            "accountsCreated" : [accountJson]
        }
        with open(pathToJson, 'w') as json_file:
            json.dump(accounts_dict, json_file)
            json_file.close()



def generateAccount(firstName,lastName,email,password,company,address1,address2,country,province,city,zipNum,phone):
    session = requests.session()
    randomProxy = get_random_proxy()
    session.proxies.update(randomProxy)
    print("Creating the account...")
    #data to create account
    data= "form_type=create_customer&utf8=%E2%9C%93&customer%5Bfirst_name%5D=" + firstName + "&customer%5Blast_name%5D=" + lastName + "&customer%5Bemail%5D=" + email + "&customer%5Bpassword%5D=" + password
    #header to create account
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'fr-FR,fr;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': '221',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
         'origin' : 'https://sneakerpolitics.com',
        'Referer': "https://sneakerpolitics.com/account/register",
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Mobile Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    #update the header
    session.headers= headers
    try:
        response = session.post("https://sneakerpolitics.com/account",data)
        regex_auth = r'(?:name="authenticity_token")\s+value="(.*?)"'
        matches = re.findall(regex_auth, response.text, re.MULTILINE)
        auth_token=""
        if matches:
            auth_token = matches[0]
            headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'fr-FR,fr;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '221',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
             'origin' : 'https://sneakerpolitics.com',
            'referer': "https://sneakerpolitics.com/challenge",
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Mobile Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
            }

            session.headers= headers
            print("Getting the captcha...")

            data= "authenticity_token=" + auth_token +  "&g-recaptcha-response=" + getCaptcha()
            response = session.post("https://sneakerpolitics.com/account",data)

            if "This email address is already associated with an account"  in response.text: 
                emailAlreadyExisting = "Account already created !"
                print(emailAlreadyExisting)
                logFile(emailAlreadyExisting)
                return -1
            else:
                print("Account created !\nAdding the address...")

                #check that all informations is here (not make sense not to put country)
                if not(firstName):
                    print("Put a first name !")
                    return -1
                if not(lastName):
                    print("Put a last name !")
                    return -1
                if not(address1):
                    print("Put an address !")
                    return -1
                if not(country):
                    print("Put name of country !")
                    return -1
                if not(province):
                    print("Put name of province !")
                    return -1
                if not(city):
                    print("Put name of city !")
                    return -1

                headers = {
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'fr-FR,fr;q=0.9',
                    'referer': "https://sneakerpolitics.com/account",
                    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Mobile Safari/537.36'
                }

                session.headers= headers

                #replacing space with + for addresses
                address1Replace = address1.replace(" ", "+")
                address2Replace = address2.replace(" ", "+")
                countryReplace = country.replace(" ", "+")
                #all data to add address
                data= "form_type=customer_address&utf8=%E2%9C%93&address%5Bfirst_name%5D=" + firstName + "&address%5Blast_name%5D=" + lastName +"&address%5Bcompany%5D=" + company + "&address%5Baddress1%5D=" + address1Replace+ "&address%5Baddress2%5D="  + address2Replace + "&address%5Bcountry%5D=" +  countryReplace+ "&address%5Bprovince%5D=" + province + "&address%5Bcity%5D=" + city+ "&address%5Bzip%5D=" + zipNum + "&address%5Bphone%5D=" + phone + "&address%5Bdefault%5D=1"
                response = session.post("https://sneakerpolitics.com/account/addresses",data)
                if(response.status_code!=200):
                    print("Error, check your address information !")
                else:
                    #everything is good we can add it to json
                    print("Adress added to account !")
                    AddAccountToJson(firstName,lastName,email,password,company,address1,address2,country,province,city,zipNum,phone)
        else:
            noTokenError = "No authenticity token found in webpage !"
            print(noTokenError)
            logFile(noTokenError)
            return 0
    #catch all errors
    except requests.exceptions.Timeout:
        timeOutError = "Time out issue !"
        print(timeOutError)
        logFile(timeOutError)
    except requests.exceptions.TooManyRedirects as e:
        urlBad = "URL is bad, try a different one !\n" + str(e)
        print(urlBad)
        logFile(urlBad)
        return -1
    except requests.exceptions.RequestException as e:
        requestException = "Big error you should check proxy !\n" + str(e)
        print(requestException)
        logFile(requestException)
        return -1
    except:
        unexpectedError = "Unexpected error: " + sys.exc_info()[0]
        logFile(unexpectedError)
        return -1


if __name__ == "__main__":
    try:
        print("###################################\nWelcome to SneakerPolitics account generator\nCompany, second address and phone are not required\n###################################")
        firstName = input("Enter first name : ")
        lastName = input("Enter last name : ")
        email = input("Enter email : ")
        password = input("Enter password : ")
        company = input("Enter company : ")
        address = input("Enter address : ")
        address2 = input("Enter second address : ")
        country = input("Enter country : ")
        province = input("Enter province : ")
        city = input("Enter city : ")
        zipNum = input("Enter zip : ")
        phone = input("Enter phone : ")
        generateAccount(firstName,lastName,email,password,company,address,address2,country,province,city,zipNum,phone)
        input("Press any key to quit")
    except:
        print("Unexpected error:", sys.exc_info()[0])
