import requests
import hashlib
import json
from requests.exceptions import HTTPError

sJsonFile = 'answer.json'
urlGet    = "https://api.codenation.dev/v1/challenge/dev-ps/generate-data?token=5437fa01dc510624e116d59e39024b1a980a1e96"
urlPost   = "https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token=5437fa01dc510624e116d59e39024b1a980a1e96"

def cesarcript(sText, nStep):
	sCript = ''
	sText = sText.lower()
	
	for c in sText:
		if ord(c) < 97 or ord(c) > 122:
			sCript = sCript + c
		elif (ord(c) + nStep) <= 122:
			sCript = sCript + chr(ord(c) + nStep)
		else:
			nChar    = (ord(c) + nStep)
			nRestart = ((nChar - 122) + 97) - 1
			sCript   = sCript + chr(nRestart)

	return sCript

def cesardecript(sCriptText, nStep):
	sDecript = ''
	sCriptText = sCriptText.lower()
	
	for c in sCriptText:
		if ord(c) < 97 or ord(c) > 122:
			sDecript = sDecript + c
		elif (ord(c) - nStep) >= 97:
			sDecript = sDecript + chr(ord(c) - nStep)
		else:
			nChar    = (ord(c) - nStep)
			nRestart = (122 - (97 - nChar)) + 1
			sDecript = sDecript + chr(nRestart)

	return sDecript

try:
	response  = requests.get(urlGet)
	jsonInput = response.json()
except HTTPError as http_err:
	print(f'HTTP error occurrer: {http_err}')
except Exception as err:
	print(f'Other error occurred: {err}')
else:
	print('Success!')

with open(sJsonFile,'w') as outfile:
	json.dump(jsonInput, outfile)

with open(sJsonFile) as json_file:
	data = json.load(json_file)

	sDecript = cesardecript(data['cifrado'], data['numero_casas'])
	data['decifrado'] = sDecript

	hashVar = hashlib.sha1(sDecript.encode())
	data['resumo_criptografico'] = hashVar.hexdigest()

	print("json pre-send: ", data)

with open(sJsonFile,'w') as outfile:
	json.dump(data, outfile)

# Enviar o arquivo
try:
	jsonFile = {'answer': (sJsonFile, open(sJsonFile, 'rb'), 'multipart/form-data', {'Expires': '0'})}
	
	r = requests.post(urlPost, files=jsonFile)

	print(r.text)
except HTTPError as http_err:
	print(f'HTTP error occurrer: {http_err}')
except Exception as err:
	print(f'Other error occurred: {err}')
else:
	print('Success!')


