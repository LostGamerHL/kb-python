if vkapi.checktext(answ_text,toho,torep):
	cmd = answ_text.split('<br>')
	flnm=str(random.random())
	with open('tmp/%s'%flnm, 'w') as cl:
		for i in range(len(cmd)):
			cl.write(cmd[i]+'\n')
	shell = subprocess.Popen('chmod 755 tmp/%s;bash tmp/%s 2>&1'%(flnm,flnm),shell=True,stdout=subprocess.PIPE)
	output = shell.communicate()[0]
	vkapi.send(output,toho,torep,0,0)
	os.remove('tmp/'+flnm)
