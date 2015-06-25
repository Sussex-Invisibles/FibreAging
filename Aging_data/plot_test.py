import transmission_plot as tp
import matplotlib.pyplot as plt

def main():
    inputFile = "07_04_2015/transmission_fibre_16.txt"
    data = tp.parseData(inputFile) 
    wavelengths = tp.parseWavelengths(inputFile)
    plt.plot(wavelengths,data)
    plt.show()

      
if __name__ == "__main__":
        main()
