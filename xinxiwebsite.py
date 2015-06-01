#!/usr/bin/python3
import smtplib  
import sys, re, urllib.request, os, time
from email.mime.text import MIMEText  

mailto_list=["SSSS@PPPPP.PPPP","SSSS@PPPPP.PPPP","SSSS@PPPPP.PPPP"] 
mail_host="mail.bit.edu.cn"  #设置服务器
mail_user="UUUUU"    #用户名
mail_pass="XXXXX"   #口令 
mail_postfix="bit.edu.cn"  #发件箱的后缀
  
def send_mail(to_list,sub,content):  
    me="hello"+"<"+mail_user+"@"+mail_postfix+">"  
    msg = MIMEText(content,_subtype='plain',_charset='utf-8')  
    msg['Subject'] = sub  
    msg['From'] = me  
    msg['To'] = ";".join(to_list)  
    try:  
        server = smtplib.SMTP()  
        server.connect(mail_host)  
        server.login(mail_user,mail_pass)  
        server.sendmail(me, to_list, msg.as_string())  
        server.close()  
        return True  
    except Exception as e:  
        print(str(e)) 
        return False  

def getPage(html):
    reg = '<divclass="xjevent"><divstyle="margin-top:8px;"><divstyle="float:left;width:580px;line-height:24px;"><bclass="xj_hll"style="margin-right:5px;"><ahref="(.*)"target="_blank">(.*)</a></b><imgsrc="(.*)"/><br/><spanclass="xj_hll">(.*)</span>(.*)&nbsp;&nbsp;<spanclass="xj_hll">(.*)</span>(.*)&nbsp;&nbsp;<spanclass="xj_hll">(.*)</span>(.*)&nbsp;&nbsp;<br/><spanstyle="color:#bbbbbb;">(.*)</span></div></div></div>'
    pageregex = re.compile(reg)
    pages = re.findall(pageregex, html)
    
#    print(len(pages))
#    for page in pages:
#        print(page)

    return pages

def gethtml(page=1):
    page = urllib.request.urlopen("http://10.104.0.225/plugin.php?id=xj_event:event_list_ajax&pc=1&inajax=1&ajaxtarget=event1&page="+str(page))
    html = page.read()
    page.close()
    
    html = html.decode('UTF-8').replace("\t","").replace(" ","").replace("\r","").replace("\n","").replace("</span></div></div></div>","</span></div></div></div>\n").replace("<divclass=\"xjevent\"><div","\n<divclass=\"xjevent\"><div")
#    print(html)
    return html

sizeofpage = 14 
while(1):
    # get pages size
    html = gethtml()
    reg='</div><divstyle="clear:both;height:30px;padding-top:5px;"><divclass="jlpg">(.*)</div></div>]]></root>'
    page= re.compile(reg)
    pagelists = re.findall(page, html)

    if(len(pagelists)>1): sys.exit(1)
    pagelist=pagelists[0]
    #print(pagelist)
    delhtmltag = re.compile("<[^<^>]*>")
    pagestring = delhtmltag.sub("", pagelist)
    #print(pagestring)
    #print(len(pagestring))
    pagesize = len(pagestring) if (len(pagestring)<=9) else ((len(pagestring)+9)/2)
    print("page size : "+str(pagesize))

    # get articles in each page
    pages=[]
    for i in range(1, pagesize+1):
        pages+=getPage(gethtml(i))

#    for page in pages:
#        print(str(page))
    print("articles size is :"+str(len(pages)))
     
    if sizeofpage == 0:
        sizeofpage = len(pages)
        time.sleep(600)

    if len(pages) > sizeofpage:
        sp = len(pages) - sizeofpage
        sizeofpage = len(pages)
        content=""
        for i in range(0,sp):
            content+=str(pages[i])
        if send_mail(mailto_list,"xinxi",content):  
            print( "发送成功" )
        else:  
            print( "发送失败" )

    time.sleep(600)

