#!/usr/bin/python3
# -*- coding: utf-8 -*-
import requests, json, random, sys

token = json.loads(open('system/info','r').read())['token']
def checktext( answtxt, toho, torep ):
	if not answtxt:
		send('А текст мб стоит вписать?',toho,torep,0,0)
		return False
	return True

def send(text,toho,torep,upload,attach):
	param = {'v':'5.63','peer_id':toho,'access_token':token,'message':text,'forward_messages':torep}
	if attach:
		param.update({'attachment':attach})
	if upload:
		ret = requests.get('https://api.vk.com/meth,od/photos.getMessagesUploadServer?access_token={access_token}&v=5.68'.format(access_token=token)).json()
		with open('tmp/'+upload, 'rb') as f:
			ret = requests.post(ret['response']['upload_url'],files={'file1': f}).text
		ret = json.loads(ret)
		ret = requests.get('https://api.vk.com/method/photos.saveMessagesPhoto?v=5.68&album_id=-3&server='+str(ret['server'])+'&photo='+ret['photo']+'&hash='+str(ret['hash'])+'&access_token='+token).text
		ret = json.loads(ret)
		param.update({'attachment':'photo'+str(ret['response'][0]['owner_id'])+'_'+str(ret['response'][0]['id'])})

	result = requests.post('https://api.vk.com/method/messages.send', data=param)
	return result.text

def search(text,toho,torep,method,item,specparam):
	param = {'v':'5.63','q':text,'count':'200','access_token':token,'forward_messages':torep}
	if specparam:
		param.update(specparam)
	res = requests.post('https://api.vk.com/method/%s'%method, data=param)
	res = json.loads(res.text)
	print(param)
	if res['response']['count']:
		info = ''
		for c in range(10):
			itm = random.randint( 1,len(res['response']['items'])-1)
			info = info+item+str(res['response']['items'][itm]['owner_id'])+'_'+str(res['response']['items'][itm]['id'])+','
		return info

def call(method,specparam):
	param = {'v':'5.63','access_token':token }
	param.update(specparam)
	ret = requests.post('https://api.vk.com/method/%s'%method, data=param)
	return json.loads(ret.text)

def GetLongPollServer():
	longpoll = json.loads(requests.get('https://api.vk.com/method/messages.getLongPollServer?access_token='+token+'&v=5.68&lp_version=2').text)
	try:
		return longpoll['response']
	except KeyError:
		sys.exit( longpoll['error']['error_msg'] )

def ListenLongPollServer(longpoll):
	responce = requests.get('https://{server}?act=a_check&key={key}&ts={ts}&wait=20&mode=2&version=2'.format(server=longpoll['server'], key=longpoll['key'], ts=longpoll['ts'])).json()
	listen = {'result':None,'ts':longpoll['ts']}
	for result in responce['updates']:
		if result[0] == 4:
			listen = {'result':result, 'ts':responce['ts']}
	return listen