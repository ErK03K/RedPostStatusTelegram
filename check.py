import requests as r, json, re
from time import sleep


urlTelegram = 'https://api.telegram.org/bot<BOT_API_KEY>/sendMessage'



def cStatusp(guide):
    url = 'https://www.redpack.com.mx/wp-admin/admin-post.php'
    datap = {
        'action' : 'track_shipping',
        'trackShipping' : '1',
        'number_guide' : guide, # Tu numero de guia
        'rastrear' : 'Buscar'
    }
    s = r.Session()

    vc = s.post(url,data=datap).text.split('<!--Detalle del paquete -->')[1].split('<!--End wrapper guide-->')[0].replace('\n','').replace('\t','').replace('\r','').split('<div class="view-packages history-package-custom">')[1]
    f = [x.replace('<h5>','').replace('&nbsp;',' ').replace('</h5>','').replace('.','-') for x in re.findall(r'<h5>.{1,150}</h5>',vc)]
    for update in reversed(f):
        if update != data[guide]:
            tgdata = {'chat_id':'<CHAT_ID>', 'text':f'\N{white heavy check mark} : {update}'}
            s.post(urlTelegram, data=tgdata)
            with open('status.json', 'w', newline='') as guides:
                data[guide] = update
                json.dump(data, guides)
                return

if __name__ == '__main__':
    while True:
        with open('status.json', 'r', newline='') as guides:
            data = json.loads(guides.read().strip())
            for i in data:
                cStatusp(i)
            sleep(1800)

