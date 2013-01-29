import strjson
creds = strjson.load('localcredentials.json')
import KDataPy.scripts.dataprocess.runLocalProcs as rp
rp.run(**creds)
