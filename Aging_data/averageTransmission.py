import transmission_plot as tp
import matplotlib.pyplot as plt

#average between two ranges
def averageArray(array, index, lower, upper):
    average =0.0
    counter = 0
    numValues = 0
    for entry in array:
        if(index[counter]>lower and index[counter]<upper):
            average += entry
            numValues+=1

        counter+=1
        
    return average/numValues

#plot average transmission percentage 
def plotAverages(fileList):
    averageList = []
    numReading = []
    i = 1
    for folder in fileList:
        wavelength = []
        transmission = []
        if i<9:
            wavelength, transmission = tp.getResultsOld(folder)
        else:
            wavelength, transmission = tp.getResultsNew(folder)
        average = averageArray(transmission,wavelength,400,700)
        numReading.append(i)
        averageList.append(average)
        i+=1

    plt.plot(numReading,averageList)
    plt.ylabel("Average Transmission %")
    plt.xlabel("Reading")
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
    fileList = [ "07_04_2015" , "13_04_2015" ,"16_04_2015" ,"20_04_2015" ,"23_04_2015","27_04_2015",  "28_04_2015", "03_05_2015" , "09_06_2015" , "16_06_2015", "23_06_2015"]
    plotSpectrum(fileList)    

if __name__ == "__main__":
        main()
