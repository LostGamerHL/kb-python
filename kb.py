#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests, json, random, untangle, time, subprocess, sys, os
from datetime import timedelta
from threading import Thread
from html import unescape
import vkapi

#Файлы системы бота
kb_name = json.loads(open('system/info','r').read())['names']
kb_cmd = json.loads(open('system/cmds','r').read())
users = json.loads(open('system/users','r').read())

def evalcmds(filename,toho,torep,answ_text):
	exec(open(filename,'r').read())

longpoll = vkapi.GetLongPollServer()
print('Лонгполл получен:  '+str(longpoll))
while True:
	try:
		listen = vkapi.ListenLongPollServer( longpoll )
		result = listen['result']
		if result:
			toho = result[3]
			torep = result[1]
			if (result[3] < 2000000000):
				userid = result[3]
			else:
				userid = result[6]['from']
			answ = result[5].split(' ')
			answ[0] = answ[0].lower()
			if len(answ) > 1:
				answ[1] = answ[1].lower()
			if len(answ) > 1 and str(userid) not in users['blacklist'] and answ[0] in kb_name and (answ[1] in kb_cmd["default"] or answ[1] in kb_cmd["vip"] or answ[1] in kb_cmd["admin"]):
				print('[Упоминание кб в '+str(toho)+']')
				answ_text = result[5].split(' ')
				if len(answ_text) > 2:
					del answ_text[0:2]
					answ_text = ' '.join(answ_text)
					answ_text = unescape(answ_text)
				else:
					answ_text = 0

				if answ[1] in kb_cmd['default']:
					Thread(target=evalcmds,args=('plugins/default/'+kb_cmd['default'][answ[1]],toho,torep,answ_text)).start()
				elif answ[1] in kb_cmd['vip'] and str(userid) in users['vip']:
					Thread(target=evalcmds,args=('plugins/vip/'+kb_cmd['vip'][answ[1]],toho,torep,answ_text)).start()
				elif answ[1] in kb_cmd['admin'] and str(userid) in users['admin']:
					Thread(target=evalcmds,args=('plugins/admin/'+kb_cmd['admin'][answ[1]],toho,torep,answ_text)).start()
				else:
					vkapi.send('У вас нет прав на использование данной команды',toho,torep,None,None)
			elif str(userid) not in users['blacklist'] and answ[0] in kb_name:
				if len(answ) > 1:
					ret = requests.post('https://isinkin-bot-api.herokuapp.com/1/talk',data=(('q',result[5]),('adminname','лост'))).json()
					vkapi.send(ret['text'],result[3],result[1],None,None)
				else:
					vkapi.send('Что такое?',result[3],result[1],None,None)
	except KeyError:
		longpoll = GetLongPollServer()
		continue
	except Exception as error:
		print(error)
	longpoll['ts'] = listen['ts']
