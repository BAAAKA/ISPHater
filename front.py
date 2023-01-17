import socket
import time
import datetime
import plotly.express as px
from datetime import datetime, timedelta
import pandas as pd


def main():
    today = []
    start = datetime.now()
    stop = start + timedelta(hours = 24)
    print(f"Starting now {start} until tmrw {stop}")
    remainingSeconds = 1000

    while remainingSeconds>100:
        print(remainingSeconds)
        checks = 60
        failures = testMinute(checks)
        failurePercent = failures/checks
        now = datetime.now()
        remainingSeconds = (stop - now).total_seconds()
        now_edited = now.strftime("%H:%M")
        text = f"{now_edited} - Last minute we had {failures} failures, {failurePercent} failure rate"
        print(text)
        writeToFile(text)
        today.append((now, failurePercent))

    createChart(today)


def testMinute(seconds, hostname = "1.1.1.1"):
    failures = 0
    for i in range(seconds):
        connection = is_connected(hostname)
        if connection:
            #print("Internet is working")
            pass
        else:
            print("Internet is not working")
            failures+=1
        time.sleep(1)
    return failures

def is_connected(hostname):
  try:
    # a DNS listening
    host = socket.gethostbyname(hostname)
    # connect to the host -- tells us if the host is actually reachable
    s = socket.create_connection((host, 80), 2)
    s.close()
    return True
  except Exception:
     pass
  return False

def writeToFile(text, situation = "None"):
    now = datetime.now()
    now_edited = now.strftime("%Y%m%d_%H%M")
    f = open(f"log/{now_edited}_ISPHater.log", "a")
    f.write(text + "\n")
    f.close()

def createChart(today):
    now = datetime.now()
    now_edited = now.strftime("%Y%m%d_%H%M")
    now_title= now.strftime("%Y-%m-%d %H:%M")

    df = pd.DataFrame(today, columns =['Time', 'Failures'])
    print(df)
    title = f"Internet Connection Failure Rate (Intergga Arlesheim) <br><sup>{now_title} | ~1 check per second | 1.1.1.1</sup> "
    fig = px.area(df, x="Time", y='Failures', title=title)
    fig.update_layout(yaxis_range=[0,1], xaxis_title="Time", yaxis_title="Failure Rate",plot_bgcolor="white")
    fig.write_image(f"img/{now_edited}_intergga.jpg", scale = 3)

if __name__ == '__main__':
    main()


