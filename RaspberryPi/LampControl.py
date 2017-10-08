import requests
import json

class LampControl:
	url_on_off = "http://192.168.1.249/api/IrRsiioaBMWqQ2PUjdB4TbqkzfeBsdHtZAB25EGL/lights/11/state"
	url_state = "http://192.168.1.249/api/IrRsiioaBMWqQ2PUjdB4TbqkzfeBsdHtZAB25EGL/lights/11"
	"""Controls the lamp and stores current status"""

	def __init__(self):
		self.status = False

	def turnOn(self):
		self.turn_lamp_on(self.url_on_off, True)
		print("Turned the Lamp On!")
		self.status = True

	def turnOff(self):
		self.turn_lamp_on(self.url_on_off, False)
		print("Turned the Lamp Off!")
		self.status = False

	def toggle(self):
		if self.status:
			self.turnOff()
		else:
			self.turnOf()


	def turn_lamp_on(url, state):
		payload = json.dumps({"on":state})
		r = requests.put(url, data = payload)
		print(r.content)

	def statusReadable(self):
		if self.status:
			return "ON"
		else:
			return "OFF"


	def is_lamp_on(self):
		response = requests.get(url = self.url_state)
		json_response = response.json()
		data = json.dumps(json_response)
		data = json.loads(data)
		reachable = data["state"]["reachable"]
		is_on = data["state"]["on"]
		if  not reachable:
			return False
		elif reachable and not is_on:
			return False
		elif reachable and is_on:
			return True
		return None
