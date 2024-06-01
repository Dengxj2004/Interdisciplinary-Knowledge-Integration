import pandas as pd
import os

#compute pi  pro_3_result.txt  pro_ipc_result.txt
with open("pro_3_result.txt", "r", encoding='utf-8') as f:
    pro = f.readlines()
keys = []
vals = []
ipcs = []
for i in pro:
    t = i.strip('\n').split(',')
    keys.append(t[0])
    ipcs.append(t[1])
    vals.append(float(t[2]))
pro1 = dict(zip(keys,vals))
pro_ipc = dict(zip(keys,ipcs))

with open("pro_ipc_result.txt","r",encoding='utf-8') as f:
    pro = f.readlines()
keys = []
vals = []
for i in pro:
    t = i.strip('\n').split(',')
    keys.append(t[0])
    vals.append(float(t[2].strip('%'))/100.0)
pro2 = dict(zip(keys,vals))

pro_total = {}
for i in pro1.keys():
    pro_total[i] = pro1[i]*pro2[i]

def dis_ipc(i,j):
    if i[0] != j[0]:
        return 16
    elif i[1:3] != j[1:3]:
        return 8
    elif i[3:4] != j[3:4]:
        return 4
    elif i[4:6] != j[4:6]:
        return 2
    else:
        return 1

def rs(l):
    result = 0
    for i in l:
        for j in l:
            if i != j:
                result += dis_ipc(pro_ipc[i],pro_ipc[j])*pro_total[i]*pro_total[j]
    return result

path = r'C:\Users\ADMIN\Desktop\跨领域数据\\'
file_list = []
fields = os.listdir(path+'non_gold')
categories = ['family_top100','family_bottom100','cite_top100','cite_bottom100']

def com_rs(df):
    df['rs'] = ''
    df['rs_citation'] = ''
    for i in range(0, len(df)):
        try:
            l1 = str(df['keyword'].iloc[i]).split(',')
            df['rs'].iloc[i] = rs(l1)
            l2 = str(df['keyword_citation'].iloc[i]).split(',')
            df['rs_citation'].iloc[i] = rs(l2)
        except:
            print('p4b6')
            continue
    return df

print('gold')
df = pd.read_csv(path+'gold3.csv')
df = com_rs(df)
df.to_csv(path+'gold3_rs.csv',index=False)

for field in fields:
    print(field)
    for cate in categories:
        print(cate)
        df = pd.read_csv(path + 'non_gold/' +field + '/' + cate + '3.csv')
        df = com_rs(df)
        df.to_csv(path + 'non_gold/' + field + '/' + cate + '3_rs.csv', index=False)
