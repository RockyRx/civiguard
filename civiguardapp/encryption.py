import hashlib

def encrypt(value):
	m = hashlib.md5()
	m.update(value)
	envalue = m.hexdigest() 
	return envalue