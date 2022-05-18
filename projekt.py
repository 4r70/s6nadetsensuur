from easygui import *
import requests
import re
from bs4 import BeautifulSoup

#api jaoks vajalikud asjad
client_access_token = '0cwbXv2AVjReCZYIxG5U8D0OD0a3SNtPGceMd0EoGIRPvyY4UrRXpTQjkBHCXI2P'
baas_url = 'https://api.genius.com'

kasutaja_sisend = enterbox("Tere, sisestage artist ja laulu pealkiri, mille lüürikat soovite tsensuurida")
kasutaja_sisend = kasutaja_sisend.replace(' ', '-')
keeled=["Eesti keeles", "Inglise keeles", "Vene keeles"]
keel=buttonbox("Valitud laul on... ", choices = keeled)


#api jaoks lingi koostamine
path = 'search/' 
request_uri = '/'.join([baas_url, path])

#api-le vajaliku info ettevalmistamine
parameetrid = {'q': kasutaja_sisend}
token = 'Bearer {}'.format(client_access_token)
headerid = {'Authorization': token}

#api-le päringu tegemine
try:
    page = requests.get(request_uri, params=parameetrid, headers=headerid)   
    sõnade_lk = page.json()['response']['hits'][0]['result']['url'] #leiab laulusõnade lingi
    sõnade_lk = sõnade_lk + '?react=1'
except:
    msgbox("Laulu ei leitud")
page = requests.get(request_uri, params=parameetrid, headers=headerid)
sõnade_lk = page.json()['response']['hits'][0]['result']['url'] #leiab laulusõnade lingi
sõnade_lk = sõnade_lk + '?react=1'


#sõnade scrapemine
page = sõnade_lk
page = requests.get(page)
supp = BeautifulSoup(page.text, 'html.parser')
tulemused = supp.find('div', class_='SongPageGriddesktop-sc-1px5b71-0 Lyrics__Root-sc-1ynbvzw-1 cjSQRu').get_text('\n') #leiab divi, mille sees on laulu sõnad ja liidab need reavahetusega kokku
tulemused = re.sub(r'\[.*?\]', '', tulemused) #eemaldab ebavajalikud märgid
artist = supp.find('h1', class_='SongHeaderVariantdesktop__Title-sc-12tszai-7').get_text() #leiab laulu artisti
pealkiri = supp.find('h1', class_='SongHeaderVariantdesktop__Title-sc-12tszai-7').get_text() #leiab laulu pealkirja

halvadsõnad = [["cum", "fuck","fucker","fucker's","fuckers'","fuckers","fucking","fuckin","fuckin'","motherfucker","motherfuckers","motherfucker's","motherfuckers'","motherfucking",
"motherfuckin'","fatherfucker","fatherfuckers","bitch","bitches","bitching","bitche's","bitches'","cunt","cunts","twats","twat","wanker","wankers","pussy","pussying","pussies",
"pussy's","pussies'","ass","asses","shit","shitter","shitting","shits","slut","sluts","slutty","sluts'","slut's","dick","dicks","dickhead","dickheads","dickhead's","dickheads'",
"dicking","slag","slags","nigga","niggas","niggas'","nigga's","nigger","niggers","niggers'","nigger's","retard","retarded","retards","retard's","retards'","hooker","hookers",
"hooker's","hookers'","faggot","faggots","faggot's","faggots'","penis","penises","vagina","vaginas","cracker","crackers","tranny","trannies","tranny's","trannies'","cock",
"cocks","coochie","knob","knobs'","shithead","shitheads","sex","porn","porno","blowjob","blowjobs","titjobs","titjob","footjob","footjobs","handjobs","handjob","bullshit",
"bullshitting","bullshitter","bullshitters","asshole","assholes","bastard","bastards","bastard's","bastards'","titties", "nutsack"],
["pede", "persevest", "perse", "lits", "litsakas", "munn", "türa", "kurat","mongol", "neeger", "sitaratas", "vittu","seks","nikk", "porr", "peenis", "tuss", "till", "türapea",
"lõhvard", "debiilik", "debiil", "pederast", "pederastia", "pederastid" , "suuseks" , "jobi" , "hoor" , "lirva" , "lombard" , "sitanikerdis" , "sitane" , "sitt" , "persse" ,
"tissid", "tutt", "värdjas", "taun"], 
["хуй", "Нахуя́", "хуёво", "охуе́нно", "по́хуй", "хуи́ло", "хуеплёт", "хуесо́с", "хуйня́", "не́хуй", "су́ка", "срать", "обосра́ться", "насра́ть", 
"обсира́ть", "просра́ть", "пизда́", "пидора́с", "муда́к", "жо́па", "еба́ть", "еба́шить", "заеба́ть", "Отъеби́сь", "дерьмо́", "блядь", "гандо́н", "дрочи́ть", "залу́па", "ки́ска", "манда́", 
"си́ська", "си́ся", "соса́ть", "ублю́док"]]

#järjendi valimine keele järgi
if keel == 'Eesti keeles': 
    keel = 1
elif keel == 'Inglise keeles':
    keel = 0
else:
    keel = 2

#censorimise funktsioon
def censor(sõnad):
    f = open(artist + " - " + pealkiri + ".txt", encoding="UTF-8", mode="w")
    laused = sõnad.split("\n")
    laused = laused[:-2] #eemaldab 2 viimast rida (share count ja embed)
    for lause in laused:
        lõpptulemus = ""
        lause = lause.split(" ")
        for sõna in lause:
            leitud = False
            if re.sub(r'\W+', '', sõna).lower() in halvadsõnad[keel]: 
                for roppus in halvadsõnad[keel]:
                        if re.sub(r'\W+', '', sõna).lower().startswith(roppus) == True and leitud == False:
                            lõpptulemus += '*' * len(sõna) + ' '
                            leitud = True
            else:
                lõpptulemus += sõna + ' '        
        print(lõpptulemus)
        f.write(lõpptulemus + '\n')
    f.close()

censor(tulemused)
f = open(artist + " - " + pealkiri + ".txt", encoding="UTF-8")
msgbox(title = artist + ' - ' + pealkiri, msg = f.read())