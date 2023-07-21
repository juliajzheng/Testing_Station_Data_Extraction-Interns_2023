import math
from pprint import pprint
from turtle import color
import numpy as np
import pandas as pd
import time
import sys
import os
from glob import glob
import csv
import matplotlib.pyplot as plt
import scipy

from scipy.optimize import leastsq
from scipy.optimize import curve_fit


def Curve_Fitting_tst(folder_path, Plot_Data = False):
  PATH = folder_path
  EXT = "*.csv"
  all_csv_files = [file
                  for path, subdir, files in os.walk(PATH)
                  for file in glob(os.path.join(path, EXT))]

  fig, axs = plt.subplots(1, 3, figsize=(15, 5))
  ''' Channel 1 output result'''
  Legend_lables = list()

  for file_path in all_csv_files:                 # Finding the path to CSV file
    if 'Pandas' in file_path:
      df = pd.read_csv(file_path)#, header=None)    
      # axs[0].plot(df['Wavelength'], df['Laser-Power(dB)'], color = 'green')
      axs[0].plot(df['Wavelength'], df['Channel-2'])
      legend_val = df['Device-ID'][0]
      Legend_lables= np.append(Legend_lables, legend_val)

  axs[0].set_title('Channel-1')
  axs[0].legend(Legend_lables, loc='center left', bbox_to_anchor=(1, 0.5),fontsize = 7)
  axs[0].set_ylim([-55, 10])#type: ignore
  axs[0].set_ylabel("Transmission (dB)")
  axs[0].set_xlabel("Wavelength (nm)")

  '''Adding approximation to the file'''

  
  for file_path in all_csv_files:                 # Finding the path to CSV file
    if 'Pandas' in file_path:
      df = pd.read_csv(file_path)#, header=None)    
      xData = df['Wavelength']
      yData = df['Channel-2']
      xFilterData, yFilterData = Filter_Data(xData= xData, yData= yData, xStart=1535, xStop= 1560)
      xFilterData = xFilterData.to_numpy()
      yFilterData = yFilterData.to_numpy()
      # print((xFilterData))
      # Lor_model = LorentzianModel()
      # params = Lor_model.guess(yFilterData, x=xFilterData)
      # result = Lor_model.fit(yFilterData, params=params, x= xFilterData)
      # # result.plot_fit()
      Curve_Fit_Loren = Loren_Model_Channel2(xFilterData, yFilterData)

      # axs[1].plot(xFilterData, yFilterData)
      axs[1].plot(xFilterData, Curve_Fit_Loren)
      # print(type(result))
      legend_val = df['Device-ID'][0]
      Legend_lables= np.append(Legend_lables, legend_val)

  axs[1].set_title('Channel-1')
  axs[1].legend(Legend_lables, loc='center left', bbox_to_anchor=(1, 0.5),fontsize = 7)
  # axs[1].set_ylim([-55, 10])
  axs[1].set_ylabel("Transmission (dB)")
  axs[1].set_xlabel("Wavelength (nm)")

  # fig.tight_layout(pad=4.0)
  plt.show()

  return()

def Loren_Model_Channel1 (xData, yData):
  
  # yData = min(yData)/yData
  generalWidth = 1

  yDataLoc = yData
  startValues = [ max( yData ) ]
  counter = 0

  min_dB = list()
  min_lambda = list()
  while max( yDataLoc ) - min( yDataLoc ) > 20:
      counter += 1
      if counter > 10: ### max 20 peak...emergency break to avoid infinite loop
          break
      minP = np.argmin( yDataLoc ) # index minimum value
      minY = yData[ minP ] # min value in dB
      min_dB.append(minY)
      x0 = xData[ minP ] # min lambda value 
      min_lambda.append(x0)
      startValues += [ x0, minY - max( yDataLoc ), generalWidth ]
      popt, ier = leastsq(res_multi_lorentz, startValues, args=( xData, yData ) )
      yDataLoc = [ y - multi_lorentz( x, popt ) for x,y in zip( xData, yData ) ]

  try :
    print(popt)#type: ignore
    testData = [ multi_lorentz(x, popt ) for x in xData ]#type: ignore
    return(testData, min_dB, min_lambda)
  except UnboundLocalError :
    print("breaking with exception")
    return()

def Loren_Model_Channel2 (xData, yData):
  
  # yData = min(yData)/yData
  generalWidth = 1

  yDataLoc = yData
  startValues = [ max( yData ) ]
  counter = 0

  min_dB = list()
  min_lambda = list()
  while max( yDataLoc ) - min( yDataLoc ) > 13:
      counter += 1
      if counter > 10: ### max 20 peak...emergency break to avoid infinite loop
          break
      minP = np.argmin( yDataLoc )
      minY = yData[ minP ]
      min_dB.append(minY)
      x0 = xData[ minP ]
      min_lambda.append(x0)
      startValues += [ x0, minY - max( yDataLoc ), generalWidth ]
      popt, ier = leastsq(res_multi_lorentz, startValues, args=( xData, yData ) )
      yDataLoc = [ y - multi_lorentz( x, popt ) for x,y in zip( xData, yData ) ]

  try :
    # print(popt)#type: ignore
    testData = [ multi_lorentz(x, popt ) for x in xData ]#type: ignore
    return(testData, min_dB, min_lambda)
  except UnboundLocalError :
    print("breaking with exception")
    return()

def lorentzian( x, x0, a, gam ):
    return a * gam**2 / ( gam**2 + ( x - x0 )**2)

def multi_lorentz( x, params ):
    off = params[0]
    paramsRest = params[1:]
    assert not ( len( paramsRest ) % 3 )
    return off + sum( [ lorentzian( x, *paramsRest[ i : i+3 ] ) for i in range( 0, len( paramsRest ), 3 ) ] )

def res_multi_lorentz( params, xData, yData ):
    diff = [ multi_lorentz( x, params ) - y for x, y in zip( xData, yData ) ]
    return diff

def Filter_Data (xData, yData, xStart, xStop):

  test_start = xData[xData == xStart].index[0]
  test_stop = xData[xData == xStop].index[0]+1

  xFilterData = xData[test_start:test_stop]
  yFilterData = yData[test_start:test_stop]

  return(xFilterData, yFilterData)

if __name__ == '__main__':
  Curve_Fitting_tst(folder_path = 'test4', Plot_Data = True)