#Method to get the transmission probability spectrum from a date folder 
import os
import sys
import matplotlib.pyplot as plt
import math
import csv
import numpy as np


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


def GetConnectionErrorArray():
    index = []
    error = []
    inFile = open('transSpectraRelConnectionError.txt',"r")
    for line in inFile:
        data = line.strip().split()
        index.append(float(data[0]))
        error.append(float(data[1]))
    return index,error



#For my data where the transmission prob needs to be calculated
def getResultsNew(folderName):
    fileList = os.listdir(folderName)
    dark_spectrum = []
    transmission_spectrum = []
    tot_transmission_spectrum = []
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
    for files in fileList: 
        #Now getting transmission data and averaging
        if "transmission" in files and files.endswith(".txt"):
            long_fibre_spectrum =(parseData(folderName+"/"+files))
            tot_transmission_spectrum.append(long_fibre_spectrum)
            numReadings+=1
    transmission_spectrum = np.mean(tot_transmission_spectrum,0)
    num_array = np.subtract(transmission_spectrum,dark_spectrum)
    num_array = np.multiply(num_array,100.)
    den_array = np.subtract(reference_spectrum,dark_spectrum)
    transmission_spectrum = np.divide(num_array,den_array)
    average_aged_error = np.std(tot_transmission_spectrum,0)
    average_aged_error = np.divide(average_aged_error,np.sqrt(numReadings))
    average_aged_error = np.divide(average_aged_error,den_array)
    average_aged_error = np.multiply(average_aged_error,100.)
    return wavelengths, transmission_spectrum, average_aged_error


def getResultsOld(folderName):
    fileList = os.listdir(folderName)
    dark_spectrum = []
    transmission_spectrum = []
    tot_transmission_spectrum = []
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
        if "converted_transmission" in files and files.endswith(".txt"):
                long_fibre_spectrum =(parseConvertedData(folderName+"/"+files))
                tot_transmission_spectrum.append(long_fibre_spectrum)
                numReadings+=1
    
    transmission_spectrum = np.mean(tot_transmission_spectrum,0)
    num_array = np.subtract(transmission_spectrum,dark_spectrum)
    num_array = np.multiply(num_array,100.)
    den_array = np.subtract(reference_spectrum,dark_spectrum)
    transmission_spectrum = np.divide(num_array,den_array)
    average_aged_error = np.std(tot_transmission_spectrum,0)
    average_aged_error = np.divide(average_aged_error,np.sqrt(numReadings))
    average_aged_error = np.divide(average_aged_error,den_array)
    average_aged_error = np.multiply(average_aged_error,100.)
    
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
  connWavelengths, connErr = GetConnectionErrorArray()
  for i in range(len(errorList)):
      pass
      #errorList[i] = np.sqrt(errorList[i]**2+(connErr[i]*transmission_spectrum[i])**2)
  plt.errorbar(wavelengths,transmission_spectrum,yerr=errorList)
  plt.plot(wavelengths,transmission_spectrum)
  plt.ylabel("Transmission %")
  plt.xlabel("Wavelength")
  plt.axis([400,700,0,100])
  plt.show()

if __name__ == "__main__":
        main()
