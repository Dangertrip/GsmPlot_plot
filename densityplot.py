#This is the code segment of density plot.
def plot(args):
    '''
        This segment are directly copied from original program. Although Variables are kept the same names, I will explain the functionality for every pieces.
    '''
    
    #File names downloaded from NCBI. We will use it for labels in our figure.
    names = list(map(lambda x:x.strip(),inputfilename.strip().split(' ')))
    #blocks are numbers of data points in one density plot.
    blocks = (int(after)+int(before)+int(scaleregion))//int(binsize)
    #Plot settings
    fig=plt.figure(figsize=(60,13))
    titles=['SpecificRegion','CGI','Genebody']
    colours = ['b','g','r','c','m','y','k']
    markers=['*','o','v','^','<','>','1','2','3','4']
    #Simlified file names as labels
    headers = list(map(lambda x:x[x.rfind('/')+1:],names))
    order=0  #figure index to generate 3 different figures.
    for ofn in ofn_arr:
        ansf,region_mean,region_title = format_gz(ofn[:-3],len(names),methmark in methnamedic,hmcmark in methnamedic,blocks)  #Get data from computing results
        y = np.array(ansf)
        ax = plt.subplot(1,3,order+1)
        plt.title(titles[order],fontsize=30)
        file_zscore(ofn[:-3])

        #This part is to generate necessary files for boxplot
        tmp_header = ['']
        tmp_header.extend(headers)
        region_m,region_t=['\t'.join(tmp_header)+'\n'],['\t'.join(tmp_header)+'\n']
        for i in range(len(region_mean)):
            rt_str = list(map(lambda x:str(x),region_title[i]))
            rt = '_'.join(rt_str[:4])
            region_m.append('\t'.join(list(map(lambda x:str(x),region_mean[i]))))
            region_m[-1] = rt+'\t'+region_m[-1]+'\n'
            region_t.append('\t'.join(rt_str)+'\n')
        with open(titles[order]+'.regionmean.txt','w') as f:
            f.writelines(region_m)
        with open(titles[order]+'.title.txt','w') as f:
            f.writelines(region_t)
        order+=1

        x = np.arange(blocks)
        #In case we have multiple background values in different scales, we have two y-axis. One for data in 0-1, the other for other scales.
        if bg_num>0: # bg_num means how many background signals are selected. 
            right_axis = ax.twinx() #another y axis
            max_right=np.max(y[len(y)-bg_num:len(y)])*1.3
            right_axis.set_ylim(0,max_right)
            right_axis.set_ylabel('Signal',fontsize=22,color='brown')
        plt.xlim(0, len(y[0]))
        #Higher limitation is set to avoid legend blocking.
        ax.set_ylim(0,np.max(y[0:len(y)-bg_num])*1.3)
        for i in range(len(y)-bg_num):
            tempy=y[i]
            if np.max(tempy)<0: tempy+=1
            ax.plot(x, tempy, colours[i], linewidth=1,marker=markers[i], label=names[i][names[i].rfind('/')+1:])
        if bg_num>0:
            for i in range(len(y)-bg_num,len(y)):
                right_axis.plot(x,y[i],'brown', linewidth=1,marker=markers[i], label=names[i][names[i].rfind('/')+1:])
                ax.plot([-1000],[-1000],'brown', linewidth=1,marker=markers[i], label=names[i][names[i].rfind('/')+1:])
        ax.legend(loc="upper left",prop={'size': 24})
        if bg_num>0: 
            right_axis.yaxis.set_tick_params(labelsize=22)
        ax.set_xticks([0,int(before)/int(binsize),(int(before)+int(scaleregion))/int(binsize),(int(before)+int(scaleregion)+int(after))/int(binsize)])
        ax.set_xticklabels(['-' + str(int(before) / 1000) + ' kb', 'Start', 'END', str(int(after) / 1000) + ' kb'])
        ax.yaxis.set_tick_params(labelsize=22)
        ax.xaxis.set_tick_params(labelsize=22)
        plt.xlabel('Regions Relative Positions', fontsize=22)
        ax.set_ylabel('Data Signal', fontsize=22)
    fig.savefig(sid + ".png")
    
    filenames=[]
    for f in ofn_arr:
        filenames.append(f[:-3]+'_z')
    bp_generate(['Selected Region','CGI','Genebody'],filenames,len(names),blocks,list(map(lambda x:x[x.rfind('/')+1:],names)),'boxplot.all.png',False) 
    
    


