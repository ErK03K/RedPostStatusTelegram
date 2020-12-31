import json
import requests as r
from flask import Flask, request, Response, jsonify

app = Flask(__name__)

try:
    with open('status.json', 'r', newline='') as guides:
        data = json.loads(guides.read().strip())

except:
    with open('status.json', 'w', newline='') as guides:
        data = {}
        json.dump(data, guides)


urlTelegram = 'https://api.telegram.org/bot<BOT_API_KEY>/sendMessage'


def appendguide(guide, filename='status.json'):
    try:
        with open(filename, 'r', newline='') as guides:
            data = json.loads(guides.read().strip())
            guides.close()
            if guide not in list(data.keys()):
                with open(filename, 'w', newline='') as guides:
                    data[guide] = 'New'
                    json.dump(data, guides)
                    return f'Guía {guide} agregada satisfactoriamente.'
            else:
                return f'Guía {guide} ya registrada.'


    except Exception as e:
        return f'Ha ocurrido el siguiente error: {str(e)}'

def removeguide(guide, filename='status.json'):
    try:
        with open(filename, 'r', newline='') as guides:
            data = json.loads(guides.read().strip())
            guides.close()
            if guide in list(data.keys()):
                with open(filename, 'w', newline='') as guides:
                    data.pop(guide)
                    json.dump(data, guides)
                    return f'Guía {guide} removida satisfactoriamente.'
            else:
                return f'Guía {guide} no registrada.'
    except Exception as e:
        return f'Ha ocurrido el siguiente error: {str(e)}'

def statusguide(guide, filename='status.json'):
    try:
        with open(filename, 'r', newline='') as guides:
            data = json.loads(guides.read().strip())
            guides.close()
            if guide in list(data.keys()):
                return f'Último registro: {data[guide]}'
            else:
                return f'Guía {guide} no registrada.'
    except Exception as e:
        return f'Ha ocurrido el siguiente error: {str(e)}'

def listguides(filename='status.json'):
    try:
        with open(filename, 'r', newline='') as guides:
            data = json.loads(guides.read().strip())
            guides = [guide for guide in data]
            guides = '\n'.join(guides)
            return f'Guías registradas:\n\n{guides}'
    except Exception as e:
        return f'Ha ocurrido el siguiente error: {str(e)}'



# FIN Bloque JSON


def getlastMsg(msg):
    chat_id = msg['message']['chat']['id']
    text = msg['message']['text']
    return text,chat_id

@app.route('/telegram', methods=['GET'])
def telegram():
    with open('status.json', 'r') as f:
        return jsonify(json.loads(f.read()))

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        msg = request.get_json()

        lastmsg, chat_id = getlastMsg(msg)

        if lastmsg.split()[0] == '!red' and lastmsg.split()[1] == 'add':
            guide = lastmsg.split()[2]

            action = appendguide(guide, 'status.json')
            r.post(urlTelegram, data={'chat_id':chat_id, 'text':action})

        elif lastmsg.split()[0] == '!red' and lastmsg.split()[1] == 'del':
            guide = lastmsg.split()[2]

            action = removeguide(guide, 'status.json')
            r.post(urlTelegram, data={'chat_id':chat_id, 'text':action})

        elif lastmsg.split()[0] == '!red' and lastmsg.split()[1] == 'status':
            guide = lastmsg.split()[2]

            action = statusguide(guide, 'status.json')
            r.post(urlTelegram, data={'chat_id':chat_id, 'text':action})

        elif lastmsg.split()[0] == '!red' and lastmsg.split()[1] == 'list':

            action = listguides('status.json')
            r.post(urlTelegram, data={'chat_id':chat_id, 'text':action})

        return Response('Ok', status=200)
    else:
        return '<h1>MÉTODO: GET</h1>'





if __name__ == '__main__':
    app.run(debug=True)
