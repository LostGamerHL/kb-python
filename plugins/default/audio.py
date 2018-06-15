if vkapi.checktext(answ_text,toho,torep):
	attach = vkapi.search(answ_text,toho,torep,'audio.search','audio',{'sort':2})
	if attach:
		vkapi.send('Музыка по вашему запросу:',toho,torep,0,attach)
	else:
		vkapi.send('Музыка по запросу не найдена',toho,torep,0,0)
