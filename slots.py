import requests
import json
import smtplib
from email.message import EmailMessage
import time

def email_alert(subject, body, to):
	msg = EmailMessage()
	msg.set_content(body)
	msg['subject'] = subject
	msg['to'] = to

	user = "ankur.6nov@gmail.com"
	msg["from"] = user
	password = "hunjhindprhijqde"
	server = smtplib.SMTP("smtp.gmail.com", 587)
	server.starttls()
	server.login(user, password)
	server.send_message(msg)
	server.quit()


headers = {
	"authority": "cdn-api.co-vin.in",
	"method": "GET",
	"path": "/api/v2/appointment/sessions/public/calendarByDistrict?district_id=637&date=21-05-2021",
	"scheme": "https",
	"accept": "application/json, text/plain, */*",
	"accept-encoding": "gzip, deflate, br",
	"accept-language": "en-US,en;q=0.9,hi;q=0.8",
	"cache-control": "no-cache",
	"origin": "https://www.cowin.gov.in",
	"pragma": "no-cache",
	"referer": "https://www.cowin.gov.in/",
	"sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
	"sec-ch-ua-mobile": "?0",
	"sec-fetch-dest": "empty",
	"sec-fetch-mode": "cors",
	"sec-fetch-site": "cross-site",
	"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36",
}

while(1):
	for ind in range(7):
		date = str(ind+22)+"-05-2021"
		"""
		For bareilly
		"""
		districtId = "637"
		print("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id="+districtId+"&date="+date)

		slots_for_today = requests.get("https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id="+districtId+"&date="+date, headers= headers, verify= False)

		slots = json.loads(slots_for_today.text)

		# print(slots_for_today)

		dose2_centers = []
		dose1_centers = []

		for i in slots["centers"]:
			for j in i["sessions"]:
				if j["min_age_limit"] == 18 or j["min_age_limit"] == "18":
					if j["available_capacity_dose2"] != 0:
						dose2_centers.append(i["name"])
						print("Dose 2 available at: ", i["name"])
					if j["available_capacity_dose1"] != 0:
						dose1_centers.append(i["name"])
						print("Dose 1 available at: ", i["name"])

		mail_sub = "Slots available for: "+date
		if len(dose2_centers):
			email_alert(mail_sub, "Doses available at: " + str(dose2_centers), "sharma.ankur0277@gmail.com")
		if len(dose1_centers):
			email_alert(mail_sub, "Doses available at: " + str(dose1_centers), "abisht1996@gmail.com")

	print("wait for 5 mins for rescan")
	time.sleep(300)