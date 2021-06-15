from datetime import datetime

def logFile(text):
        now = datetime.now()
# dd/mm/YY H:M:S
        file_name  = now.strftime("%d_%m_%Y-%H-%M-%S") + ".txt"
        f = open(file_name, "a")
        f.write(text)
        f.close()
