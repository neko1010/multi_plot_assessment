import matplotlib.ticker as mticker
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

import numpy as np
import math
import scipy.stats

##CROWN AREA SCATTERPLOTS WITH 1:1 LINE (LOG/LOG)

##h2o
#treefile = open("C:\\Users\\nkolarik\\Desktop\\thesis\\data\\field_validation2018\\tree\\tree_insitu_h2o.csv", 'r')
#shrubfile = open("C:\\Users\\nkolarik\\Desktop\\thesis\\data\\field_validation2018\\shrub\\shrub_insitu_h2o.csv", 'r')
#grassfile = open("C:\\Users\\nkolarik\\Desktop\\thesis\\data\\field_validation2018\\grass\\grass_insitu_h2o.csv", 'r')

##dalponte
treefile = open("C:\\Users\\nkolarik\\Desktop\\thesis\\data\\field_validation2018\\tree\\tree_insitu_itc.csv", 'r')
shrubfile = open("C:\\Users\\nkolarik\\Desktop\\thesis\\data\\field_validation2018\\shrub\\shrub_insitu_itc.csv", 'r')
grassfile = open("C:\\Users\\nkolarik\\Desktop\\thesis\\data\\field_validation2018\\grass\\grass_insitu_itc.csv", 'r')


tree_data = np.genfromtxt(treefile, delimiter = ',')
shrub_data = np.genfromtxt(shrubfile, delimiter = ',')
grass_data = np.genfromtxt(grassfile, delimiter = ',')


##establishing areas (column of data file)
area = 20
titles = ["RGB", "Green", "Red", "Red Edge", "NIR"]
subplots = [321, 322, 323, 324, 325]
colors = ['b', 'g', 'r', 'magenta', 'purple']
##h2o letters
#letters = ['a', 'b', 'c', 'd', 'e']
## dalponte letters
letters = ['f', 'g', 'h', 'i', 'j']


x_tree = tree_data[1:, 16]
x_shrub = shrub_data[1:, 16]
x_grass = grass_data[1:, 16]

x1 = y1 = range(0,3000)


for i in range(len(subplots)):

    y_tree = tree_data[1:, area]
    y_shrub = shrub_data[1:, area]
    y_grass = grass_data[1:, area]

    x = list(x_tree) + list(x_shrub) + list(x_grass)
    y = list(y_tree) + list(y_shrub) + list(y_grass)

    ##subplots (# of rows, # of columns, 1 - (rows * columns))
    plt.subplot(subplots[i])
    #plt.scatter(x,y)
    plt.scatter(x_tree, y_tree, marker = '.', color = colors[i])
    plt.scatter(x_shrub, y_shrub, marker = 'x', color = colors[i])
    plt.scatter(x_grass, y_grass, marker = '2', color = colors[i])
    plt.title(titles[i])
    plt.xlabel("Field Measurement")
    plt.ylabel("Estimate")

    ##log scale for areas
    plt.yscale('log')
    plt.xscale('log')
    plt.ylim([10**-1.5, 10**3.5])

    #https://stackoverflow.com/questions/49750107/how-to-remove-scientific-notation-on-a-matplotlib-log-log-plot
    ax=plt.gca()

    ax.set_xscale('log')
    ax.set_yscale('log')

    ax.xaxis.set_major_formatter(mticker.ScalarFormatter())
    ax.yaxis.set_major_formatter(mticker.ScalarFormatter())

    ##setting axes - 463.4 is largest observed; 590 is largest predicted for dalponte, 2953 for watershed! WOWZA
    #plt.axis([0,maxval,0,maxval])
    #plt.axis(0,3000, 0, 3000)

    ## abline hack
    plt.plot(x1,y1, color = '0.5')

    xlist = []
    ylist = []
    zipped = zip(x, y)
    for pair in zipped:
        ## checking for nan vals in estimates
        if np.isnan(pair[1]) == 0:
            xlist.append(pair[0])
            ylist.append(pair[1])
    ##Statistical analysis
    absresiduals = []
    #residuals = []
    res_sq = []
    for j in range(0, len(xlist)):
        diff = ylist[j] - xlist[j]

        absresiduals.append(abs(diff))

    ## Squaring residuals- REMOVED PER DR STARDUST!
    #for resid in residuals:
    #	res_sq.append(resid**2)


    sprmn_r, pval = (scipy.stats.mstats.spearmanr(xlist, ylist))
    #rmse =  math.sqrt(sum(res_sq)/ (len(xlist)-1))
    n = len(absresiduals)
    mae = (sum(absresiduals))/ n
    ## adding txt to plots

    plt.annotate("MAE = "+ str(round(mae, 2)), xy = (175, 0.1)) ## for h2o plot only
    #plt.annotate("MAE = "+ str(round(mae, 2)), xy = (325, 0.1))
    plt.annotate("p = " + str(round(float(pval),2)), xy = (625, 0.3))
    plt.annotate("r = " + str(round(sprmn_r, 2)), xy = (625, 0.75))
    plt.annotate("n = " + str(n), xy = (625, 2))
    plt.annotate(s = letters[i], xy = (1, 1000), fontweight = 'bold')
    #plt.annotate(s = "f", xy = (1,26), fontweight = 'bold')

    area += 3

## legend
grass = mlines.Line2D([], [], color = 'black', marker = '2', linestyle = 'None',
        markersize = 10, label = 'Grass dominated')


shrub = mlines.Line2D([], [], color = 'black', marker = 'x', linestyle = 'None',
        markersize = 10, label = 'Shrub dominated')

tree = mlines.Line2D([], [], color = 'black', marker = '.', linestyle = 'None',
        markersize = 10, label = 'Tree dominated')

plt.legend( handles = [grass, shrub, tree], loc = 2, bbox_to_anchor = (1.25, 0.75))
            #bbox_transform = plt.gcf().transFigure )


plt.show()
treefile.close()
shrubfile.close()
grassfile.close()

#top=0.954,
#bottom=0.075,
#left=0.08,
#right=0.969,
#hspace=0.453,
#wspace=0.231
