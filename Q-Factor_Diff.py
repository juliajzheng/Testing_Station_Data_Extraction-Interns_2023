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
import json

from scipy.optimize import leastsq
from scipy.optimize import curve_fit

# user written functions/files
from MR3_MR4_LorentzApprox import *
from FSR_GroupIndex import *

def Cal_dist (p1, p2):
  ''' 
  Calcualate distance between two points 
  
  # Input:
    Two points A and B in our case p1 and p2

  # Output:
    The distance between these two parts
  '''
  distance = math.sqrt( ((p1[0]-p2[0])**2)+((p1[1]-p2[1])**2) )
  return(distance)

def BoxPlot(Output_File_Name, File_to_write= 'Test_Matlab.csv'):

  '''
  This function helps with Plotting Box plots
  The plot generates Change in lambda (Delta Lambda) vs distance between two MRs
  
  # Inputs 
    Name of the file with two columns Lambda Diff and Dist

  # Output :
    Output plot which has been generated. 
  '''

  # df = pd.read_csv(Output_File_Name)#, header=None) 

  # Open the JSON file
  with open(Output_File_Name) as f:
      data = json.load(f)

  data = list(data.items())

  print('Total length of list is:', len(data))
  
  List1 = data[1:]
  List2 = data[:-1]

  Dist_Diff_arr = list()
  Qfactor_Diff_arr = list()
  ER_Diff_arr = list()

  for i in (List1): 
    i_Qfactor = i[1]['Q-factor']
    i_ER = i[1]['ER']
    # print(i_Qfactor)
    i_xCor = i[1]['X-Coordinate']
    i_yCor = i[1]['Y-Coordinate']
    i_Loc = [i_xCor, i_yCor]

    for j in (List2):
      j_Qfactor = j[1]['Q-factor']
      j_ER = j[1]['ER']
      # print(i_Qfactor)
      j_xCor = j[1]['X-Coordinate']
      j_yCor = j[1]['Y-Coordinate']
      j_Loc = [j_xCor, j_yCor]

      # Dist = math.dist(i_Loc, j_Loc)
      Dist = Cal_dist(i_Loc, j_Loc)
      Dist = round(Dist, 3)

      if Dist == 0:
        continue

      Qfactor_Diff = abs(i_Qfactor-j_Qfactor)
      Qfactor_Diff = round(Qfactor_Diff, 3)

      ER_Diff = abs(i_ER - j_ER)
      ER_Diff = round(ER_Diff, 3)

      Dist_Diff_arr = np.append(Dist_Diff_arr, Dist)
      Qfactor_Diff_arr = np.append(Qfactor_Diff_arr, Qfactor_Diff)
      ER_Diff_arr = np.append(ER_Diff_arr, ER_Diff)

  dict_to_write = {'Distance': Dist_Diff_arr, 'Qfactor_Diff':Qfactor_Diff_arr, 'ER_Diff':ER_Diff_arr}
  df = pd.DataFrame(dict_to_write)

  if not os.path.exists("Output"):
    os.mkdir("Output")

  # Writing the output the respective file
  df.to_csv('Output/'+File_to_write+'.csv', header=True, index= False)

  return()


if __name__ == '__main__':

  BoxPlot('Output/MR4_25C_AnalysisData.json', File_to_write = 'MR4_25C_Matlab')
# /Users/MIRZAASIF/Documents/Testing_Station_Data_Extraction/Box_Plots.py