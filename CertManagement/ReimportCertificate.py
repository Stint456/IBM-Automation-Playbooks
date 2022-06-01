#!/usr/bin/env python
# coding: utf-8
import requests
import json
import os
import csv
import urllib
from urllib.parse import urlencode
import configparser
import urllib
#from urllib.parse import urlencode

#Access Token URL - Pass the API Key and get Token
config = configparser.ConfigParser()
property_file = sys.argv[1]
config.read(property_file, encoding='utf-8-sig')
token_url = config.get("Certificate_Manager_API", "token_url")
api_key = config.get("Certificate_Manager_API", "api_key")

#Set Headers & Define Variable for Certificate Import
contenttype="application/json"
private_key=""
internediate=""
payload = {"grant_type": "urn:ibm:params:oauth:grant-type:apikey" , "apikey": api_key}
header = {"Content-type": "application/x-www-form-urlencoded",
          "Accept": "application/json"} 
proxy_host = config.get("Certificate_Manager_API", "proxy_host")
#proxies = { "http": proxy_host , "https": proxy_host}
Cert_PATH = config.get("AutoSync_Folder", "Import_Cert_Path")
reimport_url = config.get("Certificate_Manager_API", "reimport_url")
Base_URL = config.get("Certificate_Manager_API", "base_url") 
Cert_Manager_Inst = urllib.parse.quote(config.get("Certificate_Manager_API", "Certificate_Instance"), safe='')
search_url = Base_URL+Cert_Manager_Inst+"/certificates/search?search_text="
#Fetch the Access Token
response_decoded_json = requests.post(token_url, data=payload, headers=header)
response_json = response_decoded_json.json()
access_key = response_json['access_token']
#Specify the File to Search for Certificate
os.chdir(Cert_PATH)
#x=os.path.basename(CertificateFilePath)
arr_txt = [x for x in os.listdir(Cert_PATH) if x.endswith(".pem")]
print(arr_txt)
for x in arr_txt:
    x = x.replace("\r", "")
    Cert_PATH_File=Cert_PATH+"/"+x
    x = x[0:len(x)-4]
    search_Cert_url=search_url+x
    #Read the Certificate from Local File path
    f1 =  open(Cert_PATH_File ,'r')
    content=f1.read()
    x1 = {
         "content":content,
         "priv_key":private_key,
         "intermediate":internediate
     }    
    y=json.dumps(x1)
    print(y)
    hed = {"Authorization": "Bearer " +access_key,"content-type": "application/json"}
    getReq = requests.get(search_Cert_url, headers = hed)
    cert_data=json.loads(getReq.content)
    #output=y.get(certificates._id)
    value = cert_data['certificates'][0]['_id']
    #print(value)
    encoded_value = urllib.parse.quote(value, safe='')
    #encoded_value = urllib.quote(value, '')
    #print(encoded_value)
    print(reimport_url+encoded_value)
    #Re-import Certificates
    hed = {"Authorization": "Bearer " +access_key,"content-type": "application/json"}
    putreq = requests.put(reimport_url+encoded_value, data = y, headers = hed)
    print(putreq)
