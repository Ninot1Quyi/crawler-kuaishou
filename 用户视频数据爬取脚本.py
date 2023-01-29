import msvcrt
import pandas as pd
import os
from tqdm import tqdm
import requests
from datetime import datetime
from datetime import timedelta
from multiprocessing.pool import Pool
import time
import random


nowdate = datetime.today()  # 当前时间
# 日期格式定义
dateFormatter = "%Y/%m/%d/%H"
# 设置时间限度
hours_before_10 = nowdate - timedelta(hours=10)  # 十个小时前的时间
hours_before_20 = nowdate - timedelta(hours=20)  # 二十个小时前的时间
# 统计结果存在的文件
res_path = r"爬取到的可能的视频.xlsx"
global upside
global add
global reset  #初始等待时间上界
reset = 10
upside = reset
add = 2 #每次等待时间增加两秒
def wait(set=0):
    global upside
    if set != 0:
        randomT = random.uniform(0, set)
    else:
        print("等待")
        if upside == reset:
            randomT = random.uniform(0, upside)
        else:
            randomT = random.uniform(upside-add,upside)
    time.sleep(round(randomT, 2))

def Crawling(userid):
    global upside
    global reset
    global add
    usefulWorkListUnit = list()  # 作者名字 视频描述 时间差 点赞数 视频链接
    Referer = r"https://www.kuaishou.com/profile/" + userid
    prefix = r"https://www.kuaishou.com/profile/"
    # 伪装
    headers = {
        'content-type': 'application/json',
        'Cookie': r'kpf=PC_WEB; kpn=KUAISHOU_VISION; clientid=3; didv=1671761659101; did=web_ef18ba176d773f27136ea82d728dab4c; client_key=65890b29; _did=web_208573213C9DCE2A; ktrace-context=1|MS43NjQ1ODM2OTgyODY2OTgyLjM5MjMxMjQxLjE2NzQ4OTM5MzQ3NTUuMTA4ODk0|MS43NjQ1ODM2OTgyODY2OTgyLjM1NjQ4OTU1LjE2NzQ4OTM5MzQ3NTUuMTA4ODk1|0|graphql-server|webservice|false|NA; userId=1867053895; kuaishou.server.web_st=ChZrdWFpc2hvdS5zZXJ2ZXIud2ViLnN0EqABny5WhxaZjJmbnhiZbaiOPsP65uTDQIJPh2ZrZ7NLfFWZ9ModhaHKJQvAYQzUQJaJC0WUGHQs_SUZ4GOcSyPvMUle1o5-Gpu25Zv5sbacNuHvATlfAxvaGS67Bs8d7dQGsleiOXlC66l15m9ZswT_4l0RT6ax7fcMeshCrRNDaaL__94J-P77vWjjMD4ty4-Q7XyHIfgAHNUOYPx2KQF2wRoSPic3ODA5dC1PisVLgMefbzz0IiCmHJGz0WT1XDEAEW2R15JkZMBJR55gD0TpjXLUNcVnPigFMAE; kuaishou.server.web_ph=ebda1a4cdf93037a893b89e45028f3af60cb',
        'Host': 'www.kuaishou.com',
        'Origin': 'https://www.kuaishou.com',
        'Referer': Referer,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36 Edg/107.0.1418.26',
    }
    #userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
    url = r"https://www.kuaishou.com/graphql"

    json = {
        "operationName": "visionProfilePhotoList",
        "query": "fragment photoContent on PhotoEntity {\n  id\n  duration\n  caption\n  originCaption\n  likeCount\n  viewCount\n  realLikeCount\n  coverUrl\n  photoUrl\n  photoH265Url\n  manifest\n  manifestH265\n  videoResource\n  coverUrls {\n    url\n    __typename\n  }\n  timestamp\n  expTag\n  animatedCoverUrl\n  distance\n  videoRatio\n  liked\n  stereoType\n  profileUserTopPhoto\n  musicBlocked\n  __typename\n}\n\nfragment feedContent on Feed {\n  type\n  author {\n    id\n    name\n    headerUrl\n    following\n    headerUrls {\n      url\n      __typename\n    }\n    __typename\n  }\n  photo {\n    ...photoContent\n    __typename\n  }\n  canAddComment\n  llsid\n  status\n  currentPcursor\n  tags {\n    type\n    name\n    __typename\n  }\n  __typename\n}\n\nquery visionProfilePhotoList($pcursor: String, $userId: String, $page: String, $webPageArea: String) {\n  visionProfilePhotoList(pcursor: $pcursor, userId: $userId, page: $page, webPageArea: $webPageArea) {\n    result\n    llsid\n    webPageArea\n    feeds {\n      ...feedContent\n      __typename\n    }\n    hostName\n    pcursor\n    __typename\n  }\n}\n",
        "variables": {"userId": userid, "pcursor": "", "page": "profile"}
    }
    # 1.发送请求
    # 方式

    response = requests.post(url=url, headers=headers, json=json)
    # print(response)
    # 2.获取技术
    json_data = response.json()
    # 3.解析数据
    # 类型：字典+list
    # print(json_data["data"])
    while "data" not in json_data:
        upside += add
        print(json_data)
        wait()
        response = requests.post(url=url, headers=headers, json=json)
        json_data = response.json()
    else:
        upside = reset
    if "data" in json_data and "visionProfilePhotoList" not in (json_data["data"]).keys():

        print("更换浏览器")
        cookie=r"kpf=PC_WEB; kpn=KUAISHOU_VISION; clientid=3; did=web_015d58060aa7f4001c07efa4fac7b6d8; didv=1674962339460; userId=1867053895; kuaishou.server.web_st=ChZrdWFpc2hvdS5zZXJ2ZXIud2ViLnN0EqABXWIT_gC-MEmpxFuVBBwt1rMJHYhbzyiRZfQnJZ5iZ0jut-eWY3pXftpbEvT5gBWUwvw927tdUd5QOau6Xd3d6dXGujxP7L_a8HaviPvjRixfeGSUXn2yuuI2q5e_yDhO9nJttulCvokqmA8po8DD6Refa724lmXhSx8t2yZ1bL3DsriodU8QcnKli5sF-9VILOXb0b31FJ26c4Beor6a3BoSfVpfCMyKId3v5a5yUz8_gvvmIiDkRTe23IIi6ZRKHqfWuo0lWe1BGw1TqJA5pp5JTURP0ygFMAE; kuaishou.server.web_ph=11c00bb18a4b1569fb8fcd8e43d474937201"
        userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
        headers['User-Agent'] = userAgent
        headers["Cookie"]=cookie
        wait()
        response = requests.post(url=url, headers=headers, json=json)
        json_data = response.json()
        while "data" not in json_data:
            upside += add
            print(json_data)
            wait()
            response = requests.post(url=url, headers=headers, json=json)
            json_data = response.json()
        else:
            upside = reset
        while "data" in json_data and "visionProfilePhotoList" not in (json_data["data"]).keys():
            #刷新页面
            print("刷新页面")
            #有时间间隔的刷新
            wait()
            response = requests.post(url=url, headers=headers, json=json)
            json_data = response.json()
            while "data" not in json_data:
                upside += add
                print(json_data)
                wait()
                response = requests.post(url=url, headers=headers, json=json)
                json_data = response.json()
            else:
                upside = reset

    userData = json_data["data"]["visionProfilePhotoList"]["feeds"]

    length = len(userData)
    length = length if length < 10 else 10
    for i in range(length):
        # for userdata in userData:
        userdata = userData[i]
        likeCount = userdata["photo"]["likeCount"]  # 视频点赞数
        if likeCount[-1] == "万":
            video_url = userdata["photo"]["photoUrl"]  # 视频链接
            # 获取视频发布时间
            postDateIndex = video_url.index("20")
            dateString = video_url[postDateIndex:postDateIndex + 13:]
            postDate = datetime.strptime(dateString, dateFormatter)  # 视频发布时间

            if postDate > hours_before_20:  # 应用:发布时间小于20个小时
                userName = userdata["author"]["name"]  # 作者名字
                userUrl = prefix + userdata["author"]["id"]
                workDescription = userdata["photo"]["originCaption"]  # 作品描述
                photoUrl = userdata["photo"]["photoUrl"]  # 视频链接

                # 记录
                usefulWorkListUnit.append(userName)  # 作者名字
                usefulWorkListUnit.append(userUrl)  # 作者主页链接
                usefulWorkListUnit.append(workDescription)  # 作品描述
                usefulWorkListUnit.append(str((nowdate - postDate)))  # 时间差
                usefulWorkListUnit.append(likeCount)  # 点赞数
                usefulWorkListUnit.append(photoUrl)  # 视频链接

    return usefulWorkListUnit  # 一个进程的返回结果


#多进程任务显示进度条
def run_imap_mp(func, argument_list, num_processes='', is_tqdm=True):
    '''
    多进程与进度条结合

    param:
    ------
    func:function
        函数
    argument_list:list
        参数列表
    num_processes:int
        进程数，不填默认为总核心-3
    is_tqdm:bool
        是否展示进度条，默认展示
    '''
    result_list_tqdm = []
    try:
        import multiprocessing
        if num_processes == '':
            num_processes = 1  #一共12个核心,我就用1个
        pool = multiprocessing.Pool(processes=num_processes)

        if is_tqdm:
            from tqdm import tqdm
            for result in tqdm(pool.imap(func=func, iterable=argument_list), total=len(argument_list)):
                result_list_tqdm.append(result)
        else:
            for result in pool.imap(func=func, iterable=argument_list):
                result_list_tqdm.append(result)
        pool.close()
    except:
        result_list_tqdm = list(map(func,argument_list))
    return result_list_tqdm


if __name__ == "__main__":
    # 开始爬取数据
    source_path = r"我的关注列表信息.xlsx"  # 源文件
    df = pd.DataFrame(pd.read_excel(source_path))
    NAME = list(df["NAME"])  # 获得所有人的名字
    USERID = list(df['USERID'])

    res = list()  # 临时存储结果
    for userid in tqdm(USERID):
        res.append(Crawling(userid))

    # #多进程运行
    # pool = Pool()
    # res = run_imap_mp(Crawling,USERID)
    # pool.close()  # 关闭进程池，不再接受新的进程
    # pool.join()  # 主进程阻塞等待子进程的退出


    # 进行拼合
    usefulWorkList = list()
    for item in res:
        usefulWorkList = usefulWorkList + item

    print(usefulWorkList)


    userNameList = usefulWorkList[0::6]  # 作者名字
    userUrlList = usefulWorkList[1::6]
    workDescriptionList = usefulWorkList[2::6]  # 作品描述
    timedifferenceList = usefulWorkList[3::6]  # 时间差
    likeCountList = usefulWorkList[4::6]  # 点赞数
    photoUrlList = usefulWorkList[5::6]  # 视频链接


    df_w = pd.DataFrame(
        data=[userNameList, userUrlList, workDescriptionList, timedifferenceList, likeCountList, photoUrlList],
        index=["作者名字", "作者主页", "作品描述", "时间差", "点赞数", "视频链接"]).T
    print(df_w.head())
    if not df_w.empty:
        df_w.to_excel(res_path)
        print("统计完毕！")
    else:
        print("[ERROR] 未筛选出满足条件的视频")
