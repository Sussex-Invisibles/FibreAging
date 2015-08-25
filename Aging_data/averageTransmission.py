import transmission_plot as tp
import matplotlib.pyplot as plt
import math
import datetime

#Method to get the weighting array
def GetWeightingArray():
    index = []
    weight = []
    inFile = open("wavelengthDist.txt","r")
    for line in inFile:
        data = line.strip().split()
        index.append(float(data[0]))
        weight.append(float(data[1]))
    return index,weight

#Method to find index of array corresponding to entry closest to value
def findClosestIndex(array,number):
    closest = 10000
    indexClosest = -1000
    i = 0
    for num in array:
        if abs(num-number) < closest:
            closest = abs(num-number)
            indexClosest = i
        i+=1
    return indexClosest

#average between two ranges
def averageArrayWavelengthWeighted(array1,index, weightingArray, weightingIndex,  lower, upper):
    average =0.0
    sumWeight=0
    error=0
    for counter in range(0,len(array1)):
        entry = array1[counter]
        #print "Entry orig: "+str(entry)
        if(index[counter]>lower and index[counter]<upper):
            closestIndex = findClosestIndex(weightingIndex,index[counter])
            weight = weightingArray[closestIndex]
            sumWeight+=weight
            average += entry*weight
        
    weightedMean =  average/sumWeight
    for counter in range(0,len(array1)):
        entry2 = array1[counter]
        if(index[counter]>lower and index[counter]<upper):
            closestIndex = findClosestIndex(weightingIndex,index[counter])
            weight = weightingArray[closestIndex]
            error += weight*((entry2-weightedMean)**2)

    error/=sumWeight
    error = math.sqrt(error)
    return weightedMean,error

def folderNameToDate(folderName):
    dateList = folderName.split("_")
    print dateList
    Outdate = datetime.date(int(dateList[2]),int(dateList[1]),int(dateList[0])) 
    return Outdate

#plot average transmission percentage as a function of date
def plotAverages(fileList):
    weightIndex, weightArray = GetWeightingArray()
    averageList = []
    errorList = []
    dateList = []
    numReading = []
    i = 1
    for folder in fileList:
        timediff = (folderNameToDate(folder)-folderNameToDate(fileList[0])).days
        print "ON FOLDER: "+folder
        wavelength = []
        transmission = []
        if i<9:
            wavelength, transmission = tp.getResultsOld(folder)
        else:
            wavelength, transmission = tp.getResultsNew(folder)
        average,error = averageArrayWavelengthWeighted(transmission,wavelength,weightArray,weightIndex,400,700)
        numReading.append(timediff)
        averageList.append(average)
        errorList.append(error)
        i+=1
     
    plt.errorbar(numReading,averageList,yerr=errorList)
    plt.plot(numReading,averageList)
    plt.ylabel("Average Transmission %")
    plt.xlabel("Reading")
    plt.xticks(numReading,fileList,rotation=45)
    plt.show()

def plotSpectrum(fileList):
    i = 1
    for folder in fileList:
        if i<9:
            wavelength, transmission = tp.getResultsOld(folder)
        else:
            wavelength, transmission = tp.getResultsNew(folder)
        i+=1
        plt.plot(wavelength,transmission,label=folder)
        plt.ylabel("Transmission %")
        plt.xlabel("Wavelength")

    plt.axis([400,700,0,40])
    plt.legend()
    plt.show()

def main():
    fileList = [ "07_04_2015" , "13_04_2015" ,"16_04_2015" ,"20_04_2015" ,"23_04_2015","27_04_2015",  "28_04_2015", "03_05_2015" , "09_06_2015" , "16_06_2015", "23_06_2015","30_06_2015","09_07_2015","14_07_2015","21_07_2015","28_07_2015","04_08_2015","11_08_2015","19_08_2015"]
    plotAverages(fileList)    

if __name__ == "__main__":
        main()
