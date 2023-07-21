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
import re
# from sets import set

from scipy.optimize import leastsq
from scipy.optimize import curve_fit

from MR3_MR4_LorentzApprox import *

def GroupIndex_Calc():
  # Reading the csv file 
  raw_data = pd.read_csv("Output/MR1_Minimum_Lambda.csv",header= None)
  Lambda_values = list()
  Ng_values = list()

  for i_length in range(len(raw_data)):
    # print(i_length)
    list_values = raw_data[1][i_length].split(",")
    # Converting string to list 
    new_list = [float(re.findall("\d+\.\d+", i)[0]) for i in list_values] #type: ignore
    sorted_list = sorted(new_list)

    lambda_list, ng_list = Cal_FSR(input_list= sorted_list)

    Lambda_values.append(lambda_list)
    Ng_values.append(ng_list)
  
  Plot_Ng_Lambda(Lambda_list=Lambda_values,Ng_list=Ng_values)

  return ()

def Cal_FSR(Radius = 9.935,input_list = [1550,1555,1560]):
# This function is to help you calculate FSR value

  # Eliminating any duplicate values
  temp_list = list ()
  for  i in input_list:
    if i not in temp_list:
      temp_list.append(i)
  input_list = temp_list

  Ring_len = 2*math.pi*(Radius)
  lambda_list_val = list()
  ng_list_val = list()

  for i in range(len(input_list)-1):
    lambda_val = (input_list[i])
    FSR = (input_list[i+1] - input_list[i])
    try : 
      ng = round((lambda_val**2)/(Ring_len*FSR*1000),4) # Ensuring consistent units [nm --> μm]
      if ng > 2.2:
        # print(input_list)
        lambda_list_val.append(lambda_val)
        ng_list_val.append(ng)

    except ZeroDivisionError:
      print("skipping this value", input_list)

    # Appending values to the list   
  return(lambda_list_val, ng_list_val)

def Plot_Ng_Lambda (Lambda_list = [[1535.32], [1544.976], [1535.8]], 
                    Ng_list = [[3.9165],[3.9172],[3.9079]],
                    Show_Plot= True):
  
  print("Displaying values")
  for i in range(len(Lambda_list)):
    plt.scatter(Lambda_list[i], Ng_list[i])
  plt.title("Mode tracking")
  plt.ylabel("Group Index")
  plt.xlabel("Wavelength (in nm)")
  

  if Show_Plot == True:
    plt.show()
  return()

if __name__ == '__main__':
  GroupIndex_Calc()
  # Plot_Ng_Lambda()