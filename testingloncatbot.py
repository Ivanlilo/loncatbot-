# -*- coding: utf-8 -*-

import LINETCR
from LINETCR.lib.curve.ttypes import *
from datetime import datetime
from gtts import gTTS
import urllib
import urllib2
import urllib3
import requests
import goslate
from bs4 import BeautifulSoup
from datetime import datetime
import subprocess as cmd
import time,random,sys,json,codecs,threading,glob,re,ast,os,subprocess,requests

cl = LINETCR.LINE()
cl.login(qr=True)
#cl.login(token='')
cl.loginResult()

ka = LINETCR.LINE()
ka.login(qr=True)
#ka.login(token='')
ka.loginResult()
print "===[Loncat Bot]==="


helpMessage ="""Menu :
- /creator = view creator bot
- Apakah = kerang ajaib
- Kapan = kerang ajaib
- /check: = get contact
- /info @ = get info contact
- /steal dp @ = get profile
- /steal home @ = get cover
- /pict group = get pict group
- /gcreator = creator group
- /youtube: = get url youtube
- /quote = quote of the day
- /cekig = get info instagram
- /wikipedia = get wikipedia
- /music = get music
- /lyric = get lyric
- /say-id: = text to speech ID
- /say-en: = text to speech EN
- /say-jp: = text to speech JP
- /cek = check tanggal lahir
- /cek server = info server bot
- /siders = check siders
- /cyduc = view siders
- /speed = speed response bot
- /tagall = mention all
- /kalender = view date
- /time = view time
- /gift = send gift
- /gift1 = send gift
- /gift2 = send gift
- /gift3 = send gift
- /about = about of loncatbot
- /bye = loncatbot leave group
"""

mid = cl.getProfile().mid
Creator="Mid Saya"
admin=[""]

contact = cl.getProfile()
profile = cl.getProfile()
profile.displayName = contact.displayName
profile.statusMessage = contact.statusMessage
profile.pictureStatus = contact.pictureStatus

wait = {
    "LeaveRoom":True,
    "AutoJoin":True,
    "Members":0,
    "AutoCancel":False,
    "AutoKick":False,       
    "blacklist":{},
    "wblacklist":False,
    "dblacklist":False,
    "Qr":True,
    "Timeline":True,
    "Contact":True,
    "lang":"JP",
    "BlGroup":{}
}


def sendMessage(to, text, contentMetadata={}, contentType=0):
    mes = Message()
    mes.to, mes.from_ = to, profile.mid
    mes.text = text
    mes.contentType, mes.contentMetadata = contentType, contentMetadata
    if to not in messageReq:
        messageReq[to] = -1
    messageReq[to] += 1

def yt(query):
    with requests.session() as s:
         isi = []
         if query == "":
             query = "S1B tanysyz"   
         s.headers['user-agent'] = 'Mozilla/5.0'
         url    = 'http://www.youtube.com/results'
         params = {'search_query': query}
         r    = s.get(url, params=params)
         soup = BeautifulSoup(r.content, 'html5lib')
         for a in soup.select('.yt-lockup-title > a[title]'):
            if '&list=' not in a['href']:
                if 'watch?v' in a['href']:
                    b = a['href'].replace('watch?v=', '')
                    isi += ['youtu.be' + b]
         return isi

def bot(op):
    try:
#--------------------END_OF_OPERATION--------------------
        if op.type == 0:
            return
#-------------------NOTIFIED_READ_MESSAGE----------------
        if op.type == 55:
	    try:
	      group_id = op.param1
	      user_id=op.param2
	      subprocess.Popen('echo "'+ user_id+'|'+str(op.createdTime)+'" >> dataSeen/%s.txt' % group_id, shell=True, stdout=subprocess.PIPE, )
	    except Exception as e:
	      print e
#------------------NOTIFIED_INVITE_INTO_ROOM-------------
        if op.type == 22:
            cl.leaveRoom(op.param1)
#--------------------INVITE_INTO_ROOM--------------------
        if op.type == 21:
            cl.leaveRoom(op.param1)

#--------------NOTIFIED_INVITE_INTO_GROUP----------------

	    if mid in op.param3:
                if wait["AutoJoin"] == True:
                    cl.acceptGroupInvitation(op.param1)
                    cl.sendText(msg.to,"Terimakasih telah mengundang saya ke group ini :)\nKetik /help untuk mendapatkan bantuan.")
                else:
		    cl.rejectGroupInvitation(op.param1)
	    else:
                if wait["AutoCancel"] == True:
		    if op.param3 in admin:
			pass
		    else:
                        cl.cancelGroupInvitation(op.param1, [op.param3])
		else:
		    if op.param3 in wait["blacklist"]:
			cl.cancelGroupInvitation(op.param1, [op.param3])
			cl.sendText(op.param1, "Itu kicker jgn di invite!")
		    else:
			pass
#------------------NOTIFIED_KICKOUT_FROM_GROUP-----------------
        if op.type == 19:
		if wait["AutoKick"] == True:
                    if op.param2 in admin:
                        pass
                    try:
                        cl.kickoutFromGroup(op.param1,[op.param2])
			cl.inviteIntoGroup(op.param1,[op.param3])
                    except:
                        try:
			    cl.kickoutFromGroup(op.param1,[op.param2])
			    cl.inviteIntoGroup(op.param1,[op.param3])
                        except:
                            print ("client Kick regulation or Because it does not exist in the group\ngid=["+op.param1+"]\nmid=["+op.param2+"]")
                        if op.param2 in wait["blacklist"]:
                            pass
                        else:
			    if op.param2 in admin:
			        pass
			    else:
                                wait["blacklist"][op.param2] = True
                    if op.param2 in wait["blacklist"]:
                        pass
                    else:
		        if op.param2 in admin:
			    pass
		        else:
                            wait["blacklist"][op.param2] = True

#--------------------------NOTIFIED_UPDATE_GROUP---------------------
        if op.type == 11:
            if wait["Qr"] == True:
		if op.param2 in admin:
		    pass
		else:
                    cl.sendText(msg.to, "Jangan mainin QR ntr ada kicker")
            else:
                pass
#--------------------------SEND_MESSAGE---------------------------
        if op.type == 25:
            msg = op.message
#----------------------------------------------------------------------------
            if msg.contentType == 13:
                if wait["wblacklist"] == True:
		    if msg.contentMetadata["mid"] not in admin:
                        if msg.contentMetadata["mid"] in wait["blacklist"]:
                            cl.sendText(msg.to,"already")
                            wait["wblacklist"] = False
                        else:
                            wait["blacklist"][msg.contentMetadata["mid"]] = True
                            wait["wblacklist"] = False
                            cl.sendText(msg.to,"aded")
		    else:
			cl.sendText(msg.to,"Admin Detected~")
			

                elif wait["dblacklist"] == True:
                    if msg.contentMetadata["mid"] in wait["blacklist"]:
                        del wait["blacklist"][msg.contentMetadata["mid"]]
                        cl.sendText(msg.to,"deleted")
                        wait["dblacklist"] = False

                    else:
                        wait["dblacklist"] = False
                        cl.sendText(msg.to,"It is not in the black list")
#--------------------------------------------------------
                elif wait["Contact"] == True:
                     msg.contentType = 0
                     cl.sendText(msg.to,msg.contentMetadata["mid"])
                     if 'displayName' in msg.contentMetadata:
                         contact = cl.getContact(msg.contentMetadata["mid"])
                         try:
                             cu = cl.channel.getCover(msg.contentMetadata["mid"])
                         except:
                             cu = ""
                         cl.sendText(msg.to,"[displayName]:\n" + msg.contentMetadata["displayName"] + "\n\n[mid]:\n" + msg.contentMetadata["mid"] + "\n\n[statusMessage]:\n" + contact.statusMessage + "\n\n[pictureStatus]:\nhttp://dl.profile.line-cdn.net/" + contact.pictureStatus + "\n\n[coverURL]:\n" + str(cu))
                     else:
                         contact = cl.getContact(msg.contentMetadata["mid"])
                         try:
                             cu = cl.channel.getCover(msg.contentMetadata["mid"])
                         except:
                             cu = ""
                         cl.sendText(msg.to,"[displayName]:\n" + contact.displayName + "\n\n[mid]:\n" + msg.contentMetadata["mid"] + "\n\n[statusMessage]:\n" + contact.statusMessage + "\n\n[pictureStatus]:\nhttp://dl.profile.line-cdn.net/" + contact.pictureStatus + "\n\n[coverURL]:\n" + str(cu))


#--------------------------------------------------------
            elif msg.text == "/ginfo":
                if msg.toType == 2:
                    ginfo = cl.getGroup(msg.to)
                    try:
                        gCreator = ginfo.creator.displayName
                    except:
                        gCreator = "Error"
                    if wait["lang"] == "JP":
                        if ginfo.invitee is None:
                            sinvitee = "0"
                        else:
                            sinvitee = str(len(ginfo.invitee))
                        if ginfo.preventJoinByTicket == True:
                            u = "close"
                        else:
                            u = "open"
                        cl.sendText(msg.to,"[Group name]\n" + str(ginfo.name) + "\n\n[Gid]\n" + msg.to + "\n\n[Group creator]\n" + gCreator + "\n\n[Profile status]\nhttp://dl.profile.line.naver.jp/" + ginfo.pictureStatus + "\n\nMembers:" + str(len(ginfo.members)) + "members\nPending:" + sinvitee + "people\nURL:" + u + "it is inside")
                    else:
                        cl.sendText(msg.to,"[group name]\n" + str(ginfo.name) + "\n\n[gid]\n" + msg.to + "\n\n[group creator]\n" + gCreator + "\n\n[profile status]\nhttp://dl.profile.line.naver.jp/" + ginfo.pictureStatus)
                else:
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"Can not be used outside the group")
                    else:
                        cl.sendText(msg.to,"Not for use less than group")
#--------------------------------------------------------
            elif msg.text in ["/bye"]:
                if msg.toType == 2:
                    ginfo = cl.getGroup(msg.to)
                    try:
                        cl.sendText(msg.to,"kakak jahat :(")
                        cl.leaveGroup(msg.to)
                    except:
                        pass
#--------------------------------------------------------
            elif msg.text is None:
                return
#--------------------------------------------------------
            elif msg.text in ["/creator"]:
                msg.contentType = 13
                msg.contentMetadata = {'mid': Creator}
                cl.sendMessage(msg)
		cl.sendText(msg.to,"Itu Yang Bikin Bot")
#--------------------------------------------------------
	    elif msg.text in ["Group creator","Gcreator","gcreator","/gcreator"]:
		ginfo = cl.getGroup(msg.to)
		gCreator = ginfo.creator.mid
                msg.contentType = 13
                msg.contentMetadata = {'mid': gCreator}
                cl.sendMessage(msg)
		cl.sendText(msg.to,"itu yang buat group ini")
#--------------------------------------------------------
            elif msg.contentType == 16:
                if wait["Timeline"] == True:
                    msg.contentType = 0
                    msg.text = "post URL\n" + msg.contentMetadata["postEndUrl"]
                    cl.sendText(msg.to,msg.text)
#--------------------------------------------------------
            elif msg.text in ["Key","help","Help","/help"]:
                cl.sendText(msg.to,helpMessage)
#--------------------------------------------------------
            elif msg.text in ["List group","/list group"]:
                gid = cl.getGroupIdsJoined()
                h = ""
		jml = 0
                for i in gid:
		    gn = cl.getGroup(i).name
                    h += "\(^__^)/『 %s 』\n\n" % (gn)
		    jml += 1
                cl.sendText(msg.to,"======[List Group]======\n"+ h +"\n\nTotal group: "+str(jml))
#--------------------------------------------------------
	    elif "/leave group: " in msg.text:
		ng = msg.text.replace("/leave group: ","")
		gid = cl.getGroupIdsJoined()
                for i in gid:
                    h = cl.getGroup(i).name
		    if h == ng:
			cl.sendText(i,"Bye :( "+h+"~")
		        cl.leaveGroup(i)
			cl.sendText(msg.to,"Success leave ["+ h +"] group")
		    else:
			pass
#--------------------------------------------------------
            elif msg.text in ["/acceptall"]:
                if msg.from_ in admin:
                    gid = cl.getGroupIdsInvited()
                    _list = ""
                    for i in gid:
                        if i is not None:
                            gids = cl.getGroup(i)
                            _list += gids.name
                            cl.acceptGroupInvitation(i)
                        else:
                            break
                    if gid is not None:
                        cl.sendText(msg.to,"Berhasil terima semua undangan dari grup :\n" + _list)
                    else:
                        cl.sendText(msg.to,"Tidak ada grup yang tertunda saat ini")
#--------------------------------------------------------
            elif msg.text in ["/cancel","Cancel"]:
                if msg.toType == 2:
                    X = cl.getGroup(msg.to)
                    if X.invitee is not None:
                        gInviMids = [contact.mid for contact in X.invitee]
                        cl.cancelGroupInvitation(msg.to, gInviMids)
                    else:
                        cl.sendText(msg.to,"No one is inviting")
                else:
                    Cl.sendText(msg.to,"Can not be used outside the group")
#--------------------------------------------------------
            elif msg.text in ["/ourl","Url:on"]:
                if msg.toType == 2:
                    X = cl.getGroup(msg.to)
                    X.preventJoinByTicket = False
                    cl.updateGroup(X)
                    cl.sendText(msg.to,"Url Active")
                else:
                    cl.sendText(msg.to,"Can not be used outside the group")
#--------------------------------------------------------
            elif msg.text in ["/curl","Url:off"]:
                if msg.toType == 2:
                    X = cl.getGroup(msg.to)
                    X.preventJoinByTicket = True
                    cl.updateGroup(X)
                    cl.sendText(msg.to,"Url inActive")

                else:
                    cl.sendText(msg.to,"Can not be used outside the group")
#--------------------------------------------------------
            elif msg.text in ["/join on","Autojoin:on"]:
                wait["AutoJoin"] = True
                cl.sendText(msg.to,"AutoJoin Active")

            elif msg.text in ["/join off","Autojoin:off"]:
                wait["AutoJoin"] = False
                cl.sendText(msg.to,"AutoJoin inActive")

#--------------------------------------------------------
	    elif msg.text in ["Autocancel:on"]:
                wait["AutoCancel"] = True
                cl.sendText(msg.to,"The group of people and below decided to automatically refuse invitation")
		print wait["AutoCancel"][msg.to]

	    elif msg.text in ["Autocancel:off"]:
                wait["AutoCancel"] = False
                cl.sendText(msg.to,"Invitation refused turned off")
		print wait["AutoCancel"][msg.to]
#--------------------------------------------------------
	    elif "Qr:on" in msg.text:
	        wait["Qr"] = True
	    	cl.sendText(msg.to,"QR Protect Active")

	    elif "Qr:off" in msg.text:
	    	wait["Qr"] = False
	    	cl.sendText(msg.to,"Qr Protect inActive")
#--------------------------------------------------------
	    elif "Autokick:on" in msg.text:
		wait["AutoKick"] = True
		cl.sendText(msg.to,"AutoKick Active")

	    elif "Autokick:off" in msg.text:
		wait["AutoKick"] = False
		cl.sendText(msg.to,"AutoKick inActive")
#--------------------------------------------------------
#pake tag

            elif "/info @" in msg.text:
                nama = msg.text.replace("/info @","")
                target = nama.rstrip(' ')
                van = cl.getGroup(msg.to)
                for linedev in van.members:
                    if target == linedev.displayName:
                        mid = cl.getContact(linedev.mid)
                        # @riorenata_ix #
                        try:
                            cover = cl.channel.getCover(linedev.mid)
                        except:
                            cover = ""
                        cl.sendText(msg.to,"[Display Name]:\n" + mid.displayName + "\n\n[Mid]:\n" + linedev.mid + "\n\n[Bio]:\n" + mid.statusMessage + "\n\n[Foto Profile]:\nhttp://dl.profile.line-cdn.net/" + mid.pictureStatus + "\n\n[Cover]:\n" + str(cover))
                    else:
                        pass

#pake mid

            elif "/info: " in msg.text:
                mid = msg.text.replace("/info: ","")
                anu = cl.getContact(mid)
                try:
                    cover = cl.channel.getCover(mid)
                except:
                    cover = ""
                cl.sendText(msg.to,"[Display Name]:\n" + anu.displayName + "\n\n[Mid]:\n" + mid + "\n\n[Bio]:\n" + anu.statusMessage + "\n\n[Foto Profile]:\nhttp://dl.profile.line-cdn.net/" + anu.pictureStatus + "\n\n[Cover]:\n" + str(cover))
#--------------------------------------------------------
            elif "/send message to: " in msg.text:
                if msg.from_ in admin:
                    cond = msg.text.split(" ")
                    target = int(cond[1])
                    text = msg.text.replace("/send message to: " + str(target) + "\n/Message: ","")
                    try:
                        cl.findAndAddContactsByMid(target)
                        cl.sendText(target,"Saya membawakan pesan dari presiden untuk anda yang berisi: \"" + text + "\"")
                        cl.sendText(msg.to,"Berhasil mengirim pesan")
                    except:
                        cl.sendText(msg.to,"Gagal mengirim pesan, mungkin midnya salah")
#---------------------------------------------------------
#Fitur random qoute
            elif msg.text in ["Quote","quote","quotes","Quotes","/quote"]:
                quote = ['Barangsiapa yang suka meninggalkan barang di tempat umum maka ia akan kehilangan barangnya tersebut','Kunci KESUKSESAN itu cuma satu, yakni lu harus BERHASIL']
                psn = random.choice(quote)
                cl.sendText(msg.to,psn)
#---------------------------------------------------------
            elif msg.text in ["/time","/waktu"]:
                timeNow = datetime.now()
                timeHours = datetime.strftime(timeNow,"(%H:%M)")
                day = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday","Friday", "Saturday"]
                hari = ["Minggu", "Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]
                bulan = ["Januari", "Februari", "Maret", "April", "Mei", "Juni", "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
                inihari = datetime.today()
                hr = inihari.strftime('%A')
                bln = inihari.strftime('%m')
                for i in range(len(day)):
                    if hr == day[i]: hasil = hari[i]
                for k in range(0, len(bulan)):
                    if bln == str(k): blan = bulan[k-1]
                rst = hasil + ", " + inihari.strftime('%d') + " - " + blan + " - " + inihari.strftime('%Y') + "\nJam : [ " + inihari.strftime('%H:%M:%S') + " ]"
                cl.sendText(msg.to, rst)
#---------------------------------------------------------
               elif "/pict group" in msg.text:
                   group = cl.getGroup(msg.to)
                   path ="http://dl.profile.line-cdn.net/" + group.pictureStatus)
                   cl.sendImageWithURL(msg.to, path)
#---------------------------------------------------------
#---------------------------------------------------------
            elif "/steal home @" in msg.text:
                   print "[Command]COVER executing"
                   _name = msg.text.replace("/steal home @","")
                   _nametarget = _name.rstrip(' ')
                   gs = cl.getGroup(msg.to)
                   targets = []
                   for g in gs.members:
                       if _nametarget == g.displayName:
                           targets.append(g.mid)
                   if targets == []:
                       cl.sendText(msg.to,"Contact not found")
                   else:
                       for target in targets:
                           try:
                               contact = cl.getContact(target)
                               cu = cl.channel.getCover(target)
                               path = str(cu)
                               cl.sendImageWithURL(msg.to, path)
                           except:
                               pass
                   print "[Command]COVER executed"
                   
            elif "/steal dp @" in msg.text:            
                   print "[Command]DP executing"
                   _name = msg.text.replace("/steal dp @","")
                   _nametarget = _name.rstrip('  ')
                   gs = cl.getGroup(msg.to)
                   targets = []
                   for g in gs.members:
                       if _nametarget == g.displayName:
                           targets.append(g.mid)
                   if targets == []:
                       cl.sendText(msg.to,"Contact not found")
                   else:
                       for target in targets:
                           try:
                               contact = cl.getContact(target)
                               path = "http://dl.profile.line-cdn.net/" + contact.pictureStatus
                               cl.sendImageWithURL(msg.to, path)
                           except:
                               print "[Command]DP executed"
#---------------------------------------------------------
            elif msg.text in ["Kernel","kernel","/kernel"]:
                 if msg.from_ in admin:
                     botKernel = subprocess.Popen(["uname","-svmo"], stdout=subprocess.PIPE).communicate()[0]
                     cl.sendText(msg.to, botKernel)
                     print "[Command]Kernel executed"
                 else:
                     cl.sendText(msg.to,"Command denied.")
                     cl.sendText(msg.to,"Admin permission required.")
                     print "[Error]Command denied - Admin permission required"
#---------------------------------------------------------
              elif msg.text in ["/kalender"]:
	    	      wait2['setTime'][msg.to] = datetime.today().strftime('TANGGAL : %Y-%m-%d \nHARI : %A \nJAM : %H:%M:%S')
	              cl.sendText(msg.to, "KALENDER\n\n" + (wait2['setTime'][msg.to]))
#---------------------------------------------------------
            elif msg.text in ["/cek"]:
            	cl.sendText(msg.to,"contoh : /cek 16-05-2004")
#---------------------------------------------------------
            elif msg.text in ["/about"]:
            	cl.sendText(msg.to,"About :\n\nBot ini dibuat oleh Rio Renata\n\nJika anda menemukan bug di bot ini, silakan screenshot dan kirim ke id line di bawah ini.\nline.me/ti/p/~imrra\n\n\n© I MADE RIO RENATA | 2017")
#---------------------------------------------------------
#Spam by mid

            elif "/spam " in msg.text:
                korban = msg.text.replace("/spam ","")
                korban2 = korban.split()
                midd = korban2[0]
                jumlah = int(korban2[1])
                if jumlah <= 1000:
                    for var in range(0,jumlah):
                        cl.sendText(midd,"Cie yang kena spam😂😂")
                else:
                    cl.sendText(msg.to, "Kebanyakan anjir! ")
                print "Spam Contact"

#cara make : /spam midtarget jumlah : /spam MID 10
#klo ga work coba add dlu targetnya

            elif "/add " in msg.text:
                target = msg.text.replace("/add ","")
                cl.findAndAddContactsByMid(target)
                cl.sendText(msg.to, "Menambahkan : " +cl.getContact(target).displayName+ " sebagai teman Berhasil!!")
                print "Add user"
#--------------------------------------------------------------------------------------
          elif '/music ' in msg.text.lower():
                try:
                    songname = msg.text.lower().replace('/music ','')
                    params = {'songname': songname}
                    r = requests.get('http://ide.fdlrcn.com/workspace/yumi-apis/joox?' + urllib.urlencode(params))
                    data = r.text
                    data = json.loads(data)
                    for song in data:
                        hasil = 'This is Your Music\n'
                        hasil += 'Judul : ' + song[0]
                        hasil += '\nDurasi : ' + song[1]
                        hasil += '\nLink Download : ' + song[4]
                        cl.sendText(msg.to, hasil)
                        cl.sendText(msg.to, "Please Wait for audio...")
                        cl.sendAudioWithURL(msg.to, song[4])
		except Exception as njer:
		        cl.sendText(msg.to, str(njer))
#--------------------------------- TRANSLATE --------------------------------
            elif "/en " in msg.text:
                txt = msg.text.replace("/en ","")
                try:
                    gs = goslate.Goslate()
                    trs = gs.translate(txt,'en')
                    cl.sendText(msg.to,trs)
                    print '[Command] Translate EN'
            except Exception as njer:
		        cl.sendText(msg.to, str(njer))

            elif "/id " in msg.text:
                txt = msg.text.replace("/id ","")
                try:
                    gs = goslate.Goslate()
                    trs = gs.translate(txt,'en')
                    cl.sendText(msg.to,trs)
                    print '[Command] Translate ID'
            except Exception as njer:
		        cl.sendText(msg.to, str(njer))
#----------------------------------------------------------------------------
             elif "/broadcast " in msg.text:
                  imade = msg.text.replace("/broadcast ", "") 
                  rio = cl.getAllContactIds()
                  for renata in rio:
                       cl.sendText(renata, (imade))
#----------------------------------------------------------------------------
             elif "/ig " in msg.text:
                 print "[Command] IG executing"
                 stalkID = msg.text.replace("/ig ","")
                 subprocess.call(["instaLooter",stalkID,"tmp/","-n","1"])   
                 files = glob.glob("tmp/*.jpg")
                 for file in files:
                     os.rename(file,"tmp/tmp.jpg")
                 fileTmp = glob.glob("tmp/tmp.jpg")
                 if not fileTmp:
                     cl.sendText(msg.to, "Image not found, maybe the account haven't post a single picture or the account is private")
                     print "[Command]IG,executed - no image found"
                 else:
                     image = upload_tempimage(client)
                     cl.sendText(msg.to, format(image['link']))
                     subprocess.call(["sudo","rm","-rf","tmp/tmp.jpg"])
                     print "[Command]Stalk executed - succes"   
#=============== CEK SPEK SRV =============
       elif "/cek server" in msg.text:
           a="lscpu | grep -i 'model name'|awk -F : '{print $2}'"
           b="lscpu | grep -i 'architecture' | awk -F : '{print $2}'"
           c="cat /etc/redhat-release"
           d="lsblk | awk '{print $4}' | head -2 | tail -1"
           e="free -lm | awk '{print $2}'| head -2|tail -1"
           g="lscpu | grep -i 'virtualization' | awk -F : '{print $2}'"
           h="lscpu | grep -i 'CPU op-mode' | awk -F : '{print $2}'"
           cmdlis = [a,b,c,d,e,g,h]
           rio = "Server\n\n"
           for i in cmdlis:
                c=cmd.getoutput(i)
                rio += c.strip()+"\n"
           cl.sendMessage(msg.to, rio)
#---------------------------------------------------------
            elif "/cek " in msg.text:
                tanggal = msg.text.replace("/cek ","")
                r=requests.get('https://script.google.com/macros/exec?service=AKfycbw7gKzP-WYV2F5mc9RaR7yE3Ve1yN91Tjs91hp_jHSE02dSv9w&nama=ervan&tanggal='+tanggal)
                data=r.text
                data=json.loads(data)
                lahir = data["data"]["lahir"]
                usia = data["data"]["usia"]
                ultah = data["data"]["ultah"]
                zodiak = data["data"]["zodiak"]
                cl.sendText(msg.to,"Tanggal Lahir : "+lahir+"\n\nUmur : "+usia+"\n\nUltah : "+ultah+"\n\nZodiak : "+zodiak)
#---------------------------------------------------------
            elif '/wikipedia ' in msg.text.lower():
                  try:
                      wiki = msg.text.lower().replace("/wikipedia ","")
                      wikipedia.set_lang("id")
                      pesan="Wikipedia : "
                      pesan+=wikipedia.page(wiki).title
                      pesan+="\n\n"
                      pesan+=wikipedia.summary(wiki, sentences=1)
                      pesan+="\n"
                      pesan+=wikipedia.page(wiki).url
                      cl.sendText(msg.to, pesan)
                  except:
                          try:
                              pesan="Text Terlalu Panjang Silahkan Click link di bawah ini\n"
                              pesan+=wikipedia.page(wiki).url
                              cl.sendText(msg.to, pesan)
                          except Exception as e:
                              cl.sendText(msg.to, str(e))
#============ TTS ==============#
            elif "/say " in msg.text.lower():
              if msg.from_ in owner:
                    query = msg.text.lower().replace("/say ","")
                    with requests.session() as s:
                        s.headers['user-agent'] = 'Mozilla/5.0'
                        url    = 'https://google-translate-proxy.herokuapp.com/api/tts'
                        params = {
                                    'language': 'id',
                                    'speed': '1',
                                    'query': query
                                    }
                        r    = s.get(url, params=params)
                        mp3  = r.url
                        ka.sendAudioWithURL(msg.to, mp3)
#---------------------------------------------------------
        elif "/say-id: " in msg.text:
            query = msg.text.replace("/say-id: ","")
            with requests.session() as s:
                s.headers['user-agent'] = 'Mozilla/5.0'
                url    = 'https://google-translate-proxy.herokuapp.com/api/tts'
                params = {
                            'language': 'id',
                            'speed': '1',
                            'query': query
                            }
                r    = s.get(url, params=params)
                mp3  = r.url
                cl.sendAudioWithURL(msg.to, mp3)
#---------------------------------------------------------
        elif "/say-en: " in msg.text:
            query = msg.text.replace("/say-en: ","")
            with requests.session() as s:
                s.headers['user-agent'] = 'Mozilla/5.0'
                url    = 'https://google-translate-proxy.herokuapp.com/api/tts'
                params = {
                            'language': 'en',
                            'speed': '1',
                            'query': query
                            }
                r    = s.get(url, params=params)
                mp3  = r.url
                cl.sendAudioWithURL(msg.to, mp3)
#---------------------------------------------------------
        elif "/say-jp: " in msg.text:
            query = msg.text.replace("/say-jp: ","")
            with requests.session() as s:
                s.headers['user-agent'] = 'Mozilla/5.0'
                url    = 'https://google-translate-proxy.herokuapp.com/api/tts'
                params = {
                            'language': 'ja',
                            'speed': '1',
                            'query': query
                            }
                r    = s.get(url, params=params)
                mp3  = r.url
                cl.sendAudioWithURL(msg.to, mp3)
#---------------------------------------------------------
            elif '/cekig ' in msg.text.lower():
                try:
                    instagram = msg.text.lower().replace("/cekig ","")
                    html = requests.get('https://www.instagram.com/' + instagram + '/?')
                    soup = BeautifulSoup(html.text, 'html5lib')
                    data = soup.find_all('meta', attrs={'property':'og:description'})
                    text = data[0].get('content').split()
                    data1 = soup.find_all('meta', attrs={'property':'og:image'})
                    text1 = data1[0].get('content').split()
                    user = "Nama: " + text[-2] + "\n"
                    user1 = text[-1]
                    followers = "Pengikut: " + text[0] + "\n"
                    following = "Mengikuti: " + text[2] + "\n"
                    post = "Post: " + text[4] + "\n"
                    link = "Link: " + "https://www.instagram.com/" + instagram
                    detail = "Info Akun: " + user1 + "\n\n"
                    details = " "
                    cl.sendText(msg.to, detail + user + followers + following + post + link + details)
                    cl.sendImageWithURL(msg.to, text1[0])
                except Exception as njer:
                	cl.sendText(msg.to, str(njer))
#---------------------------------------------------------
            elif "/youtube:" in msg.text.lower():
                   query = msg.text.split(":")
                   try:
                       if len(query) == 3:
                           isi = yt(query[2])
                           hasil = isi[int(query[1])-1]
                           cl.sendText(msg.to, hasil)
                       else:
                           isi = yt(query[1])
                           cl.sendText(msg.to, isi[0])
                   except Exception as e:
                       cl.sendText(msg.to, str(e))
#---------------------------------------------------------
            elif '/lyric ' in msg.text.lower():
                try:
                    songname = msg.text.lower().replace('/lyric ','')
                    params = {'songname': songname}
                    r = requests.get('http://ide.fdlrcn.com/workspace/yumi-apis/joox?' + urllib.urlencode(params))
                    data = r.text
                    data = json.loads(data)
                    for song in data:
                        hasil = 'Lyric Lagu : '
                        hasil += song[0]
                        hasil += '\n\n'
                        hasil += song[5]
                        cl.sendText(msg.to, hasil)
                except Exception as wak:
                        cl.sendText(msg.to, str(wak))
#---------------------------------------------------------
            elif "Apakah " in msg.text:
                  tanya = msg.text.replace("Apakah ","")
                  jawab = ("iya","Tidak","mungkin","bisa jadi")
                  jawaban = random.choice(jawab)
                  tts = gTTS(text=jawaban, lang='id')
                  tts.save('tts.mp3')
                  cl.sendAudio(msg.to,'tts.mp3')
                  
            elif "Kapan " in msg.text:
                  tanya = msg.text.replace("Kapan ","")
                  jawab = ("kapan  kapan","besok","satu  abad  lagi")
                  jawaban = random.choice(jawab)
                  tts = gTTS(text=jawaban, lang='id')
                  tts.save('tts.mp3')
                  cl.sendAudio(msg.to,'tts.mp3')
#---------------------------------------------------------
            elif "/dosa " in msg.text:
                tanya = msg.text.replace("/dosa ","")
                jawab = ("Tidak ada","10%","20%","30%","40%","50%","60%","70%","80%","90%","100%","Tak terhingga")
                jawaban = random.choice(jawab)
                cl.sendText(msg.to,"Dosanya " + tanya + " adalah " + jawaban + " Banyak banyak tobat tong ")
#---------------------------------------------------------
#-----------Show contact dari mid----------#
            elif "/check:" in msg.text:
                midd = msg.text.replace("/check:","")
                msg.contentType = 13
                msg.contentMetadata = {"mid":midd}
                cl.sendMessage(msg)
#--------------------------------------------------------
            elif msg.text in ["/k on","Contact:on"]:
                wait["Contact"] = True
                cl.sendText(msg.to,"Contact Active")

            elif msg.text in ["/k off","Contact:off"]:
                wait["Contact"] = False
                cl.sendText(msg.to,"Contact inActive")
#--------------------------------------------------------
            elif msg.text in ["Status","Setting","/status"]:
                md = ""
		if wait["AutoJoin"] == True: md+="✦ Auto join : on\n"
                else: md +="✦ Auto join : off\n"
		if wait["Contact"] == True: md+="✦ Info Contact : on\n"
		else: md+="✦ Info Contact : off\n"
                if wait["AutoCancel"] == True:md+="✦ Auto cancel : on\n"
                else: md+= "✦ Auto cancel : off\n"
		if wait["Qr"] == True: md+="✦ Qr Protect : on\n"
		else:md+="✦ Qr Protect : off\n"
		if wait["AutoKick"] == True: md+="✦ Autokick : on\n"
		else:md+="✦ Autokick : off"
                cl.sendText(msg.to,"=====[Status]=====\n"+md)
#--------------------------------------------------------
            elif msg.text in ["Gift","gift","/gift"]:
                msg.contentType = 9
                msg.contentMetadata={'PRDID': 'a0768339-c2d3-4189-9653-2909e9bb6f58',
                                    'PRDTYPE': 'THEME',
                                    'MSGTPL': '5'}
                msg.text = None
                cl.sendMessage(msg)


            elif msg.text in ["/gift1"]:
                msg.contentType = 9
                msg.contentMetadata={'PRDID': '696d7046-843b-4ed0-8aac-3113ed6c0733',
                                    'PRDTYPE': 'THEME',
                                    'MSGTPL': '6'}
                msg.text = None
                cl.sendMessage(msg)

            elif msg.text in ["/gift2"]:
                msg.contentType = 9
                msg.contentMetadata={'PRDID': '8fe8cdab-96f3-4f84-95f1-6d731f0e273e',
                                    'PRDTYPE': 'THEME',
                                    'MSGTPL': '7'}
                msg.text = None
                cl.sendMessage(msg)

            elif msg.text in ["/gift3"]:
                msg.contentType = 9
                msg.contentMetadata={'PRDID': 'ae3d9165-fab2-4e70-859b-c14a9d4137c4',
                                    'PRDTYPE': 'THEME',
                                    'MSGTPL': '8'}
                msg.text = None
                cl.sendMessage(msg)

#--------------------------------------------------------
	    elif "/tagall" == msg.text:
		group = cl.getGroup(msg.to)
		mem = [contact.mid for contact in group.members]
		for mm in mem:
		    xname = cl.getContact(mm).displayName
		    xlen = str(len(xname)+1)
		    msg.contentType = 0
		    msg.text = "Woy siapa aja yang on?"
		    msg.text = "@"+xname+" "
		    msg.contentMetadata = {'MENTION':'{"MENTIONEES":[{"S":"0","E":'+json.dumps(xlen)+',"M":'+json.dumps(mm)+'}]}','EMTVER':'4'}
		    try:
		        cl.sendMessage(msg)
		    except Exception as e:
			print str(e)

#--------------------------CEK SIDER------------------------------
            elif "/siders" in msg.text:
                subprocess.Popen("echo '' > dataSeen/"+msg.to+".txt", shell=True, stdout=subprocess.PIPE)
                cl.sendText(msg.to, "melihat siders...\nketik /cyduc untuk mencyducnya!")
                print "setview"

            elif "/cyduc" in msg.text:
	        lurkGroup = ""
	        dataResult, timeSeen, contacts, userList, timelist, recheckData = [], [], [], [], [], []
                with open('dataSeen/'+msg.to+'.txt','r') as rr:
                    contactArr = rr.readlines()
                    for v in xrange(len(contactArr) -1,0,-1):
                        num = re.sub(r'\n', "", contactArr[v])
                        contacts.append(num)
                        pass
                    contacts = list(set(contacts))
                    for z in range(len(contacts)):
                        arg = contacts[z].split('|')
                        userList.append(arg[0])
                        timelist.append(arg[1])
                    uL = list(set(userList))
                    for ll in range(len(uL)):
                        try:
                            getIndexUser = userList.index(uL[ll])
                            timeSeen.append(time.strftime("%H:%M:%S", time.localtime(int(timelist[getIndexUser]) / 1000)))
                            recheckData.append(userList[getIndexUser])
                        except IndexError:
                            conName.append('nones')
                            pass
                    contactId = cl.getContacts(recheckData)
                    for v in range(len(recheckData)):
                        dataResult.append(contactId[v].displayName + ' ('+timeSeen[v]+')')
                        pass
                    if len(dataResult) > 0:
                        tukang = "T E R C Y D U C\n*"
                        grp = '\n* '.join(str(f) for f in dataResult)
                        total = '\n\nTotal %i siders (%s)' % (len(dataResult), datetime.now().strftime('%H:%M:%S') )
                        cl.sendText(msg.to, "%s %s %s" % (tukang, grp, total))
                    else:
                        cl.sendText(msg.to, "Belum ada siders")
                    print "viewseen"
#--------------------------------------------------------

#KICK_BY_TAG
	    elif "/usir " in msg.text:
		if 'MENTION' in msg.contentMetadata.keys()!= None:
		    names = re.findall(r'@(\w+)', msg.text)
		    mention = ast.literal_eval(msg.contentMetadata['MENTION'])
		    mentionees = mention['MENTIONEES']
		    print mentionees
		    for mention in mentionees:
			cl.kickoutFromGroup(msg.to,[mention['M']])

#--------------------------------------------------------
	    elif "/add all" in msg.text:
		thisgroup = cl.getGroups([msg.to])
		Mids = [contact.mid for contact in thisgroup[0].members]
		mi_d = Mids[:33]
		cl.findAndAddContactsByMids(mi_d)
		cl.sendText(msg.to,"Success Add all")
#--------------------------------------------------------
	    elif "/recover" in msg.text:
		thisgroup = cl.getGroups([msg.to])
		Mids = [contact.mid for contact in thisgroup[0].members]
		mi_d = Mids[:33]
		cl.createGroup("Recover", mi_d)
		cl.sendText(msg.to,"Success recover")
#--------------------------------------------------------
	    elif msg.text in ["Remove all chat","/hapus semua chat"]:
		cl.removeAllMessages(op.param2)
		cl.sendText(msg.to,"Removed all chat")
#--------------------------------------------------------
            elif ("Gn: " in msg.text):
                if msg.toType == 2:
                    X = cl.getGroup(msg.to)
                    X.name = msg.text.replace("Gn: ","")
                    cl.updateGroup(X)
                else:
                    cl.sendText(msg.to,"It can't be used besides the group.")
#--------------------------------------------------------
            elif "/kick: " in msg.text:
                midd = msg.text.replace("/kick: ","")
		if midd not in admin:
		    cl.kickoutFromGroup(msg.to,[midd])
		else:
		    cl.sendText(msg.to,"Admin Detected")
#--------------------------------------------------------
            elif "/invite: " in msg.text:
                midd = msg.text.replace("/invite: ","")
                cl.findAndAddContactsByMid(midd)
                cl.inviteIntoGroup(msg.to,[midd])
#--------------------------------------------------------
            elif msg.text in ["#welcome","Welcome","welcome","Welkam","welkam"]:
                gs = cl.getGroup(msg.to)
                cl.sendText(msg.to,"Selamat datang di "+ gs.name)
                cl.sendText(msg.to,"Semoga betah yaa kak 😘😘")
                cl.sendText(msg.to,"Jangan jadi kicker \(>_<)/")
#--------------------------------------------------------
	    elif "Bc: " in msg.text:
		bc = msg.text.replace("Bc: ","")
		gid = cl.getGroupIdsJoined()
		for i in gid:
		    cl.sendText(i,"=======[BROADCAST]=======\n\n"+bc+"\n\nContact Me : line.me/ti/p/~imrra")
		cl.sendText(msg.to,"Success BC BosQ")
#--------------------------------------------------------
            elif msg.text in ["/cancelall","Cancelall"]:
                gid = cl.getGroupIdsInvited()
                for i in gid:
                    cl.rejectGroupInvitation(i)
                cl.sendText(msg.to,"All invitations have been refused")
#--------------------------------------------------------
            elif msg.text in ["/gurl"]:
                if msg.toType == 2:
                    x = cl.getGroup(msg.to)
                    if x.preventJoinByTicket == True:
                        x.preventJoinByTicket = False
                        cl.updateGroup(x)
                    gurl = cl.reissueGroupTicket(msg.to)
                    cl.sendText(msg.to,"line://ti/g/" + gurl)
                else:
                    if wait["lang"] == "JP":
                        cl.sendText(msg.to,"Can't be used outside the group")
                    else:
                        cl.sendText(msg.to,"Not for use less than group")
#--------------------------------------------------------
	    elif msg.text in ["Self Like","/self like"]:
		try:
		    print "activity"
		    url = cl.activity(limit=1)
		    print url
		    cl.like(url['result']['posts'][0]['userInfo']['mid'], url['result']['posts'][0]['postInfo']['postId'], likeType=1001)
		    cl.comment(url['result']['posts'][0]['userInfo']['mid'], url['result']['posts'][0]['postInfo']['postId'], "Auto like by : \nine.me/ti/p/~imrra")
		    cl.sendText(msg.to, "Success~")
		except Exception as E:
		    try:
			cl.sendText(msg.to,str(E))
		    except:
			pass

#--------------------------------------------------------
            elif msg.text in ["Sp","Speed","speed","/speed"]:
                start = time.time()
		print("Speed")
                elapsed_time = time.time() - start
		cl.sendText(msg.to, "Testing speed response ...")
                cl.sendText(msg.to, "Speed response : %s second" % (elapsed_time))

#--------------------------------------------------------
            elif msg.text in ["/ban"]:
                wait["wblacklist"] = True
                cl.sendText(msg.to,"send contact")

            elif msg.text in ["/unban"]:
                wait["dblacklist"] = True
                cl.sendText(msg.to,"send contact")
#--------------------------------------------------------
	    elif "/backup" in msg.text:
		try:
		    cl.updateDisplayPicture(profile.pictureStatus)
		    cl.updateProfile(profile)
		    cl.sendText(msg.to, "Success backup profile")
		except Exception as e:
		    cl.sendText(msg.to, str(e))
#--------------------------------------------------------
	    elif "/copy " in msg.text:
                copy0 = msg.text.replace("/copy ","")
                copy1 = copy0.lstrip()
                copy2 = copy1.replace("@","")
                copy3 = copy2.rstrip()
                _name = copy3
		group = cl.getGroup(msg.to)
		for contact in group.members:
		    cname = cl.getContact(contact.mid).displayName
		    if cname == _name:
			cl.CloneContactProfile(contact.mid)
			cl.sendText(msg.to, "Success~")
		    else:
			pass
		
#--------------------------------------------------------
            elif "/ban @" in msg.text:
                if msg.toType == 2:
                    print "Ban by mention"
                    _name = msg.text.replace("/ban @","")
                    _nametarget = _name.rstrip('  ')
                    gs = cl.getGroup(msg.to)
                    targets = []
                    for g in gs.members:
                        if _nametarget == g.displayName:
                            targets.append(g.mid)
                    if targets == []:
                        cl.sendText(msg.to,"Not found")
                    else:
                        for target in targets:
			    if target not in admin:
                                try:
                                    wait["blacklist"][target] = True
                                    f=codecs.open('st2__b.json','w','utf-8')
                                    json.dump(wait["blacklist"], f, sort_keys=True, indent=4,ensure_ascii=False)
                                    cl.sendText(msg.to,"Succes BosQ")
                                except:
                                    cl.sendText(msg.to,"Error")
			    else:
				cl.sendText(msg.to,"Admin Detected~")
#--------------------------------------------------------
            elif msg.text in ["/banlist"]:
                if wait["blacklist"] == {}:
                    cl.sendText(msg.to,"tidak ada")
                else:
                    mc = ""
                    for mi_d in wait["blacklist"]:
                        mc += "->" +cl.getContact(mi_d).displayName + "\n"
                    cl.sendText(msg.to,"===[Blacklist User]===\n"+mc)

#--------------------------------------------------------
            elif "/unban @" in msg.text:
                if msg.toType == 2:
                    print "Unban by mention"
                    _name = msg.text.replace("/unban @","")
                    _nametarget = _name.rstrip('  ')
                    gs = cl.getGroup(msg.to)
                    targets = []
                    for g in gs.members:
                        if _nametarget == g.displayName:
                            targets.append(g.mid)
                    if targets == []:
                        cl.sendText(msg.to,"Not found")
                    else:
                        for target in targets:
                            try:
                                del wait["blacklist"][target]
                                f=codecs.open('st2__b.json','w','utf-8')
                                json.dump(wait["blacklist"], f, sort_keys=True, indent=4,ensure_ascii=False)
                                cl.sendText(msg.to,"Succes BosQ")
                            except:
                                cl.sendText(msg.to,"Succes BosQ")
#--------------------------------------------------------
            elif msg.text in ["/kill ban"]:
                if msg.toType == 2:
                    group = cl.getGroup(msg.to)
                    gMembMids = [contact.mid for contact in group.members]
                    matched_list = []
                    for tag in wait["blacklist"]:
                        matched_list+=filter(lambda str: str == tag, gMembMids)
                    if matched_list == []:
                        cl.sendText(msg.to,"There was no blacklist user")
                        return
                    for jj in matched_list:
                        cl.kickoutFromGroup(msg.to,[jj])
                    cl.sendText(msg.to,"Blacklist emang pantas tuk di usir")
#--------------------------------------------------------
            elif "ばんたい" in msg.text:
                if msg.toType == 2:
                    print "Kick all member"
                    _name = msg.text.replace("ばんたい","")
                    gs = cl.getGroup(msg.to)
                    cl.sendText(msg.to,"Dadaaah~")
                    targets = []
                    for g in gs.members:
                        if _name in g.displayName:
                            targets.append(g.mid)
                    if targets == []:
                        cl.sendText(msg.to,"Not found.")
                    else:
                        for target in targets:
			     if target not in admin:
                                try:
                                    cl.kickoutFromGroup(msg.to,[target])
                                    print (msg.to,[g.mid])
                                except Exception as e:
                                    cl.sendText(msg.to,str(e))
			 cl.inviteIntoGroup(msg.to, targets)
#--------------------------------------------------------
#Restart_Program
	    elif msg.text in ["Bot:restart"]:
		cl.sendText(msg.to, "Bot has been restarted")
		restart_program()
		print "Restart"
#--------------------------------------------------------



        if op.type == 59:
            print op


    except Exception as error:
        print error


#thread2 = threading.Thread(target=nameUpdate)
#thread2.daemon = True
#thread2.start()

while True:
    try:
        Ops = cl.fetchOps(cl.Poll.rev, 5)
    except EOFError:
        raise Exception("It might be wrong revision\n" + str(cl.Poll.rev))

    for Op in Ops:
        if (Op.type != OpType.END_OF_OPERATION):
            cl.Poll.rev = max(cl.Poll.rev, Op.revision)
            bot(Op)

