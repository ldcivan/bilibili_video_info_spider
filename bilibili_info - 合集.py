# 导入模块
import json
import requests
import time

def change_time(created):
    timeStamp = created  # 10位时间戳
    # timeStamp_13 = 1381419600234# 13位时间戳
    timeArray = time.localtime(timeStamp)  # timeStamp_13 / 1000
    otherStyleTime = time.strftime("%m.%d", timeArray)
    return otherStyleTime

userid = input('输入目标userid：')
series_id = input('输入目标series_id(网址上写作sid)：')
i=1
ifloop=1
# 循环19次，将每一页的数据都抓取到
while ifloop==1 :
    # 模拟浏览器
    headers = {
        'User-Agent': ' Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
    }
    # 包含待爬取信息的url
    url = 'https://api.bilibili.com/x/polymer/space/seasons_archives_list?mid=%s&season_id=%s&sort_reverse=false&page_num=%s&page_size=30' % (userid, series_id, i)
    # 访问url
    r = requests.get(url, headers)
    # 将爬取道德json格式的数据转化为字典
    text = json.loads(r.text)
    # 取出嵌套字典里我们想要的部分
    # 这里的字典嵌套在控制台里其实看的很清楚，我在上面的截图里圈了出来
    res = text['data']['archives']
    aids = text['data']['aids']
    print(aids)
    if aids==[]:
        ifloop=0
    for item in res:
        if "【咩栗】" in item['title']:
            print("跳过%s" % item['title'])#排除需要排除的
        else:
            # 以列表的形式取出对我们有用的数据
            list = ['|-|' + str(change_time(item['ctime'])), '|' + item['title'], '| |{{bililink|' + str(item['bvid']) + '}}', '|']
            # 转化为字符串格式
            result = ''.join(list)
            # 写进文件里
            with open(userid+'_'+series_id+'.txt', 'a+', encoding="utf-8") as f:
                f.write(result + '\n')
    if ifloop==1:
        print("%s结束" % i)
        i = i+1
        time.sleep(2)
    else:
        print("全部结束，进行倒序")

with open(userid+'_'+series_id+'.txt','r', encoding="utf-8") as fp1, open(userid+'_'+series_id+'_out.txt','w', encoding="utf-8") as fp2:
    fp2.write(''.join(fp1.readlines()[::-1]))

print("倒序结束，正在Wiki text化")
with open(userid+'_'+series_id+'_out.txt', 'r', encoding="utf-8") as f:
    contents = f.read()# 打开这个文件
with open(userid+'_'+series_id+'_out.txt', 'w', encoding="utf-8") as f:
    f.write(contents.replace('|', '\n|'))
