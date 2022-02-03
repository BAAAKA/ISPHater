import discord
from pythonping import ping
import time
import datetime

# GetTokenOfDiscordBot
with open('token.txt','r') as f:
    lines = f.readlines()
token = lines[0]

print("Token: {}".format(token))
ip = '1.1.1.1' #Any big cooperation IP would do

currentIssue = []
activity = discord.Game(name="DOES MY INTERNET WORK?", type=3)
targetChannelID = 935630315488182282

client = discord.Client()
@client.event
async def on_ready():
    channel = client.get_channel(targetChannelID)
    activity = discord.Game(name="DOES MY INTERNET WORK?", type=3)
    await client.change_presence(status=discord.Status.online, activity=activity)
    print("[INFO] ISP HATER {} is ready!".format(client.user))
    await pinging(channel)

async def pinging(channel):
    global ip
    global currentIssue
    print(f"Start pinging {ip}")
    while(True):
        result = ping(ip, verbose=False, count=1)
        now = str(datetime.datetime.now().time())[:-7]
        output = str(result).partition('\n')[0]
        if(result.success()):
            await success(channel, now, output)
        else:
            await failure(channel, now, output)
        time.sleep(5)

async def failure(channel, now, output):
    text = '[FAILURE] {} - {}'.format(now, output)
    print(text)
    currentIssue.append(now)

async def success(channel, now, output):
    global currentIssue
    print(f'[SUCCESS] {now} - {output}')
    if(currentIssue):
        if currentIssue[-1] == currentIssue[0]:
            message = '`ISSUE - {}`'.format(currentIssue[0])
        else:
            message = '`ISSUE - {} to {}`'.format(currentIssue[0], currentIssue[-1])
        sendSuccess = await sendToDiscord(channel, message)
        if(sendSuccess):
            currentIssue = []

async def sendToDiscord(channel, message):
    global currentIssue
    try:
        await channel.send(message)
        return True
    except Exception as e:
        print("[EXCEPTION] couldnt send message to discord: {}".format(e))
        return False

client.run(token)

