#Method to get the transmission probability spectrum from a date folder 
import os
import sys
import matplotlib.pyplot as plt
import math

sigma_ref = 68.54
sigma_aged = 39.44
sigma_dark = 1.61

#Method to get the error on the transmission from the errors on the various spectrums
def calcTransmissionUncertainty(referenceSpectrum, darkSpectrum, transmissionFibreSpectrum):
    transmission_uncertainty = [0] * len(referenceSpectrum)
    for i in range(len(referenceSpectrum)):
        #first term
        if referenceSpectrum[i] == darkSpectrum[i]:
            continue
        else:
            transmission_uncertainty[i] += ((sigma_aged/(referenceSpectrum[i]-darkSpectrum[i]))**2)
            #second term
            transmission_uncertainty[i] += (((darkSpectrum[i]-transmissionFibreSpectrum[i])*sigma_ref)/((referenceSpectrum[i]-darkSpectrum[i])**2))**2
            #third term
            transmission_uncertainty[i] += (((transmissionFibreSpectrum[i]-darkSpectrum[i])*sigma_dark)/((referenceSpectrum[i]-darkSpectrum[i])**2))**2
            #sqrt
            transmission_uncertainty[i] = math.sqrt(transmission_uncertainty[i])*100
    return transmission_uncertainty

#For my data where the transmission prob needs to be calculated
def getResultsNew(folderName):
    fileList = os.listdir(folderName)
    dark_spectrum = []
    transmission_spectrum = []
    reference_spectrum = []
    average_aged_error  = []
    sumWeights = []
    wavelengths = []
    
    #Getting wavelength and dark and reference data
    numReadings = 0
    for files in fileList:
        if "dark" in files and files.endswith(".txt"):
            wavelengths = (parseWavelengths(folderName+"/"+files))
            dark_spectrum = (parseData(folderName+"/"+files))
        
        if "reference" in files and files.endswith(".txt"):
            reference_spectrum =parseData(folderName+"/"+files)
    sumWeights = [0] * len(wavelengths)
    transmission_spectrum = [0]* len(wavelengths)
    for files in fileList: 
        #Now getting transmission data and averaging
        if "transmission" in files and files.endswith(".txt"):
            if numReadings == 0:
                long_fibre_spectrum =(parseData(folderName+"/"+files))
                transmission_uncertainty = calcTransmissionUncertainty(reference_spectrum,dark_spectrum,long_fibre_spectrum)
                for i in range(len(long_fibre_spectrum)):
                    #Making sure no division by 0
                    if reference_spectrum[i] != 0 and transmission_uncertainty[i] != 0:
                        transmission_value = (long_fibre_spectrum[i]-dark_spectrum[i])*100/(reference_spectrum[i]-dark_spectrum[i])
                        transmission_spectrum[i] +=(transmission_value/(transmission_uncertainty[i]**2))
                        sumWeights[i] +=(1.0/(transmission_uncertainty[i]**2))
            else:
                long_fibre_spectrum  =(parseData(folderName+"/"+files))
                transmission_uncertainty = calcTransmissionUncertainty(reference_spectrum,dark_spectrum,long_fibre_spectrum)
                for i in range(len(long_fibre_spectrum)):
                    if reference_spectrum[i] != 0 and transmission_uncertainty[i] != 0:
                        transmission_value = (long_fibre_spectrum[i]-dark_spectrum[i])/(reference_spectrum[i]-dark_spectrum[i])*100
                        transmission_spectrum[i] += (transmission_value/(transmission_uncertainty[i]**2))
                        sumWeights[i] += (1.0/(transmission_uncertainty[i]**2))
            
            numReadings+=1
    
    for i in range(len(wavelengths)):
        if sumWeights[i] != 0:
            transmission_spectrum[i] /= sumWeights[i]
            #Multiply by 100 to get percentage
            average_aged_error.append(math.sqrt(1.0/sumWeights[i]))
        else:
            average_aged_error.append(100)
            transmission_spectrum[i] = 0
    return wavelengths, transmission_spectrum, average_aged_error


def getResultsOld(folderName):
    fileList = os.listdir(folderName)
    dark_spectrum = []
    transmission_spectrum = []
    reference_spectrum = []
    average_aged_error  = []
    sumWeights = []
    wavelengths = []
    
    #Getting wavelength and dark and reference data
    numReadings = 0
    for files in fileList:
        if "dark" in files and files.endswith(".txt"):
            wavelengths = (parseWavelengths(folderName+"/"+files))
            dark_spectrum = (parseData(folderName+"/"+files))
        
        if "reference" in files and files.endswith(".txt"):
            reference_spectrum =parseData(folderName+"/"+files)
    sumWeights = [0] * len(wavelengths)
    transmission_spectrum = [0]* len(wavelengths)
    for files in fileList: 
        #Now getting transmission data and averaging
        if "converted_transmission" in files and files.endswith(".txt"):
            if numReadings == 0:
                long_fibre_spectrum =(parseConvertedData(folderName+"/"+files))
                transmission_uncertainty = calcTransmissionUncertainty(reference_spectrum,dark_spectrum,long_fibre_spectrum)
                for i in range(len(long_fibre_spectrum)):
                    #Making sure no division by 0
                    if reference_spectrum[i] != 0 and transmission_uncertainty[i] != 0:
                        transmission_value = (long_fibre_spectrum[i]-dark_spectrum[i])*100/(reference_spectrum[i]-dark_spectrum[i])
                        transmission_spectrum[i] +=(transmission_value/(transmission_uncertainty[i]**2))
                        sumWeights[i] +=(1.0/(transmission_uncertainty[i]**2))
            else:
                long_fibre_spectrum  =(parseConvertedData(folderName+"/"+files))
                transmission_uncertainty = calcTransmissionUncertainty(reference_spectrum,dark_spectrum,long_fibre_spectrum)
                for i in range(len(long_fibre_spectrum)):
                    if reference_spectrum[i] != 0 and transmission_uncertainty[i] != 0:
                        transmission_value = (long_fibre_spectrum[i]-dark_spectrum[i])/(reference_spectrum[i]-dark_spectrum[i])*100
                        transmission_spectrum[i] += (transmission_value/(transmission_uncertainty[i]**2))
                        sumWeights[i] += (1.0/(transmission_uncertainty[i]**2))
            
            numReadings+=1
    
    for i in range(len(wavelengths)):
        if sumWeights[i] != 0:
            transmission_spectrum[i] /= sumWeights[i]
            #Multiply by 100 to get percentage
            average_aged_error.append(math.sqrt(1.0/sumWeights[i]))
        else:
            average_aged_error.append(100)
            transmission_spectrum[i] = 0
    return wavelengths, transmission_spectrum, average_aged_error


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

def parseConvertedData(inputFile):
    inputData = open(inputFile,"r")
    output = [] 
    for line in inputData:
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
  wavelengths,transmission_spectrum,errorList = getResultsNew(sys.argv[1])
  plt.errorbar(wavelengths,transmission_spectrum,yerr=errorList)
  plt.plot(wavelengths,transmission_spectrum)
  plt.ylabel("Transmission %")
  plt.xlabel("Wavelength")
  plt.axis([400,700,0,100])
  plt.show()

if __name__ == "__main__":
        main()
