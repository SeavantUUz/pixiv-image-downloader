# -*- coding:utf-8 -*-

import optparse
import ConfigParser

import platform

def get_encode():
	if platform.system() == 'Linux':
		return 'UTF-8'
	elif platform.system() == 'Windows':
		return 'gb2312'
	else:
		print "Sanae could not run on your system..."
		sys.exit(1)
	
def writeToConfig(account,password,OsName,CSID,basepath):
	config = ConfigParser.SafeConfigParser()
	fp = open('Sanae.ini','w')
	config.add_section('info')
	config.set('info','account',account)
	config.set('info','password',password)
	config.set('info','os',OsName)
	config.set('info','CSID',CSID)
	config.set('info','basepath',basepath)
	config.write(fp)
	fp.close()
	
	
def checkInput(options):
	if options.detail:
		help_doc()
		return False
	if options.account == '' or options.password == '':
		print '''
		早苗发现您的输入不太对哦，主人让早苗转告您，
		帐号和密码是必须输入的，重新输入吧，或者再调用 
		python pixivDownloader -d 看看主人的说明'''.decode('UTF-8').encode(get_encode())
		print ''
		return False
	if options.CSID == '':
		print '''
		哎嘿嘿，您不输入画师ID的话，早苗也不知道你要找谁啊，
		再看看主人的说明吧,
		python pixivDownloader -d'''.decode('UTF-8').encode(get_encode())
		print ''
		return False
	if options.os == 'Linux':
		print '''
		主人要求早苗向您确认一下，您的系统真的是Linux么？
		这项由于是默认值，总有人搞错……搞错就没法用了啊~'''.decode('UTF-8').encode(get_encode())
		a = raw_input('''
		早苗向您确认您的系统是否真是Linux (y/n):'''.decode('UTF-8').encode(get_encode()))
		if a.lower() == 'y' or a.lower() == 'yes':
			return True
		elif a.lower() == 'n' or a.lower() == 'no':
			print '''
		主人担心对了～～主人好厉害～'''.decode('UTF-8').encode(get_encode())
			print ''
			options.os = 'Windows'
			return True
		else:
			print '''
		这是什么？早苗虽然英语很好，但是这个早苗不认识~'''.decode('UTF-8').encode(get_encode())
			return False 
	if options.os == 'Windows':
		print '''
		主人要求早苗向您确认一下，您的系统真的是Windows么？
		这项由于是默认值，总有人搞错……搞错就没法用了啊~'''.decode('UTF-8').encode(get_encode())
		a = raw_input('''
		早苗向您确认您的系统是否真是Windows (y/n):'''.decode('UTF-8').encode(get_encode()))
		if a.lower() == 'y' or a.lower() == 'yes':
                        return True
		elif a.lower() == 'n' or a.lower() == 'no':
			print '''
		主人担心对了～～主人好厉害～'''.decode('UTF-8').encode(get_encode())
			options.os = 'Linux'
			return True
		else:
			print '''
		这是什么？早苗虽然英语很好，但是这个我不认识~'''.decode('UTF-8').encode(get_encode())
			return False 
	return True
	
def help_doc():
	doc = '''
	程序名：
		早苗的图片游廊（尽管极有可能文件名不是这个……）
	程序用途：
		根据画师的ID下载这位画师的全部画作，请注意，由于某种不可知的原因
		（时间……），并不能下载“所有”的画作，具体而言，漫画是不行的，单独
		的图片没有任何问题。
	已知问题：
		由于大陆网络环境恶劣，很有可能会返回一个错误，而使得程序无法工作，
		这和程序本身没有关系，请注意。解决办法是挂VPN……（笑），建议先
		ping www.pixiv.net，看数据包的往返时间，或者
		traceroute -n www.pixiv.net,如果一半以上都是 *,
		那多半是不行的。
	使用说明：
		如果您是第一次使用，这份说明请务必仔细阅读，虽然我已经尽力排除了
		意外因素，但是并不代表程序没有任何问题。
	  	第一次使用，请按照以下格式输入代码 
	  	pixivDownloader.py -a 你的P站帐号
	  	-p 你的P站密码 
	  	-o 操作系统名字（只能从 Linux,Windows中选择）
	  	-i 你想要下载的画师的ID号 
	  	-b 你希望的图片储存的根目录(比如 E:\\Pixiv,或者 
	  	/media/E/Pixiv,
	  	诸如此类都可以)，可以不使用这个选项，那样就保存在当前目录
	  	-s 写入配置文件（第一次最好有，这样以后就不需要这样输入了）
	  	如果感觉比较复杂的话，这里有一个例子
	  	pixivDownloader.py -a xxxx@163.com -p xxxxx -o Linux 
	  	-i 61513 -s
	  	第一次的话，这样就可以了，这样第二次使用的时候 直接 
	  	pixivDownloader.py就好
	注意：
		如果依然对用法困惑，或者有bug，请发送邮件到 
		axdiaoqi220@gmail.com
		可以任意修改，为了不对pixiv服务器造成影响，如果你重写了多线程
		版本，请不要随意传播，这是我唯一的希望
	作者：
		风笳(AproSanae|LoveSanae)
	版本:
		1.1
	时间:
		2012-10-28 20:35:54 
	备注:
		程序开始执行以后，提示信息由早苗小姐提供，要感谢勤劳的早苗小姐
		哦~~
		Sanae San Wa Dai Su ki!!!
	'''
	print doc.decode('UTF-8').encode(get_encode())
	

