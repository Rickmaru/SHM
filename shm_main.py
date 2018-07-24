#author;R.Kunimoto, TAKENAKA co.
#coding:utf-8

import csv
import pandas as pd
from random import random
from janome.tokenizer import Tokenizer
import gensim
from datetime import datetime
import re

path = "C:\\Users\\1500570\\Documents\\R\\WS\\social_heatmap"
rfn ="\\tokyo_noimage_201710_utf8.csv"
wfn ="\\outputs\\output_" +datetime.now().strftime("%Y%m%d%H%M%S") +".csv"
pdfn ="\\pn_ja_utf8.csv"
print(wfn)

rf = pd.read_csv(path+rfn, encoding ="utf-8")
rf["flag_eva"] =0
rf["flag_rep"] =0
rf["polar_score"] =0.0

ng_words =["．","*","['","']","）']" ,"いる","い","う","た","ため","する", "れる","時","し","中","れ","しよ","－","部",
           "為","せ","さ","とき","なり"]
hinshi =["形容詞","動詞","副詞","助動詞","名詞"]
extr_adjective_words =["おいしい","美味しい","旨い","美味い","うまい","不味い","まずい","良い","悪い","楽しい","苦しい",
                       "珍しい","めずらしい","きたない","汚い","高い","たかい","安い","やすい","暑い","寒い","すごい",
                       "しょぼい","おもしろい","面白い","つまらない","可愛い","かわいい","カワイイ","騒がしい","さわがしい","うるさい",]
extr_verb_words =["混む","こむ","空く","すく","開く","閉まる","落ち着く","おちつく","売り切れる"]
extr_noun_words =["久々","ひさびさ","初","毎度","まいど","恒例","綺麗","きれい","キレイ","好き","すき","嫌い","きらい",
                  "キライ","華やか","おだやか","穏やか","豊富"]
extr_adverb_words =["いつも","がっつり","ガッツリ"]

rep_others =re.compile("I'm.at.+")
rep_others_sta =re.compile("I'm.at.+(駅|ホーム|新幹線).+")
rep_verb_words =["行く","いく","来る","くる","去る","食べる","たべる","いただく","呑む","飲む","のむ","買う","売る",
                 "使う","つかう","遊ぶ","あそぶ","育てる","学ぶ","整える","休む","愛する","歩く","見る","観る","みる",
                 "する"]
rep_noun_words =["なう","ナウ","now","食事","飯","メシ","朝飯","ランチ","ディナー","おやつ","デザート","カフェ","お茶",
                 "腹ごしらえ","食べ放題","飲み放題","定食","丼","セット","プレート","名物","天気"]

t = Tokenizer(path+"\\shmdict_simple_utf8.csv", udic_type="simpledic", udic_enc="utf8")

def judge_evaluate(sentence):
    tokens =t.tokenize(sentence)
    for tok in tokens:
        if "形容詞" in tok.part_of_speech and tok.base_form in extr_adjective_words:
            return True
        elif "動詞" in tok.part_of_speech and tok.base_form in extr_verb_words:
            return True
        elif "副詞" in tok.part_of_speech and tok.base_form in extr_adverb_words:
            return True
        elif "名詞" in tok.part_of_speech and tok.base_form in extr_noun_words:
            return True
    return False

def judge_repoprt(sentence):
    tokens =t.tokenize(sentence)
    if bool(rep_others.match(sentence)) ==True:
        if bool(rep_others_sta.match(sentence)) ==False:
            for tok in tokens:
                if tok.part_of_speech.split(",")[1] =="固有名詞":
                    return True
                else:
                    return False
        else:
            return False
    else:
        for tok in tokens:
            if "動詞" in tok.part_of_speech and tok.base_form in rep_verb_words:
                return True
            elif "名詞" in tok.part_of_speech and tok.base_form in rep_noun_words:
                return True
        return False

#極性辞書の作成
pdic =pd.read_csv(path +pdfn)
pdic_verb =pdic[pdic["speech"] =="動詞"]
pdic_auxiliary_verb =pdic[pdic["speech"] =="助動詞"]
pdic_adverb =pdic[pdic["speech"] =="副詞"]
pdic_noun =pdic[pdic["speech"] =="名詞"]
pdic_adjective =pdic[pdic["speech"] =="形容詞"]

t = Tokenizer(path+"\\shmdict_simple_utf8.csv", udic_type="simpledic", udic_enc="utf8")
wf =open(path+wfn,"w+", encoding ="utf-8")

tp =0
tn =0
fp =0
fn =0

i =0
while i <len(rf):
    sen =str(rf.iat[i,5])
    if i %100 ==0:
        print(i,"/",len(rf))
        print(sen)
    tokens =t.tokenize(sen)
    tmp_score =0.0
    tmp_denom =0
    for line in tokens:
        tmp_denom +=1
        if "動詞" in line.part_of_speech:
            try:
                tmp_score +=float(pdic_verb[pdic_verb["base" ]==str(line.base_form)].iat[0,3])
            except:
                pass
        elif "助動詞" in line.part_of_speech:
            try:
                tmp_score +=float(pdic_auxiliary_verb[pdic_auxiliary_verb["base" ]==str(line.base_form)].iat[0,3])
            except:
                pass
        elif "副詞" in line.part_of_speech:
            try:
                tmp_score +=float(pdic_adverb[pdic_adverb["base" ]==str(line.base_form)].iat[0,3])
            except:
                pass
        elif "名詞" in line.part_of_speech:
            try:
                tmp_score +=float(pdic_noun[pdic_noun["base" ]==str(line.base_form)].iat[0,3])
            except:
                pass
        elif "形容詞" in line.part_of_speech:
            try:
                tmp_score +=float(pdic_adjective[pdic_adjective["base" ]==str(line.base_form)].iat[0,3])
            except:
                pass
    #tmp_score =tmp_score/tmp_denom
    rf.iat[i,12] =tmp_score
    #ルールベース
    if judge_evaluate(sen) ==True:
        rf.iat[i,10] =1
    if judge_repoprt(sen) ==True:
        rf.iat[i,11] =1
    if rf.iat[i,10] ==1 or rf.iat[i,11] ==1:
        if rf.iat[i,3] ==0:
            tp +=1
        else:
            fp +=1
    else:
        if rf.iat[i,3] ==1:
            tn +=1
        else:
            fn +=1
    i +=1
rf.to_csv(path+wfn, encoding ="utf-8",)

"""
for line in rf:
    tmp =t.tokenize(str(line[6]))
    for token in tmp:
        if token.part_of_speech in hinshi:
"""
print("---------------------\n真陽性:"+str(tp)+"|偽陰性:"+str(fn)+"\n---------------------\n偽陽性:"+str(fp)+"|真陰性:"+str(tn)+"\n---------------------")
print("precision of positive:", str(float(tp/(tp+fp))))
print("precision of negative:", str(float(tn/(tn+fn))))
print("recall of positive:", str(float(tp/(tp+fn))))
print("recall of negative:", str(float(tn/(tn+fp))))

print("finished")