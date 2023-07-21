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
import statistics as stat

from scipy.optimize import leastsq
from scipy.optimize import curve_fit

# user written functions/files
from MR3_MR4_LorentzApprox import *
from FSR_GroupIndex import *

def BoxPlot(Output_File_Name, Show_Plot = False):

  '''
  This function helps with Plotting Box plots
  The plot generates Change in lambda (Delta Lambda) vs distance between two MRs
  
  # Inputs 
    Name of the file with two columns Lambda Diff and Dist

  # Output :
    Output plot which has been generated. 
  '''

  df = pd.read_csv(Output_File_Name)#, header=None) 

  # Remove all rows where 'Distance' matches 0
  df = df.drop(df[df['Distance'] == 0].index)

  # Sort the DataFrame based on column 'Distance'
  sorted_df = df.sort_values('Distance')

  # convert dataframe to numpy array
  data_arr = sorted_df.to_numpy()

  # print((data_arr[0][1]))

  # Divide the list into 8 different sublists based on the first element of each tuple

  size = math.ceil(len(data_arr)/10)

  subarrays = []
  subarrays_lambda = []
  subarrays_dist = []
  for i in range(0, len(data_arr), size):
      subarrays.append(data_arr[i:i+size])
      subarrays_lambda.append(data_arr[i:i+size,0])
      subarrays_dist.append(data_arr[i:i+size,1])

  # # for i in range(len(xData)):
  # plt.scatter(xData, yData, c='Blue') #type: ignore

  # plt.title('Delta Lambda vs Distance Diff--M4')#type: ignore
  # # plt.legend(Legend_lables, loc='center left', bbox_to_anchor=(1, 0.5),fontsize = 7) #type: ignore
  # # plt.set_ylim([-55, 10])#type: ignore
  # plt.ylabel("Delta Lambda (nm)")#type: ignore
  # plt.xlabel("Distance (um)")#type: ignore
  # if Show_Plot == True:
  #   plt.show()
  # print("Done Printing")
  # return()

  # xData = sorted_df['Distance']
  # yData = sorted_df['Lambda_Diff']

  fig, ax = plt.subplots()
  for i in range (len(subarrays_lambda)):
    ax.scatter(subarrays_dist[i], subarrays_lambda[i], c='Blue', alpha=0.4) #type: ignore
  
  fig2, ax2 = plt.subplots()
  ax2.boxplot(subarrays_lambda)
  ax2.set_xticklabels(['','','','','','','','','',''])

  # Add labels and title
  # ax.set_xticklabels(['Data 1', 'Data 2', 'Data 3','Data 2', 'Data 3', 'Data 2', 'Data 3', 'Data 2', 'Data 3', 'Data 4'])
  # ax.set_ylabel('Value')
  # ax.set_title('Multi-Box Plot')

  fig.savefig('figureMR1.png', transparent=True)
  fig2.savefig('figure2_MR1.png', transparent=True)
  

  # for i in range(len(xData)):
  

  # ax.title('Delta Lambda vs Distance Diff--M4')#type: ignore
  # plt.legend(Legend_lables, loc='center left', bbox_to_anchor=(1, 0.5),fontsize = 7) #type: ignore
  # plt.set_ylim([-55, 10])#type: ignore
  # ax.ylabel("Delta Lambda (nm)")#type: ignore
  # ax.xlabel("Distance (um)")#type: ignore

  if Show_Plot == True:
    plt.show()
  print("Done Printing")
  return()

def Test():
  '''
  Just to test out all the possible cases
  '''
  print("You are now in the test function \n okay bye \n")

  # Generate some random data
  x = np.random.randn(100)
  y = np.random.randn(100)
  z = np.random.randn(100)

  # Create a figure and axis object
  fig, ax = plt.subplots()

  # Create a list of data for box plots
  data = [x, y, z]

  # Create a box plot for each data set
  bp = ax.boxplot(data)

  # Create a scatter plot
  ax.scatter(np.random.normal(1, 0.04, len(x)), x, alpha=0.7)
  ax.scatter(np.random.normal(2, 0.04, len(y)), y, alpha=0.7)
  ax.scatter(np.random.normal(3, 0.04, len(z)), z, alpha=0.7)

  # Set the x-axis label
  ax.set_xlabel('Data')

  # Set the y-axis label for box plot
  ax.set_ylabel('Box Plot')

  # Set the y-axis label for scatter plot
  ax2 = ax.twinx()
  ax2.set_ylabel('Scatter Plot')

  # Show the plot
  plt.show()

  return None

if __name__ == '__main__':

  # Test()

  BoxPlot('Output/Dist_vs_LambdaDiff_M1_25C.csv', Show_Plot = True)
