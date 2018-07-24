#author;R.Kunimoto, TAKENAKA co.
#coding:utf-8

import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

path = "C:\\Users\\1500570\\Documents\\R\\WS\\social_heatmap\\outputs"
rfn ="\\output_20180625195827_utf8.csv"
wfn ="\\output_summary_" +datetime.now().strftime("%Y%m%d%H%M%S") +".csv"

rf = pd.read_csv(path+rfn, encoding ="utf-8")

plt.subplot(1,3,1)
plt.hist(np.array(rf.polar_score),bins =14, range=(-12,2))
plt.title("all data",fontsize=7)
plt.xlabel("polar value", fontsize=7)
plt.ylabel("num of tweets", fontsize=7)
plt.tick_params(labelsize=7)

plt.subplot(1,3,2)
plt.hist(np.array(rf[rf["a"] ==0].polar_score),bins =14, range=(-12,2))
plt.title("goal data",fontsize=7)
plt.xlabel("polar value", fontsize=7)
plt.ylabel("num of tweets", fontsize=7)
plt.tick_params(labelsize=7)

plt.subplot(1,3,3)
plt.hist(np.array(rf[rf["a"] ==1].polar_score),bins =14, range=(-12,2))
plt.title("not-goal data",fontsize=7)
plt.xlabel("polar value", fontsize=7)
plt.ylabel("num of tweets", fontsize=7)
plt.tick_params(labelsize=7)

plt.show()