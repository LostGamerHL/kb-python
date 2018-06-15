if vkapi.checktext(answ_text,toho,torep):
	attach = vkapi.search(answ_text,toho,torep,'video.search','video',{'adult':1})
	if attach:
		vkapi.send('Видео по вашему запросу:',toho,torep,0,attach)
	else:
		vkapi.send('Видео по запросу не найдены.',toho,torep,0,0)

