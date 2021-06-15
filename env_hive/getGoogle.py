import requests
from ProxyManager import get_random_proxy
from logFile import logFile
import sys

def getGoogle(): 
    i = 0
    attempt = 4
    #attempting 5 times to do a get
    while(i< attempt):
        ++i
        random_proxy = get_random_proxy()
        try:
            response =requests.get("http://google.com", proxies=random_proxy)
            status = response.status_code
            if(status!=200):
                logFile("Bad response from server")
            else:
                print("All good !")
                break
        except requests.exceptions.Timeout as e:
            timeOutError = "Time out issue !"
            print(timeOutError)
            logFile(timeOutError)
        except requests.exceptions.TooManyRedirects as e:
            urlBad = "URL is bad, try a different one !\n" + str(e)
            print(urlBad)
            logFile(urlBad)
            return -1
        except requests.exceptions.RequestException as e:
            requestException = "Proxy error !\n" + str(e)
            print(requestException)
            logFile(requestException)
        except:
            unexpectedError = "Unexpected error: " + sys.exc_info()[0]
            print(unexpectedError)
            logFile(unexpectedError)
            return -1
    if(i==attempt):
        print("All attempts were executed but it's unsuccessfull")

getGoogle()
