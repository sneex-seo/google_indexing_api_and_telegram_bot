from oauth2client.service_account import ServiceAccountCredentials
import time
import httplib2
from datetime import date
import telebot 
import json

bot_token = ''
bot = telebot.TeleBot(bot_token)

JSON_KEY_FILE = "client_secrets.json"
SCOPES = ["https://www.googleapis.com/auth/indexing"]


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):

    # https://developers.google.com/search/apis/indexing-api/v3/prereqs#header_2

    credentials = ServiceAccountCredentials.from_json_keyfile_name(JSON_KEY_FILE, scopes=SCOPES)
    http = credentials.authorize(httplib2.Http())

    ENDPOINT = "https://indexing.googleapis.com/v3/urlNotifications:publish"
    
    indexing_list = message.text.split()

    bot.send_message(message.chat.id, 'Получил список ссылок: ' + message.text)

   # print("U: {} type: {}".format(u, type(u)))
    
    for site_url in indexing_list:
        bot.send_message(message.chat.id, 'Пробую просканировать: ' + site_url)
        content = {}
        content['url'] = site_url
        content['type'] = "URL_UPDATED"
        json_ctn = json.dumps(content)    
        
        #print(json_ctn)
        
        response, content = http.request(ENDPOINT, method="POST", body=json_ctn)

        result = json.loads(content.decode())

        # For debug purpose only
        if("error" in result):
            print("Error({} - {}): {}".format(result["error"]["code"], result["error"]["status"], result["error"]["message"]))
            bot.send_message(message.chat.id, 'Ошибка попробуй позже')

        else:
            print("urlNotificationMetadata.url: {}".format(result["urlNotificationMetadata"]["url"]))
            print("urlNotificationMetadata.latestUpdate.url: {}".format(result["urlNotificationMetadata"]["latestUpdate"]["url"]))
            print("urlNotificationMetadata.latestUpdate.type: {}".format(result["urlNotificationMetadata"]["latestUpdate"]["type"]))
            print("urlNotificationMetadata.latestUpdate.notifyTime: {}".format(result["urlNotificationMetadata"]["latestUpdate"]["notifyTime"]))
            bot.send_message(message.chat.id, 'Проиндексировал ссылку: ' + site_url)

        time.sleep(10)




while True: 
    try:      
        if __name__ == '__main__':
            bot.polling(none_stop=True)
    except:
        time.sleep(5)