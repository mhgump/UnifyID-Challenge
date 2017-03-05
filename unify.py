
## Unify ID Challenge 
## Random.org
## By Michael Gump

## Refrences :

# https://pypi.python.org/pypi/json-rpc
# https://api.random.org/json-rpc/1/introduction
# https://en.wikibooks.org/wiki/Python_Imaging_Library/Editing_Pixels

### First Beta Key : 1b559a30-1759-4678-b968-ea671a497298
### Request One @ https://api.random.org/api-keys/beta

import requests
import json

from PIL import Image

import math
import random


url = "https://api.random.org/json-rpc/1/invoke"

## We need at least two API keys do make a 128*128*3 image

api_keys = ["1b799a1d-3c60-4bf5-84a0-071c30998c95", #random1unifyid@gmail.com
			"4dceb12f-4a58-4c05-b287-53636edd93dc"  #random2unifyid@gmail.com
			]
api_key = api_keys.pop()

headers = {'content-type': 'application/json'}


def get_usage():
	global api_key 
	global api_keys
	
	payload = {
	"jsonrpc": "2.0",
	"method": "getUsage",
	"params": {
		"apiKey": api_key
	},
	"id": 15998
}
	response = requests.post(url, data=json.dumps(payload), headers=headers).json()
	result = None
	try:
		result = response['result']['bitsLeft']
	except:
		print(response)
	return result
def generate_blobs(num_bits,chunks):
	global api_key 
	global api_keys

	payload = {
		"jsonrpc": "2.0",
		"method": "generateBlobs",
		"params": {
			"apiKey": api_key,
			"n": chunks,
			"size": num_bits,
			"format": "hex"
		},
		"id": 42
	}
	if num_bits*chunks>get_usage():
		api_key = api_keys.pop()
	response = requests.post(url, data=json.dumps(payload), headers=headers).json()
	result = None
	try:
		result = response['result']['random']['data']
	except:
		print(response)
	return result
def generate_integers(min,max,n):
	global api_key
	global api_keys

	payload = {
		"jsonrpc": "2.0",
		"method": "generateIntegers",
		"params": {
			"apiKey": api_key,
			"n": n,
			"min": min,
			"max": max
		},
		"id": 42
	}
	if math.log(max-min)*n>get_usage():
		api_key = api_keys.pop()
	response = requests.post(url, data=json.dumps(payload), headers=headers).json()
	result = None
	try:
		result = response['result']['random']['data']
	except:
		print(response)
	return result

def random_rgb(size,filename = 'random_rgb.bmp'): 
	# The resultant image will be square with dimensinos size x size
	# Uses the python PIL library
	img = Image.new( 'RGB', (size,size), "black")
	pixels = img.load()
	for i in range(0,size):
		# n has allowable range [1,10000]
		pixel_values = generate_integers(0,255,size*3)
		for j in range(0,size):
			r = pixel_values[3*(j)]
			g = pixel_values[3*(j)+1]
			b = pixel_values[3*(j)+2]
			pixels[i,j] = (r,g,b)
	img.save(filename)

# random_rgb(128) #will take 393216 bits, more than a beta key's 250000 available bits


# Test, 2400 bits
print(get_usage())
random_rgb(10,filename = 'test.bmp')
print(get_usage())

def random_dot_org(n):
	return generate_blobs(n*8,1)[0].decode('hex')

from Crypto.PublicKey import RSA

def generate_rsa_key(bits):
	if bits%256 != 0 or bits < 1024:
		return
	keys = RSA.generate(bits,randfunc=random_dot_org) 
	public_key = keys.publickey().exportKey("PEM") 
	private_key = keys.exportKey("PEM") 
	return private_key, public_key

# bits = 1024
# print(get_usage()) ## Will use about 2*bits
# print(generate_rsa_key(bits))
# print(get_usage())



