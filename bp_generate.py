from .format_gz import *
from .boxplot import * 
#import matplotlib
#matplotlib.use('Agg')
from matplotlib import pyplot as plt

def bp_generate(titles,files,snum,blocks,labels,figname,mean=False):
    fig = plt.figure(figsize=(30,len(files)*10))
    filenum=1
    for fn in files:
        data=bp_format(fn,snum,blocks)
        ax = plt.subplot(len(files),1,filenum)
        pvalue=generate_boxplot(ax,data,labels,mean)
        addon=' , pvalue='+pvalue
        if not mean:
            addon=''
        ax.set_title(titles[filenum-1]+addon,fontsize=30)
        ax.set_xlabel("bins",fontsize=30)
        ax.set_ylabel("Column z-score",fontsize=30)
        ax.yaxis.set_tick_params(labelsize=24)
        ax.xaxis.set_tick_params(labelsize=24)
        filenum+=1
    plt.savefig(figname)

if __name__=="__main__":
    bp_generate(['1542385493.7215164_temp_cgi_z','1542385493.7215164_temp_gb_z'],4,30,["GSM2148380_CLL_ATAC-seq_50_1-5-35290_ATAC27-8","GSM2148382_CLL_ATAC-seq_244_1-5-16241_ATAC30-2","GSM2148384_CLL_ATAC-seq_244_1-5-33025_ATAC30-1","GSM2148386_CLL_ATAC-seq_552_1-5-12302_ATAC31-7"],"temp.png")
