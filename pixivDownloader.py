# -*- coding:utf-8 -*-

##本程序作用为：给定一个P站画师的ID，然后遍历下载那个画师所有的画
##因为使用了linux内置的工具，所以只能在liunx环境下工作，不支持windows
##单线程，非多线程。
##由于国内的网络环境，极有可能程序运行失败，建议先ping www.pixiv.net，看数据包的往返时间
##或者traceroute -n www.pixiv.net,如果一半以上都是 *,那多半是不行的。
##挂VPN可破……
##这一版不支持命令行传参数，使用方法很僵硬……只能python DrawDownVer1.py 这样。
##唯一支持的功能：支持给定一个根目录地址，程序会自动在这个根目录下存放（默认位置为本脚本的当前所在目录）
##不用担心图片存放会混杂……下载的图片会自动放在一个新建的文件夹里，文件夹的名字为画师的名字
##比如 给定了根目录地址为 /media/,而被下载画师id为61513，程序会在网站上找到画师的名字 ideolo
##然后建立一个叫做ideolo的文件夹，地址为 /media/ideolo/，图片在这个文件夹存放/
##图片的命名全是数字……
##不支持断点续传，但是程序不会下载已有的图片，比如，已经有一幅 21123432.jpg的图片，下一次更新图片文件
##夹的时候，这幅图片不会下载------当然你已经改名了就另算
##希望退出的时候使用 Ctrl-c 就好，标准的键盘中断……
##只能下载图片，漫画什么的我没有匹配，书签也不行……
##这一版程序相当简陋，不排除有bug出现，如果发现了,请mail-> axdiaoqi220@gmail.com
##由于后一段时间相当忙，下一版遥遥无期，更新了我会发贴的
##
##author ： 风笳(AproSanae)
##version : 0.1
##data 2012-10-20 15:24:07 
##PS:Sanae San Wa Dai Su Ki!!!!

import mechanize
import re
import os
import time

_cookie = mechanize.CookieJar()

#-----------------所有的配置在这里填写---------------------------------
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5'
account = '' #p站账号
password = '' #密码
basepath = '' #文件存放的根目录位置,默认的我是放到这个脚本的目录来着,请注意，如果不为空的字符串，末尾请务必加上/,如 /media/
CSID = 61513 #这个是你想要下载的画师的id,变量名意思是“触手ID”，恩……



##这个函数执行初始化，登录以及提交表单的作用，值得注意的是，国内访问pixiv可能返回慢连接错误，这是不可抗力……

def _initialize(browser):
	browser.set_cookiejar(_cookie)
	browser.addheaders = [('User-Agent',user_agent)]
	print '早苗已经收到指示，开始进行初始化设定,请稍等的说……'
	if not len(_cookie):
		browser.open("https://ssl.pixiv.net/login.php")		
		browser.select_form(nr = 1)
		browser["pixiv_id"] = account
		browser["pass"] = password
		browser.submit()
		print '成功登录，早苗正在寻找图片下载，请注意哦，H是不可以的～'

#这里通过一个正则表达式去找到当前页中所有的图片链接，返回是一个四元素的元组
def _getImgUrl(page):
	pat = r'http://i1.pixiv.net/(.+)/img/(.+)/(.+)\.(png|jpg)'
	pattern = re.compile(pat)	
	image_url = pattern.findall(page)
	return image_url

#同样，通过一个正则表达式去找到指向下一页，下下一页的连接
def _getPageUrl(page):
	pat = r'<a href="(member_illust.php\?id=\d+&p=\d+)">'
	pattern = re.compile(pat)
	page_url = pattern.findall(page)
	return page_url

#收集所有的图片链接，返回
def _collectImgUrl(page_url,img_url):
	for url in page_url:
		url = 'http://www.pixiv.net/'+url
		response = browser.open(url)
		img_url += _getImgUrl(response.read())
	return img_url

def _downloader(img_url,records_url,imgCount,infofile):
	count = 0
	try:
		for element in img_url:
			dirname = element[1]
			filename = element[2][0:-2]+'.'+element[3]
			url = 'http://i1.pixiv.net/'+element[0]+'/img/'+dirname+'/'+filename
		
			if url in records_url:
				continue
			else:
				wget = 'wget ' + url + ' -O ' + basepath  + dirname + '/' + filename + ' --referer=http://www.pixiv.net/'
				os.system(wget)
			infofile.write(url+'\n')
			count += 1
			print '下载进度 %d/%d\n' % (count,imgCount)
			time.sleep(5)
	except KeyboardInterrupt:
		infofile.close()
	infofile.close()
	if account == 'zengli220@163.com' or account == 'axdiaoqi220@gmail.com':
		print '主人,我工作做完了，今天也能一起睡么？（害羞|扭扭捏捏……）恩，可以啊？早苗好开心～～'
	else:
		print '做完了～～主人叫我回家睡觉了，早苗得去照顾他，下次再见了～～'
	
browser = mechanize.Browser()
_initialize(browser)

response = browser.open('http://www.pixiv.net/member_illust.php?id=%d' % CSID)
img_url = _collectImgUrl(_getPageUrl(response.read()),_getImgUrl(response.read()))

#这里声明三个后面需要的变量，img_url是所有图片的集合，imgCount是图片是数目,authorName是存放的文件夹的名称
#不知为何会有重复链接出现，姑且通过集合的手段去除掉
img_url = list(set(img_url))
imgCount = len(img_url)
authorName = img_url[0][1]
print "累了……但是早苗一共找到了%d幅图片哦～～今天早苗也很努力呢（奋斗ing～）" % imgCount

#判断是不是下过这个画师的图，没下过的话建目录，然后建一个记录文档
if os.path.isdir(basepath+authorName):
	infofile = open(basepath+authorName+'/urlinfo.sanae','r+')
	records_url = infofile.read().split()
else:
	os.mkdir(basepath+authorName)
	infofile = open(basepath+authorName+'/urlinfo.sanae','w')
	records_url = []
	
_downloader(img_url,records_url,imgCount,infofile)

