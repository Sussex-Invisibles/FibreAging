import transmission_plot as tp
import matplotlib.pyplot as plt
import numpy
import math
import datetime
import ROOT

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

def GetConnectionErrorArray():
    index = []
    error = []
    inFile = open('transSpectraRelConnectionError.txt',"r")
    for line in inFile:
        data = line.strip().split()
        index.append(float(data[0]))
        error.append(float(data[1]))
    return index,error

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

#average between two ranges using array error and an external weighting array
#array1: data
#arrayError error on the data
#index the xvalue (in this case wavelength)
#weighging array array of all the weights
#weighting index x value of weights (in this case wavelength of tellie spectrum)
# lower adn upper upper and lower index values
def averageArrayWavelengthWeighted(array1,arrayError,index, weightingArray, weightingIndex,  lower, upper):
    average =0.0
    sumWeight=0.0
    error=0.0
    averageConnectionError = 0
    connection_wavelength, connection_error = GetConnectionErrorArray()
    for counter in range(0,len(array1)):
        entry = array1[counter]
        entryError = arrayError[counter]
        connectionError = connection_error[counter]
        #print "Entry orig: "+str(entry)
        if(index[counter]>lower and index[counter]<upper):
            closestIndex = findClosestIndex(weightingIndex,index[counter])
            weight = weightingArray[closestIndex]
            sumWeight+=weight
            average += (entry*weight)
            error += (weight*entryError)**2
            averageConnectionError += weight*entry*connectionError
    error = math.sqrt(error) 
    error /= sumWeight
    error += (averageConnectionError/sumWeight)
    print str(average)
    print str(sumWeight)
    weightedMean = average/sumWeight
    return weightedMean,error

#average between two ranges using weighted mean using only the error
def averageArrayWavelengthErrorWeighted(array1,arrayError,index, lower, upper):
    average =0.0
    sumWeight=0
    error=0
    for counter in range(0,len(array1)):
        entry = array1[counter]
        #print "Entry orig: "+str(entry)
        if(index[counter]>lower and index[counter]<upper):
            weight = 1.0/(arrayError[counter]*arrayError[counter])
            sumWeight+=weight
            average += entry*weight
       
    average/=sumWeight
    error = 1.0/sumWeight 
    error = math.sqrt(error)
    return average,error


def folderNameToDate(folderName):
    dateList = folderName.split("_")
    print dateList
    Outdate = datetime.date(int(dateList[2]),int(dateList[1]),int(dateList[0])) 
    return Outdate

#plot average transmission percentage as a function of date
def plotAverages(fileList, singleValue=False):
    connection_wavelength, connection_error = GetConnectionErrorArray()
    weightIndex, weightArray = GetWeightingArray()
    agingFactor = 2**4.72
    agingFactorError = 2**4.75-2**4.72
    averageList = []
    yErrorList = []
    xErrorList = []
    dateList = []
    agingTime = []
    average = 0
    AVerror = 0
    i = 1
    for folder in fileList:
        timediff = (folderNameToDate(folder)-folderNameToDate(fileList[0])).days
        print "ON FOLDER: "+folder
        wavelength = []
        transmission = []
        error = []
        if i<9:
            wavelength, transmission, error = tp.getResultsOld(folder)
        else:
            wavelength, transmission, error = tp.getResultsNew(folder)
        if singleValue:
            for j in range(len(wavelength)):
                if wavelength[j] == 505.62:
                    average = transmission[j]
                    connectionError = connection_error[j]
                    AVerror = math.sqrt(error[j]**2+(connection_error[j]*transmission[j])**2)
                    print str(AVerror)
        else:
            average,AVerror = averageArrayWavelengthWeighted(transmission,error,wavelength,weightArray,weightIndex,400,700)
        #average,error = averageArrayWavelengthErrorWeighted(transmission,error,wavelength,400,700)
        agingTime.append(timediff*agingFactor)
        averageList.append(average)
        yErrorList.append(AVerror)
        xErrorList.append(agingFactorError*timediff)
        i+=1
    
    #Fitting to linear polynomial
    fitWeights = []
    for iError in range(len(yErrorList)):
        fitWeights.append(1.0/math.sqrt((yErrorList[iError]**2)))
    fitParamsNoAging = numpy.polyfit(agingTime,averageList,0,w=fitWeights)
    fitParamsAging = numpy.polyfit(agingTime,averageList,1,w=fitWeights)
    polyNoAging = numpy.poly1d(fitParamsNoAging)
    polyAging = numpy.poly1d(fitParamsAging)
    chi_squared_no_aging = numpy.sum((numpy.polyval(polyNoAging, agingTime) - averageList) ** 2)
    chi_squared_aging = numpy.sum((numpy.polyval(polyAging, agingTime) - averageList) ** 2)
    reduced_chi_squared_no_aging = chi_squared_no_aging/(len(agingTime)-len(fitParamsNoAging))
    reduced_chi_squared_aging = chi_squared_aging/(len(agingTime)-len(fitParamsAging))
    print "Parameters for no aging: "+str(fitParamsNoAging)
    print "Parameters for  aging: "+str(fitParamsAging)
    print "Number of Degrees of Freedom for no aging  is: "+str(len(agingTime)-len(fitParamsNoAging))
    print "Number of Degrees of Freedom for  aging  is: "+str(len(agingTime)-len(fitParamsAging))
    print "Reduced chi squared for no aging is: "+str(reduced_chi_squared_no_aging)
    print "Reduced chi squared for  aging is: "+str(reduced_chi_squared_aging)
    print "Likelihood of fit for no aging is is: "+str(ROOT.TMath.Prob(chi_squared_no_aging,len(agingTime)-len(fitParamsNoAging)))
    print "Likelihood of fit for aging is is: "+str(ROOT.TMath.Prob(chi_squared_aging,len(agingTime)-len(fitParamsAging)))
    plt.errorbar(agingTime,averageList,yerr=yErrorList,xerr=xErrorList)
    plt.plot(agingTime,averageList)
    plt.plot(agingTime,polyNoAging(agingTime))
    plt.plot(agingTime,polyAging(agingTime))
    plt.ylabel("Average Transmission %")
    plt.xlabel("Effective number of days aged")
    #plt.xticks(numReading,fileList,rotation=45)

def plotSpectrum(fileList):
    wavelength, transmission, err = tp.getResultsNew(fileList)
    wavelengthWeight, weight = GetWeightingArray()
    low_index = 0
    high_index = 0
    for i in range(len(wavelength)):
        if wavelength[i] > 400:
            low_index = i
            break

    for i in range(len(wavelength)-1,0,-1):
        if wavelength[i] < 700:
            high_index = i
            break
    transmission = transmission[low_index:high_index]
    wavelength = wavelength[low_index:high_index]
    transmission = numpy.multiply(transmission,1.0/numpy.amax(transmission))
    plt.plot(wavelength,transmission,label=fileList)
    weight = numpy.multiply(weight,1.0/numpy.amax(weight))
    plt.plot(wavelengthWeight,weight,label="TELLIE SPECTRUM")
    plt.xlabel("Wavelength")

    plt.axis([400,700,0,1])
    plt.legend()
    plt.show()

def main():
    fileList = [ "07_04_2015" , "13_04_2015" ,"16_04_2015" ,"20_04_2015" ,"23_04_2015","27_04_2015",  "28_04_2015", "03_05_2015" , "09_06_2015" , "16_06_2015", "23_06_2015","30_06_2015","09_07_2015","14_07_2015","21_07_2015","28_07_2015","04_08_2015","19_08_2015","26_08_2015","01_09_2015","15_09_2015","22_09_2015","06_10_2015","14_10_2015","21_10_2015","27_10_2015","03_11_2015"]
    plotAverages(fileList,True)    
    #plotAverages(fileList)    
    plt.show()
    #plotSpectrum("15_09_2015")

if __name__ == "__main__":
        main()
