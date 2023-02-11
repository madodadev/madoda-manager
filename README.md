# madoda-manager v3
Download Youtube Video, Convert To Mp3, Remove Tags, Upload to google drive

## how to use
install all requirements
> pip3 install -r requirements.txt

### setup the app
#### copy google drive credentials to 
    ./assets/google_drive/client_ids if is client ids and 
    ./assets/google_drive/service_accounts if service accounts 
(you can use both but client_id has priority) 

## RUN Setup Agent
### The Setup Agent will ask for 
1. Google Drive Folder ID to Sotre Musics and logs
2. Client ID for Desktop For YOUTUBE OAuth 2.0 Auth
 *Use more then one Client ID to pass Youtube Upload Limit*
> python3 setup.py

### copy api_key to the host app
After run Setup Agent Copy api_key to madoda manager WP_Plugin
in settings page, for authentication

## run the app
>python3 main.py
