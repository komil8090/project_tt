from email.mime.text import MIMEText
from aiosmtplib import SMTP
import asyncio

sender = 'jasurmavloniy24@gmail.com'
password = 'lqil zdsp jkgi ezhy'

receivers = [

]

html = """
<h2>Assalomu alaykum!</h2>
<p><b>SMTP</b> orqali yuborildi.</p>
"""

message = MIMEText(html,'html')


# content-type => application/json
# text/html




async def send_one(receiver):
    msg = MIMEText(html, "html")
    msg["Subject"] = "Python SMTP Test"
    msg["From"] = sender
    msg["To"] = receiver

    server = SMTP(hostname="smtp.gmail.com", port=587, start_tls=True)
    await server.connect()
    await server.login(sender, password)
    await server.send_message(msg)
    await server.quit()

    print(f"{receiver} ga yuborildi")


    


async def main():
    tasks = [send_one(r) for r in receivers]
    await asyncio.gather(*tasks)
    
asyncio.run(main())
