if vkapi.checktext(answ_text,toho,torep):
	attach = vkapi.search(answ_text,toho,torep,'photos.search','photo',0)
	if attach:
		vkapi.send('Фото по вашему запросу:',toho,torep,0,attach)
	else:
		vkapi.send('Фото по запросу не найдено',toho,torep,0,0)
