import re
from urllib.request import urlopen
from urllib.parse import quote
#sfsdgsdfgfg
pRm = r'<p class="date dateFree">(\d{1,2})</p>'
pDt = r'<p class="date ">(\d{1,2})</p>'
pMh = r'<p class="month">(\w+)</p>'
pTr = r'<span>([+-]\d+|0)&deg;</span>'

P_ENC = r'\bcharset=(?P<ENC>.+)\b'

def getencoding(http_file):
    '''Отримати кодування файлу http_file з Інтернет.'''
    headers = http_file.getheaders()    # отримати заголовки файлу

    dct = dict(headers)                 # перетворити у словник

    content = dct.get('Content-Type','')# знайти 'Content-Type'

    mt = re.search(P_ENC, content)      # знайти кодування (після 'charset=' )

    if mt:
        enc = mt.group('ENC').lower().strip() # виділити кодування
    elif 'html' in content:
        enc = 'utf-8'
    else:
        enc = None
    return enc

city=input('Яким містом цікавитесь?')

url = "https://ua.sinoptik.ua/" + quote('погода',encoding='utf-8') + '-' + quote(city,encoding='utf-8')

http_file = urlopen(url)

s = ''
enc = getencoding(http_file)
for line in http_file:
    s += str(line, encoding=enc)

dd = re.findall(pRm, s)
idd = re.findall(pDt, s)

ad = idd + dd
pm = re.findall(pMh, s)
pt = re.findall(pTr, s)

data = [dd for dd in ad if dd[0]!='0']
data_with0 = [dd0 for dd0 in ad if dd0[0] == '0']
list_data = data+data_with0


pt_min = pt[::2]
pt_max = pt[1::2]


for data, month, min_t, max_t in zip(list_data,pm,pt_min,pt_max):
    print(f"Погода в місті {city} на {data} {month} мінімальна: {min_t}, максимальна: {max_t}")
