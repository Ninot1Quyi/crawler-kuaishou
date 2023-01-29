import msvcrt
import pandas as pd
import os
from tqdm import tqdm


# 读取关注列表文件
def getPaper(path):
    #prefix = r"https://www.kuaishou.com/profile/"
    paperlist = list()
    file = open(path, encoding="utf-8")
    while True:
        line = file.readline()
        if line:
            line = line.rstrip()
            if line:
                # paperlist.append(line)
                if "user_name" in line:
                    paperlist.append(line[18:-2])
                if "user_id" in line:
                    paperlist.append(line[16:-2])
        else:
            break
    file.close()
    return paperlist


# main
source_path = r"我的关注列表信息.txt"
res_path = r"我的关注列表信息.xlsx"
following_id = list()
following_id = getPaper(source_path)
for item in following_id:
    print(item)
print(len(following_id))
if len(following_id) % 2 != 0:
    print("error[数据异常，用户与链接不匹配]")
    exit()
# 数据匹配进行接下来的出来
print(following_id[0::2])
print(len(following_id[0::2]))
print(following_id[1::2])
print(len(following_id[1::2]))
# 将用户名与链接对应起来-整理成字典 可以自动去重
followingDis = {k: v for k, v in zip(following_id[0::2], following_id[1::2])}
print(followingDis)
print("一共关注的人数为：", len(followingDis))
# 将数据写入到excel文件中
df_w = pd.DataFrame(list(followingDis.items()), columns=["NAME", "USERID"])
df_w.to_excel(res_path)

