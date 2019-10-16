import requests
import json
import time

url = 'https://www.virustotal.com/vtapi/v2/domain/report'
API_KEY = 'YOU_VT_API_KEY'
DOMAIN = 'api.telegram.org'

##################################################
# Extract malicious exposed Telegram APIs on VirusTotal
##################################################


def extract_domain(params_new):
    try:
        response = requests.get(url, params=params_new)
        response_json = response.json()
        detected_urls = response_json['detected_urls']
        undetected_urls = response_json['undetected_urls']

        for detected_url in detected_urls:
            link_url = detected_url['url']
            response_url = requests.get(link_url)
            if response_url.status_code == 200:
                txt_page = response_url.text
                json_string = json.loads(txt_page)
                username = json_string['result']['username']
                print("{};{}".format(username, link_url))

        for undetected_url in undetected_urls:
            time.sleep(0)
            try:
                response_url = requests.get(undetected_url[0])
                if response_url.status_code == 200:
                    if "documents" in undetected_url[0]:
                        print(undetected_url[0])
                    else:
                        txt_page = response_url.text
                        json_string = json.loads(txt_page)
                        if json_string['result']['from']:
                            username = json_string['result']['from']['username']
                            chat_id = json_string['result']['chat']['id']
                            print("bot_name:{};chat_id:{};link:{}".format(username, chat_id, undetected_url[0]))
                        else:
                            username = json_string['result']['username']
                            print("{}".format(username))
            except Exception as e:
                print(e)

    except Exception as e:
        print(e)


if __name__ == '__main__':
    params = {'apikey': API_KEY, 'domain': DOMAIN}
    extract_domain(params)
