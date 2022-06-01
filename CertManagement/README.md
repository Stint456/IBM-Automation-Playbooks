### CertManagement
Import / Delete / Search Certificates and create secrets in cluster
### Pre-Requsites
1. IBM Certificate Manager Instance to be created
2. API Key for accessing Certificate manager Service to be created
3. Python Environment required
### Configuration
### config.properties - Used to specify the configuration to (Folder / Search Key / Cloud API)
## [AutoSync_Folder]
Temp_Data_file = <CSV_FILE_PATH>

Del_Data_file = <CSV_FILE_PATH>

Import_Cert_Path = <CERTS_PATH>

Import_Cert_Path_Private = <PRIVATE_CERT_PATH>

Import_File_Name = .pem < File Extension>

## [Search_Module]
search_key = name
# [Secret_Management_API]
create_secret = https://containers.cloud.ibm.com/global/ingress/v2/secret/createSecret

delete_secret = https://containers.cloud.ibm.com/global/ingress/v2/secret/deleteSecret

get_secret = https://containers.cloud.ibm.com/global/ingress/v2/secret/getSecrets

update_secret = https://containers.cloud.ibm.com/global/ingress/v2/secret/updateSecret
# [Certificate_Manager_API]
proxy_host = <Proxy_URL>

token_url = https://iam.cloud.ibm.com/identity/token

base_url = https://us-south.certificate-manager.cloud.ibm.com/api/v3/

reimport_url = https://us-south.certificate-manager.cloud.ibm.com/api/v1/certificate/

delete_url = https://us-south.certificate-manager.cloud.ibm.com/api/v2/certificate/

api_key = <API_KEY>

Certificate_Instance = <Certificate_Instance_ID>
