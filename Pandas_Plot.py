from cProfile import label
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

def Plot_Pandas (folder_path, extension):
  PATH = folder_path
  EXT = extension
  all_csv_files = [file
                  for path, subdir, files in os.walk(PATH)
                  for file in glob(os.path.join(path, EXT))]

  fig, axs = plt.subplots(1, 3, figsize=(15, 5))
  ''' Channel 1 output result'''
  Legend_lables = list()
  for file_path in all_csv_files:                 # Finding the path to CSV file
    if 'Pandas' in file_path:
      df = pd.read_csv(file_path)#, header=None)    
      axs[0].plot(df['Wavelength'], df['Channel-1'])
      legend_val = df['Device-ID'][0]
      true_legend = legend_val.split('_')
      chart_title = true_legend[0]
      true_legend= '_'.join([true_legend[1],true_legend[2]])
      Legend_lables= np.append(Legend_lables, true_legend)

  axs[0].set_title(chart_title+'--Channel-1')
  axs[0].legend(Legend_lables)
  axs[0].set_ylim([-55, -10])
  axs[0].set_ylabel("Transmission (dB)")
  axs[0].set_xlabel("Wavelength (nm)")

  ''' Channel 2 output result'''
  Legend_lables = list()
  for file_path in all_csv_files:                 # Finding the path to CSV file
    if 'Edit' in file_path:
      df = pd.read_csv(file_path)#, header=None)    
      axs[1].plot(df['Wavelength'], df['Channel-2'])
      legend_val = df['Device-ID'][0]
      true_legend = legend_val.split('_')
      chart_title = true_legend[0]
      true_legend= '_'.join([true_legend[1],true_legend[2]])
      Legend_lables= np.append(Legend_lables, true_legend)

  axs[1].set_title(chart_title+'--Channel-2')
  axs[1].legend(Legend_lables)
  axs[1].set_ylim([-55, -10])
  axs[1].set_ylabel("Transmission (dB)")
  axs[1].set_xlabel("Wavelength (nm)")

  ''' Location of the Device on the chip '''
  Legend_lables = list()
  for file_path in all_csv_files:                 # Finding the path to CSV file
    if 'Edit' in file_path:
      df = pd.read_csv(file_path)#, header=None)    
      axs[2].plot(df['X-Coordinate'][0], df['Y-Coordinate'][0], 
              color = 'red', marker='o', markerfacecolor='green')
      legend_val = df['Device-ID'][0]
      true_legend = legend_val.split('_')
      chart_title = true_legend[0]
      true_legend= '_'.join([true_legend[1],true_legend[2]])
      Legend_lables= np.append(Legend_lables, true_legend)
      
  axs[2].set_title(chart_title)
  axs[2].legend(Legend_lables)
  axs[2].set_xlim([-4600, 4600])
  axs[2].set_ylim([-4600, 4600])

  plt.show()
  # print('Success')
  return()

if __name__ == '__main__':
  
  Plot_Pandas(folder_path= 'test', extension='*.csv')
  print("----------File Successfully Written----------")