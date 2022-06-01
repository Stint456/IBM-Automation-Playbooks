import requests
import json
import os
import configparser
import urllib
import pandas as pd
from urllib.parse import urlencode

#Access Token URL - Pass the API Key and get Token
config = configparser.ConfigParser()
property_file = sys.argv[1]
config.read(property_file, encoding='utf-8-sig')
token_url = config.get("Certificate_Manager_API", "token_url")
api_key = config.get("Certificate_Manager_API", "api_key")
payload = {"grant_type": "urn:ibm:params:oauth:grant-type:apikey" , "apikey": api_key}
header = {"Content-type": "application/x-www-form-urlencoded",
          "Accept": "application/json"} 
#Set Headers & Define Variable for Certificate Import
contenttype="application/json"
private_key=""
internediate=""
secretname=""
cluster=""
namespace=""

#Post the Request to extract Token 
response_decoded_json = requests.post(token_url, data=payload, headers=header)
response_json = response_decoded_json.json()
access_key = response_json['access_token']
#print(access_key)
#Set Certificate File Directory

Cert_PATH = config.get("AutoSync_Folder", "Import_Cert_Path")
Cert_PATH_Private = config.get("AutoSync_Folder", "Import_Cert_Path_Private")
Cert_Manager_Inst1 = config.get("Certificate_Manager_API", "Certificate_Instance")
Cert_Manager_Inst = urllib.parse.quote(config.get("Certificate_Manager_API", "Certificate_Instance"), safe='')
Base_URL = config.get("Certificate_Manager_API", "base_url")
Cert_Import_url = Base_URL+Cert_Manager_Inst+'/certificates/import'
create_secret_url = config.get("Secret_Management_API", "create_secret")
File_Name = config.get("AutoSync_Folder", "Import_File_Name")
#print (Cert_Import_url)
os.chdir(Cert_PATH)
#Cert Manager Allows only .PEM file format ( Read Certificate Content & Write the Content Body in JSON File
arr_txt = [x for x in os.listdir() if x.endswith(File_Name)]
os.chdir(Cert_PATH_Private)
arr_txt1 = [x1 for x1 in os.listdir() if x1.endswith(File_Name)]
#print(arr_txt)
for x in arr_txt:
    for x1 in arr_txt1:
        print(x+":"+x1)
        if (x==x1):
            f =  open(Cert_PATH_Private+"/"+x1 ,'r')
            content1=f.read()
            private_key = content1  
        else:
            private_key = ""
        
    Cert_PATH_File=Cert_PATH+"/"+x
    cert_name = x[0:len(x)-4].lower()
    #txt = "apple#banana#cherry#orange"

    # setting the maxsplit parameter to 1, will return a list with 2 elements!
    splitcertname = cert_name.split(".", 2)
    secretname = splitcertname[0]
    cluster = splitcertname[1]
    namespace = splitcertname[2]
    print(secretname + ":" + cluster + ":" + namespace)

    f1 =  open(Cert_PATH_File ,'r')
    content=f1.read()
    x1 = {
    "name":cert_name,
    "description":cert_name,
    "data":{
        "content":content,
        "priv_key":private_key,
        "intermediate":internediate
           }
     }
    
    y=json.dumps(x1)
    print(y)


    #Post the Certificate Content Using Post Method
    hed = {"Authorization": "Bearer " +access_key,"content-type": contenttype}
    #print("Bearer " +access_key)
    insert = requests.post(Cert_Import_url, data = y, headers = hed)
    print(insert.content)
    cert_data=json.loads(insert.content)
    dataframe = pd.DataFrame.from_dict(cert_data)
    for index , row in dataframe.iterrows():
        crn_id = row['_id']      
        #  print(crn_id)          
        x2 = {
             "cluster": cluster,
             "crn": crn_id,
             "name": secretname,
             "namespace": namespace ,
             "persistence": bool(1)
           }
        y1=json.dumps(x2) 
        print(y1)
    #Create Secret  Content Using Post Method    
        hed = {"Authorization": "Bearer " +access_key,"content-type": contenttype,"accept": contenttype}
        s = requests.post(create_secret_url, data = y1, headers = hed)
        print(s.content)
        
      

