import matplotlib
matplotlib.use('Agg')
from matplotlib.pyplot import plot, show, savefig, xlim, figure, \
                hold, ylim, legend, boxplot, setp, axes
from matplotlib import pyplot as plt
import numpy as np
from scipy.stats import ks_2samp

# function for setting the colors of the box plots pairs
def setBoxColors(bp,num,color):
    for i in range(num):
        setp(bp['boxes'][i], color=color[i])
        setp(bp['caps'][2*i], color=color[i])
        setp(bp['caps'][2*i+1], color=color[i])
        setp(bp['whiskers'][2*i], color=color[i])
        setp(bp['whiskers'][2*i+1], color=color[i])
        setp(bp['medians'][i], color=color[i])

# Some fake data to plot
def generate_boxplot(ax,data,labels,mean=False):
    colorbar=['b','g','r','c','m','y','k']
    hold(True)
    
    num=0
    groupnum=0
    x_sticks=[]
    mean_dis=[]
    for group in data:
        pos=[groupnum+i for i in range(1,len(group)+1)]
        bp =boxplot(group,showfliers=False,positions=pos,widths=0.6)
        setBoxColors(bp,len(group),colorbar[:len(group)])
        groupnum+=len(group)+1
        x_sticks.append(np.median(pos))
        d=[]
        for g in group:
            d.append(np.mean(g))
        
        mean_dis.append(d)
        num+=1
    mean_dis = np.array(mean_dis).T
    pvalue=None

    if len(mean_dis)==2:
        pvalue=str(ks_2samp(mean_dis[0],mean_dis[1])[1])[:6]
    ax.set_xticklabels(np.arange(1,len(data)+1))
    ax.set_xticks(x_sticks)
    xlim(0,len(data)*len(data[0])+len(data))
    # draw temporary red and blue lines and use them to create a legend
    lines=[]
    for i in range(len(data[0])):
        if mean:
            lines.append(plot(x_sticks,mean_dis[i],colorbar[i]+'-')[0])
        else:
            lines.append(plot([1,1],colorbar[i]+'-')[0])
    legend(lines,labels,loc="upper left",prop={'size': 15})
    if not mean:
        for l in lines:
            l.set_visible(False)
        plot(x_sticks,[0]*len(data),color="gray",linestyle="--")
    return pvalue
    
    #savefig(filename)
    #show()

if (__name__=="__main__"):
    A=[[1,2,3],[1,2,3]]
    B=[[1,2,3],[1,2,3]]
    C=[[1,2,3],[1,2,3]]
    D=[[1,2,3],[1,2,3]]
    E=[[1,2,3],[1,2,3]]
    fig=figure()
    ax=plt.subplot(2,1,1)
#(ax,data,labels,mean=False)
    generate_boxplot(ax,[A,B,C,D,E],['A','B','C','d','e','f'],False)
    ax=plt.subplot(2,1,2)
    generate_boxplot(ax,[A,B,C,D,E],['A','B','C','d','e','f'],False)
    show()
