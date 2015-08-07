#Method to get the transmission probability spectrum from a date folder 
import os
import sys
import matplotlib.pyplot as plt

#For my data where the transmission prob needs to be calculated
def getResultsNew(folderName):
    fileList = os.listdir(folderName)
    dark_spectrum = []
    transmission_spectrum = []
    reference_spectrum = []
    average_aged_spectrum = []
    wavelengths = []
    
    #Getting wavelength and dark and reference data
    numReadings = 0
    for files in fileList:
        if "dark" in files and files.endswith(".txt"):
            wavelengths = (parseWavelengths(folderName+"/"+files))
            dark_spectrum = (parseData(folderName+"/"+files))
        
        if "reference" in files and files.endswith(".txt"):
            reference_spectrum =parseData(folderName+"/"+files)
            

        #Now getting transmission data and averaging
        if "transmission" in files and files.endswith(".txt"):
            if numReadings == 0:
                average_aged_spectrum =(parseData(folderName+"/"+files))
            else:
                data = parseData(folderName+"/"+files)
                for i in range(len(data)):
                    average_aged_spectrum[i]+=data[i]

            numReadings+=1

    #Dividing to get the average 
    for i in range(len(average_aged_spectrum)):
       average_aged_spectrum[i] = average_aged_spectrum[i]/numReadings
    print "Length of aged: "+str(len(average_aged_spectrum))
    print "Length of dark: "+str(len(dark_spectrum))
    print "Length of wavelenght: "+str(len(wavelengths))
    for i in range(len(wavelengths)):
        num = (average_aged_spectrum[i]-dark_spectrum[i])*100
        den = (reference_spectrum[i]-dark_spectrum[i])
        if den == 0:
            transmission_spectrum.append(0)
        else:
            transmission_spectrum.append(num/den)

    return wavelengths, transmission_spectrum


#For hebbas data where the processor calculates the transmission percentage
def getResultsOld(folderName):
    fileList = os.listdir(folderName)
    dark_spectrum = []
    transmission_spectrum = []
    reference_spectrum = []
    average_aged_spectrum = []
    wavelengths = []
    
    #Getting wavelength and dark and reference data
    numReadings = 0
    for files in fileList:
        if "dark" in files and files.endswith(".txt"):
            wavelengths = (parseWavelengths(folderName+"/"+files))
            dark_spectrum = (parseData(folderName+"/"+files))
        
        if "reference" in files and files.endswith(".txt"):
            reference_spectrum =parseData(folderName+"/"+files)
            

        #Now getting transmission data and averaging
        if "transmission" in files and files.endswith(".txt"):
            if numReadings == 0:
                average_aged_spectrum =(parseData(folderName+"/"+files))
            else:
                data = parseData(folderName+"/"+files)
                for i in range(len(data)):
                    average_aged_spectrum[i]+=data[i]

            numReadings+=1

    #Dividing to get the average 
    for i in range(len(average_aged_spectrum)):
       average_aged_spectrum[i] = average_aged_spectrum[i]/numReadings
    

    return wavelengths, average_aged_spectrum



def parseData(inputFile):
    inputData = open(inputFile,"r")
    output = [] 
    for line in inputData:
        if line.strip() == ">>>>>Begin Processed Spectral Data<<<<<" or line.strip() == ">>>>>Begin Spectral Data<<<<<" :
            break
    
    for line in inputData:
        if line.strip() == ">>>>>End Processed Spectral Data<<<<<" or line.strip() == ">>>>>End Spectral Data<<<<<":
            break
        data = line.strip().split()
        output.append(float(data[1]))

    return output

def parseWavelengths(inputFile):
    inputData = open(inputFile,"r")
    output = [] 
    for line in inputData:
        if line.strip() == ">>>>>Begin Processed Spectral Data<<<<<" or line.strip() == ">>>>>Begin Spectral Data<<<<<":
            break
    
    for line in inputData:
        if line.strip() == ">>>>>End Processed Spectral Data<<<<<" or line.strip() == ">>>>>End Spectral Data<<<<<":
            break
        data = line.strip().split()
        if len(output)>1 and output[-1]==float(data[0]) :
            print "Possible Staturation of Spectrometer has occured in ",inputFile
        output.append(float(data[0]))

    return output


def main():
  wavelengths,transmission_spectrum = getResultsNew(sys.argv[1])
  plt.plot(wavelengths,transmission_spectrum)
  plt.ylabel("Transmission %")
  plt.xlabel("Wavelength")
  plt.axis([400,700,0,100])
  plt.show()

if __name__ == "__main__":
        main()
