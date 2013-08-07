# -*- coding:utf-8 -*-

##本程序作用为：给定一个P站画师的ID，然后遍历下载那个画师所有的画
##单线程，非多线程。
##不用担心图片存放会混杂……下载的图片会自动放在一个新建的文件夹里，文件夹的名字为画师的名字
##比如 给定了根目录地址为 /media/,而被下载画师id为61513，程序会在网站上找到画师的名字 ideolo
##然后建立一个叫做ideolo的文件夹，地址为 /media/ideolo/，图片在这个文件夹存放/
##图片的命名全是数字……
##不支持断点续传，但是程序不会下载已有的图片，比如，已经有一幅 21123432.jpg的图片，下一次更新图片文件
##夹的时候，这幅图片不会下载------当然你已经改名了就另算
##希望退出的时候使用 Ctrl-c 就好，标准的键盘中断……
##只能下载图片，漫画什么的我没有匹配，书签也不行……
##这一版程序相当简陋，不排除有bug出现，如果发现了,请mail-> axdiaoqi220@gmail.com
##
##author ： 风笳(AproSanae)
##version : 0.1
##data 2012-10-20 15:24:07 
##PS:Sanae San Wa Dai Su Ki!!!!
## ------------------
##data 2013-8-7 重写了整个程序……
##使用requests代替machinze

import requests
import pickle,re,os,time,sys,optparse,ConfigParser,platform,codecs
from initConfig import *
	
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en; rv:1.9.1.5) Gecko/20091102 Firefox/3.5.5'

if platform.system() == 'Linux':
	typeCode = 'UTF-8'
elif platform.system() == 'Windows':
	typeCode = 'gb2312'
else:
	print "Sanae could not run on your system..."
	sys.exit(1)
	

pat1 = r'''src="(http://i\d\.pixiv\.net/(img\d+?)/img/(.+?)/(\d+?)_s\.(png|jpg))"\s'''
pattern1 = re.compile(pat1)	
pat2 = r'''src="(http://i\d\.pixiv.net/img-inf/img/.+?/(\d+?)_s\.(png|jpg))"\s'''
pattern2 = re.compile(pat2)

# 这里通过一个正则表达式去找到当前页中所有的图片链接，返回是一个四元素的元组
# P站老的链接可以通过下面的正则式进行匹配
def _getOldImgUrl(page):
    global pattern1
    image_old_url = pattern1.findall(page)
    return image_old_url

# P站使用了新的链接规则
def _getNewImgUrl(page):
    global pattern2
    image_new_url = pattern2.findall(page)
    return image_new_url

# 同样，通过一个正则表达式去找到指向下一页，下下一页的连接
# 也注意，这个链接也变动过
def _getPageUrl(page):
    pat = r'''href="(\?id=\d+&amp;p=\d+)"'''
    pattern = re.compile(pat)
    page_url = pattern.findall(page)
    ## 记住要算上第一面
    return len(page_url)

## 收集所有的图片链接
def _collectImageUrl(session,page_urls):
    image_old_links=[]
    image_new_links=[]
    for link in page_urls:
        r = session.get(link)
        image_old_links += _getOldImgUrl(r.text)
        image_new_links += _getNewImgUrl(r.text)
    return image_old_links,image_new_links

def _parserInput():
## 这个是三无状态（笑），第一次使用，然后不知道怎么用
    if sys.argv[1:] == []:
        if os.path.isfile('Sanae.ini') == False:
	    print ''
	    print '''
		不会使用？主人建议早苗告诉你，请输入 
		python pixivDownloader.py -d 
		或者 输入 python pixcDownloader.py -h 
		试试哦，或者看看主人写的文档～'''.decode('UTF-8').encode(typeCode)
	    print ''
	    sys.exit(1)
			
    config = ConfigParser.SafeConfigParser()
    ##当没有配置文件时，给一个默认的配置文件
    ##读取配置文件
    if config.read('Sanae.ini') == []:
        print '''
		早苗建立了一个配置文件，但是这只是默认的哦，
		还需要在命令行传入参数的~~'''.decode('UTF-8').encode(typeCode)
	print ''

	fp = open('Sanae.ini','w')
	config.add_section('info')
	config.set('info','account','')
    	config.set('info','password','')
	config.set('info','os','Linux')
	config.set('info','CSID','')
	config.set('info','basepath','')
	config.write(fp)
	fp.close()

	##防止初次使用或者不熟悉的用户输入错误
    usage = "usage: %prog [options] arg1 arg2"
    ##使用下面的代码解析用户传入
    parser = optparse.OptionParser(usage)
    parser.add_option('-a','--account',dest = 'account',
		        action = 'store',default = config.get('info','account'),
			help = 'Your account of pixiv.net')
    parser.add_option('-p','--password',dest = 'password',
			action = 'store',default = config.get('info','password'),
			help = 'Your password of pixiv.net')
    parser.add_option('-o','--os',dest = 'os',action = 'store',
			default = config.get('info','os'),
			help = "The OS's name,'Linux' or 'Windows'")
    parser.add_option('-i','--id',dest = 'CSID',action = 'store',
                        default = config.get('info','CSID'),
                        help = "The drawer's ID which you are trying to download")
    parser.add_option('-b','--basepath',dest = 'basepath',action = 'store',
                        default = config.get('info','basepath'),
                        help = "The root path of your image-dirs")
    parser.add_option('-s','--save',dest = 'save',action = 'store_true',
                        default = False,
                        help ='Save your configration into local_computer')
    parser.add_option('-d','--detail',dest = 'detail',action = 'store_true',
			default = False,
			help = 'Print detail information by Chinese')
    options,remainder = parser.parse_args()

    return options

      
	
			
def main():	
    options = _parserInput()
    print '''
	    早苗接受了你的输入，正在检查，马上告诉你结果~'''.decode('UTF-8').encode(typeCode)
    print ''

    if checkInput(options):	
        account = options.account
	password = options.password
	OsName = options.os
	CSID = options.CSID
	basepath = options.basepath
	if options.save:
	    writeToConfig(account,password,OsName,CSID,basepath)
        print '''
	    早苗检查完成!马上为您连接~~'''.decode('UTF-8').encode(typeCode)

    else:
        print '''
            欧尼酱有些配置填写错了哦，早苗表示不理解呢，好好看看主人大人的说明吧？'''.decode('UTF-8').encode(typeCode)
	sys.exit(1)

    
    session = requests.Session()
    print '''
	    开启session模式'''.decode('UTF-8').encode(typeCode)

    session.headers['User-Agent'] = user_agent
    print ''

    print '''
	    伪造请求头已装入，开始进行初始化设定,请稍等的说……'''.decode('UTF-8').encode(typeCode)
    print ''

    data = {
            'mode':'login',
            'pixiv_id':account,
            'pass':password,
            'skip':'1'}
    print '''
	    post包封装完成，准备投递'''.decode('UTF-8').encode(typeCode)
    print ''

    resp = session.post('https://www.secure.pixiv.net/login.php?lang=zh',data=data)
    if resp.status_code == 200:
        print '''
            嗯哼～早苗已经成功登入了'''.decode('UTF-8').encode(typeCode)
        print ''
    else:
        print '''
            阿咧？为什么早苗登录不了呢～欧尼酱没搞错什么东西吧，要不然问问主人大人？'''.decode('UTF-8').encode(typeCode)
        print ''
        sys.exit(1)

    index_page = 'http://www.pixiv.net/member_illust.php?id=' + CSID
    resp = session.get(index_page)
    if not resp.status_code == 200:
        print '''
            找不到这位画师的id呢，欧尼酱没弄错什么吧？'''.decode('UTF-8').encode(typeCode)
        print ''
        sys.exit(1)
        
    lenPage = _getPageUrl(resp.text)
    page_urls = [index_page]
    page_urls += [index_page+'&p='+str(i+2) for i in range(lenPage)]
    img_old_urls,img_new_urls = _collectImageUrl(session,page_urls)
    Download(img_old_urls,img_new_urls,basepath,session)


def Download(*args):

    count = 0
    img_old_urls = args[0] or []
    img_new_urls = args[1] or []
    basePath = args[2] or '.'
    session = args[3]
    ## 分析出作者名字
    try:
        authorName = img_old_urls[0][2]
    except IndexError:
        print ''' 
            嗯，由于P站变更了某些规则，导致早苗无法完成作者名的自动寻找，需要欧尼酱您手动输入哦~~'''.decode('UTF-8').encode(typeCode)
        print ''
        print "Please input the author's name:"
        authorName = raw_input() 
    path = os.path.join(basePath,authorName)
    if not os.path.exists(path):
        os.mkdir(path)
    image_urls = [i[0].replace('_s','') for i in img_old_urls]
    image_urls += [i[0].replace('_s','') for i in img_new_urls]
    image_urls = set(image_urls)
    imageNum = len(image_urls)
    
    ## 一种优雅的方式
    try:
        with codecs.open('_downloadedImage.sanae','rb','utf-8') as f:
            record_urls = pickle.load(f)
    except IOError:
        record_urls = []

    for url in image_urls:
        ## 每下载十张图片存档一次
        if not count % 0:
            with codecs.open('_downloaderImage.sanae','wb','utf-8') as f:
            pickle.dump(record_urls,f)

        if url in record_urls:
            count += 1
            print '{0}/{1}'.format(count,imageNum)
            continue
        else:
            _download(session,url,path)
            count += 1
            print '{0}/{1}'.format(count,imageNum)
            record_urls.append(url)

    with codecs.open('_downloaderImage.sanae','wb','utf-8') as f:
        pickle.dump(record_urls,f)

    print ''' 
            下载完了哦，您辛苦了～～早苗得回去给主人做饭了，他没有我真是什么都干不了（叹气，摊手），嗯，拜拜了～～'''.decode('UTF-8').encode(typeCode)
    print ''


def _download(session,image_url,basepath):
    filename = image_url.split('/')[-1]
    headers = {'Referer':'http://www.pixiv.net/'}
    r = session.get(image_url,headers=headers,stream=True)
    path = os.path.join(basepath,filename)
    with open(path,'wb') as f:
        for chunk in r.iter_content(1024):
            f.write(chunk)

if __name__ == "__main__":
    main()
