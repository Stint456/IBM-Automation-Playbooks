#!/usr/bin/python
# coding: utf-8
import requests
import csv
import json
import time
import pandas as pd 
from datetime import datetime
import configparser
import urllib
import sys
from urllib.parse import urlencode
config = configparser.ConfigParser()
property_file = sys.argv[1]
config.read(property_file, encoding='utf-8-sig')
search_key = config.get("Search_Module", "search_key")
Cert_Match_file = config.get("AutoSync_Folder", "Cert_Match_file")
proxy_host = config.get("Certificate_Manager_API", "proxy_host")
proxies = { "http": proxy_host , "https": proxy_host}


#df = pd.read_csv(config.get("AutoSync_Folder", "DPCert_Manager_File"))
df = pd.read_csv(config.get("AutoSync_Folder", "Del_Data_file"))
Matched_Cert = []
Non_Matched_Cert = []
# Just use 'w' mode in 3.x
for index, row in df.iterrows():
    #date_time_str = row[search_key]
    #print(date_time_str)
    CM_Cert_Name = row[search_key]
    Matched_Cert.append(CM_Cert_Name) 
    
Matched_Set = set(Matched_Cert)
Matched_Cert = list(dict.fromkeys(Matched_Cert))
#Non_Matched_Cert  = list(dict.fromkeys(Non_Matched_Cert))
#print(Non_Matched_Cert)
print(Matched_Cert)
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
proxies = { "http": proxy_host , "https": proxy_host}
Cert_PATH = config.get("AutoSync_Folder", "Import_Cert_Path")
delete_url = config.get("Certificate_Manager_API", "delete_url")
Base_URL = config.get("Certificate_Manager_API", "base_url") 
#Cert_Manager_Inst = urllib.quote(config.get("Certificate_Manager_API", "LLE_DPCertificate_Instance"), '')
Cert_Manager_Inst = urllib.parse.quote(config.get("Certificate_Manager_API", "Certificate_Instance"), safe='')
search_url = Base_URL+Cert_Manager_Inst+"/certificates/search?search_text="
#Fetch the Access Token
response_decoded_json = requests.post(token_url, data=payload, headers=header)
response_json = response_decoded_json.json()
access_key = response_json['access_token']
#Cert_PATH = config.get("AutoSync_Folder", "ReImport_Cert_Path")
#arr_txt = [x for x in os.listdir(Cert_PATH) if x.endswith(".pem")]
#print(arr_txt)
print("No Updated Certificates found")
for x in Matched_Cert:
    search_file=x
    #rpl_r = x.replace("\r", "")
    #search_text = "\""+rpl_r+"\""
    #print(search_text)
    Cert_PATH_File=Cert_PATH+"/"+search_file
    search_Cert_url=search_url+search_file
    print(search_Cert_url)
    hed = {"Authorization": "Bearer " +access_key,"content-type": "application/json"}
    getReq = requests.get(search_Cert_url, headers = hed)
    cert_data=json.loads(getReq.content)
    #output=y.get(certificates._id)
    value = cert_data['certificates'][0]['_id']
    print(value)
    #encoded_value = urllib.quote(value, '')
    encoded_value = urllib.parse.quote(value, safe='')
    print(encoded_value)
    #print(reimport_url+encoded_value)
    #Delete Certificates
    hed = {"Authorization": "Bearer " +access_key,"content-type": "application/json"}
    delreq = requests.delete(delete_url+encoded_value, headers = hed)
    print(delreq.content)
   


  

 



    
    


