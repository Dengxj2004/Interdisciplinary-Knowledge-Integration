import os

import pandas as pd
from textrank4zh import TextRank4Keyword



#ipc-div
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

def dis(l,gini=0.85):
    n = len(l)
    dis = 0
    for i in l:
        for j in l:
            if i == j:
                continue
            else:
                dis += (1-gini)*dis_ipc(i,j)/(n-1)  # n约掉了
    return dis

def ipc_div(df,df_citation):
    #self ipc-div
    df['IPC'] = df['IPC'].apply(lambda i:str(i).split('; '))
    df['ipc_div'] = ''
    df['ipc_num'] = ''
    for i in range(0,len(df)):
        l = df['IPC'].iloc[i]
        df['ipc_num'].iloc[i] = len(l)
        if len(l) > 1:
            df['ipc_div'].iloc[i] = dis(l)
        else:
            df['ipc_div'].iloc[i] = None

    #citation ipc-div
    df_citation['IPC'] = df_citation['IPC'].apply(lambda i: str(i).split('; '))
    df['引证专利'] = df['引证专利'].apply(lambda i: str(i).split('; '))
    df['ipc_div_citation'] = ''
    df['ipc_num_citation'] = ''
    for i in range(0, len(df)):
        citations = df['引证专利'].iloc[i]
        corr_citation = df_citation[df_citation['公开（公告）号'].isin(citations)]
        l = []
        for ipc in list(corr_citation['IPC']):
            l.extend(ipc)
        l = list(set(list(l)))
        df['ipc_num_citation'].iloc[i] = len(l)
        if len(l) > 1:
            df['ipc_div_citation'].iloc[i] = dis(l)
        else:
            df['ipc_div_citation'].iloc[i] = None

    return df['ipc_div'],df['ipc_div_citation'],df['ipc_num'],df['ipc_num_citation']

#get keywords
def textrank(df,df_citation):
    df['text'] = df['标题 (英文)'] +'. '+ df['摘要 (英文)']
    df['keyword'] = ''
    for i in range(0, len(df)):
        text = df['text'].iloc[i]
        if str(text) != 'nan':
            tr4w.analyze(text=text, lower=True, window=2)
            l = []
            for item in tr4w.get_keywords(num=3, word_min_len=1):
                l.append(item.word)
            df['keyword'].iloc[i] = ','.join(l)
        else:
            df['keyword'].iloc[i] = None

    df_citation['text'] = df_citation['标题 (英文)'] + '. ' +df_citation['摘要 (英文)']
    #df['引证专利'] = df['引证专利'].apply(lambda i: str(i).split('; '))
    df['keyword_citation'] = ''
    for i in range(0, len(df)):
        citations = df['引证专利'].iloc[i]
        corr_citation = df_citation[df_citation['公开（公告）号'].isin(citations)]
        l = []
        for text in list(corr_citation['text']):
            if str(text) != 'nan':
                tr4w.analyze(text=text, lower=True, window=2)
                l1 = []
                for item in tr4w.get_keywords(num=3, word_min_len=1):
                    l1.append(item.word)
                l.extend(l1)
            else:
                continue
        if len(l) > 0:
            l = list(set(list(l)))
            df['keyword_citation'].iloc[i] = ','.join(l)
        else:
            df['keyword_citation'].iloc[i] = None

    return df['keyword'],df['keyword_citation']

