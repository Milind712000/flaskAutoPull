import os, json, hmac, hashlib, base64
from flask import Flask, request, jsonify

app = Flask(__name__)

config = {
	'lambda' : {
		'loc':'dsfad',
		'secret':'fasdf'
	}
}

@app.route('/sample/<int:id>', methods=['POST'])
def sampleJson(id):
	if (int(id) & 1):
		return ("id : " + str(id))
	
	payload = request.get_json()

	return jsonify(payload)









@app.route('/webhook/<string:id>', methods=['POST', 'GET'])
def verifyPostData(id):
	if request.method == "GET":
		return "its up and running"

	payload = json.dumps(request.get_json(), separators=(',', ':'))
	checksum = request.headers['X-Hub-Signature']

	if not payload:
		return next('Request body empty')
	
	repo = config[id]
	secret = repo['secret']

	digester = hmac.new(secret.encode(), payload.encode(), hashlib.sha1)
	signature = "sha1=" + digester.hexdigest()

	# if (not checksum or not signature or signature != checksum):
	if hmac.compare_digest(signature, checksum):
		print("verified")
		return "Verified"
	else :
		msg = 'Request body digest ({}) did not match X-Hub-Signature ({})'.format(signature,checksum)
		print(msg)
		return msg














@app.route('/', methods=['GET'])
def index():
	return 'The Server is running'

if __name__ == "__main__":
	app.run(debug=True)