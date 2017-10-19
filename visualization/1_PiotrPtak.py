#   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@   #
#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    #
#       PYTHON VISUALIZATION EXERCISE        #
#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    #
#         author: Piotr Ptak (poe)           #
#   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    #
#   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@   #

import matplotlib.pyplot as plt
import csv

#   ~~~~~~~~~~~ DEFINE ~~~~~~~~~~~~  #
dataFiles = ['rsel.csv', 'cel-rs.csv', '2cel-rs.csv', 'cel.csv', '2cel.csv']
labelNames = ['1-Evol-RS', '1-Coev-RS', '2-Coev-RS', '1-Coev', '2-Coev']
labelsPokolenie = ['0', '40', '80', '120', '160', '200']
colors = [ '#3f0aff', '#339f33', '#ff0a0a', '#2e2e33', '#cd67db']               #in plot, every algorithm is represented by a different color on a graph.
markers = ['o', 'v', 'D', 's', 'd']
boxValues = []


#get actual x values
#since they are the same for every algorithm, this function will be called only once
def getXValues(filePath):
    content = []
    with open(filePath, 'r') as csvfile:
        next(csvfile)                       #ignore header line
        plots = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC, delimiter=',')    #each argument is seperated by comma

        #X argument is represented by the number of games played
        #to get the desired interval (0-500), I'm deviding second column by 1000
        for row in plots:
            content.append(int(row[1]) / 1000)
    return content


#get y values, which is different for every algorithm
#every algorithm was run 32 times, so in order to calculate the average value, this function sums all the values and divides the sum by 32
#since this function receives data without X parameter in it, we don't have to cut it before processing it
def getYValues(content, correction):
    avg = []
    for i in content:
        sum = 0
        for j in i[:]:
            # add up the current value to the sum
            sum += float(j)

        #since we want to show the percentage values rather than floating points values, we multiply it by 100
        avg.append(sum/32  * correction)        #32 is a number of arguments in a row (excluding x axis arguments)
    return avg

#processing data for the boxplot
def getBoxValues(content, correction):
    result = []

    #the last column is the one we're searching for (it has and index of -1)
    for i in content[-1][:]:
        #we want to show percentage values, so we have to multiply by 100
        result.append(float(i) * correction)

    return result


#function to get the actual input data (reading from files)
def loadDataFromFile(filePath):
    content = []
    with open(filePath, 'r') as csvfile:
        next(csvfile)                       #ignore header line
        plots = csv.reader(csvfile, quoting=csv.QUOTE_NONNUMERIC, delimiter=',')
        for row in plots:
            #first element is a generation, so we have to ignore it.
            #second element is the number of games played, so we ignore it as well
            #we assign next values to Y arguments
            content.append(row[2:])
    return content

def main():
    #   ~~~~~~~~~~~ INPUT  ~~~~~~~~~~~~  #
    data = []
    xValues = getXValues(dataFiles[0])
    for i in range(0, 5):
        data.append(loadDataFromFile(dataFiles[i]))
    boxValues = []
    for i in range(0, 5):
        boxValues.append(getBoxValues(data[i], 100))


    #initialize plots
    visualisation = plt.figure(figsize=(7.5, 5.5))
    plot1 = visualisation.add_subplot(1, 2, 1)      #left graph
    plot2 = visualisation.add_subplot(1, 2, 2)     #right graph

    #   ~~~~~~~~~~~ PLOT 1  ~~~~~~~~~~~~  #
    for i in range(0, 5):
        plot1.plot(xValues, getYValues(data[i], 100), label=labelNames[i], color=colors[i], marker=markers[i], markevery=25, linewidth=1.0)

    #labels
    plot1.set_xlabel("Rozegranych gier (x1000)")    #(0-500)
    plot1.set_ylabel("Odsetek wygranych gier [%]")  #(0-100)

    #now we have to apply those intervals as limits to our plot
    plot1.set_xlim(0, 500)
    plot1.set_ylim(60, 100)

    #top labels and title
    top = plot1.twiny()                                #this creates so called twin axes which shares the y axis with original plot. This way we can actually have two sets of parameters on the graph
    top.set_xticklabels(labelsPokolenie)             #these are hardcoded values for the top label (sorry for the hardcoding tho.)
    top.set_xlabel("Pokolenie")                      #(0-200)

    #additional customization
    plot1.legend(loc='lower right')                #where do we want to put our legend (in relation to the figure)
    plot1.grid(alpha=0.5, linestyle='dashed')


    #   ~~~~~~~~~~~ PLOT 2 (BOXPLOT)  ~~~~~~~~~~~~  #
    plot2.boxplot(boxValues, notch=True, showmeans=True, boxprops=dict(color=colors[0]), meanprops=dict(marker='o', markeredgecolor='black', markerfacecolor='blue'), whiskerprops=dict(linestyle='dashed', color='blue'), flierprops=dict(marker='+', markeredgecolor='blue'))
    plot2.set_ylim(60, 100)

    #customization
    plot2.set_xticklabels(labelNames, rotation=20)
    plot2.grid(alpha=0.5, linestyle='dashed')
    plot2.yaxis.tick_right()

    plt.savefig('myplot.pdf')
    plt.close()

if __name__ == '__main__':
    main()
