import requests
import json
import os
import csv
import urllib
import configparser
import pandas as pd
import time
from datetime import datetime
#Access Token URL - Pass the API Key and get Token
config = configparser.ConfigParser()
property_file = sys.argv[1]
config.read(property_file, encoding='utf-8-sig')
token_url = config.get("Certificate_Manager_API", "token_url")
api_key = config.get("Certificate_Manager_API", "api_key")
Temp_Data_file = config.get("AutoSync_Folder", "Temp_Data_file")
payload = {"grant_type": "urn:ibm:params:oauth:grant-type:apikey" , "apikey": api_key}
header = {"Content-type": "application/x-www-form-urlencoded",
          "Accept": "application/json"} 

response_decoded_json = requests.post(token_url, data=payload, headers=header)
response_json = response_decoded_json.json()
access_key = response_json['access_token']
#Search_Certs and write Cert-Manager_Inventory
Base_URL = config.get("Certificate_Manager_API", "base_url") 
Cert_Manager_Inst = urllib.parse.quote(config.get("Certificate_Manager_API", "Certificate_Instance"), safe='')
All_Certs_Search = Base_URL+Cert_Manager_Inst+"/certificates?order=expires_on&page_number=1&page_size=200"

#All_Certs_Search = Base_URL+Cert_Manager_Inst+"/certificates/search?order=expires_on&search_text=prdldb&page_size=100&page_number=0"
#All_Certs_Search = Base_URL+Cert_Manager_Inst+"/certificates?page_number=2&page_size=200"
access_token=access_key
hed = {"Authorization": "Bearer " +access_key,"content-type": "application/json"}
getReq = requests.get(All_Certs_Search, headers = hed)
cert_data=json.loads(getReq.content)
#output=y.get(certificates._id)
#value = cert_data['certificates'][0]['_id']
cert_Value = cert_data['certificates']
dataframe = pd.DataFrame.from_dict(cert_Value)
fnames = ["CRN_Id","name", "CREATION", "EXPIRATION","ISSUER","algorithm","key_algorithm","domains"]
f1 = open(Temp_Data_file, 'w')
with f1:
#fnames = ['first_name', 'last_name']
    writer = csv.DictWriter(f1, fieldnames=fnames) 
    writer.writeheader()
    for index, row in dataframe.iterrows():
    #date_time_str = row[search_key]
    #print(date_time_s#tr)
    #for index2 , row2 in df3.iterrows():
        #date_time_str = row['EXPIRATION']
        filename = row['name'] 
        issuer = row['issuer']
        crn_id = row['_id']
    #Expiry_ts = row['expires_on'] / 1000
        Expiry_ts = time.strftime("%m/%d/%Y", time.localtime(row['expires_on'] / 1000))
    #Server_date_Expiry = datetime.strptime(date_time_str.replace(" ", ""), '%m/%d/%Y').date()
        Expiry_date = datetime.strptime(Expiry_ts.replace(" ", ""), '%m/%d/%Y').date()
        begin_ts = time.strftime("%m/%d/%Y", time.localtime(row['begins_on'] / 1000))
    #Server_date_Expiry = datetime.strptime(date_time_str.replace(" ", ""), '%m/%d/%Y').date()
        begin_date = datetime.strptime(begin_ts.replace(" ", ""), '%m/%d/%Y').date()
        algorithm = row['algorithm'] 
        key_algorithm = row['key_algorithm'] 
        domains = row['domains'] 
        writer.writerow({'CRN_Id' : crn_id, 'name' : filename, 'CREATION': begin_date ,'EXPIRATION': Expiry_date,'ISSUER': issuer,"algorithm":algorithm,"key_algorithm":key_algorithm,"domains":domains})
    
        #print(CM_date_Expiry)
     #   File_Name = row['name'] 
            #print("else"+File_Name)
    f1.close()
  
