
## Unify ID Challenge 
## Random.org
## By Michael Gump

## Refrences :

# https://api.random.org/api-keys/beta
# https://pypi.python.org/pypi/json-rpc
# https://api.random.org/json-rpc/1/introduction
# https://en.wikibooks.org/wiki/Python_Imaging_Library/Editing_Pixels
# https://www.dlitz.net/software/pycrypto/api/current/Crypto-module.html

### Beta Key : 1b559a30-1759-4678-b968-ea671a497298
### Request One @ https://api.random.org/api-keys/beta

import requests
import json

from PIL import Image

import math
import random


url = "https://api.random.org/json-rpc/1/invoke"

## We need at least two API keys do make a 128*128*3 image

api_key = '1b559a30-1759-4678-b968-ea671a497298'

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
# I can not do this without getting multiple beta keys which will probably get me banned

# Test, 2400 bits
# print(get_usage())
# random_rgb(10,filename = 'test.bmp')
# print(get_usage())

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

def write_rsa_key(priv,pub):
	f = open('private_key.pem','wb')
	f.write(priv)
	f.close()
	f = open('public_key.pub','wb')
	f.write(pub)
	f.close()

# Generate an RSA public/private key pair
bits = 1024
priv,pub = generate_rsa_key(bits)
write_rsa_key(priv,pub)



