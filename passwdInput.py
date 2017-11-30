import hashlib
import getpass
def getPasswdInput(logginginUser):
	ret=False
	dic={};dic["Net"]="391b6629d9b645d3073c6f5ad432c40537646604";dic["Waii"]="8f2d8845f955ce58189ea828b40c802e52650b2c"
	pw = getpass.getpass()
	if logginginUser not in dic:
		return ret
	m=hashlib.sha1((pw).encode('utf-8')).hexdigest()
	if m==dic[logginginUser]:
		ret=True
	return ret