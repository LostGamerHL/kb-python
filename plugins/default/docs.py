if vkapi.checktext(answ_text,toho,torep):
	attach = vkapi.search(answ_text,toho,torep,'docs.search','doc',0)
	if attach:
		vkapi.send('Документы по вашему запросу:',toho,torep,0,attach)
	else:
		vkapi.send('Документов по запросу не найдено',toho,torep,0,0)
