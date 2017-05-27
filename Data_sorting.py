"""This class contains calculation for sorting data in order to make the plotting scripts lighter
@author Boris Gailleton"""
import numpy as np
import pandas as bamboo_bears
from pyproj import Proj, transform

def source_num_of_longest_river(arr):
    """
    This function will return the source number of the longuest channel by counting the number of occurence of each sources number.
    It may be an issue if your channel have similar size, I will create a fancier function that calculate the actual lenght of each channel if required.
    """
    counount = 0
    max_count = -999
    max_count_index = -999

    for i in range(1,arr.shape[0]):
        if(arr[i] == arr[i-1]):
            counount += 1
        else:
            if (counount > max_count):
                max_count_index = arr[i-1]
                max_count = counount
            counount = 0

    return max_count_index

def crop_point_data_to_base_raster(raster_name, raster_directory, csv_file, EPSG_code = 0):
    """
    This function create a new csv file cropped to the base raster. It can lower the processing time if your point data is on a significantly larger area than the base raster.
    """
    print("ok let me load your dataset and your hdr file")
    # Read the file
    df = bamboo_bears.read_csv(csv_file)
    # Read and sort the csv_info
    with open(raster_directory+raster_name+".hdr","r") as hdr_file:
        print("I got these")
        for line in hdr_file:
            if(line[0:8] == "map info"):
                info = line[12:-2]
                info = info.split(",")
                x_min = float(info[3])
                y_max = float(info[4])
                x_res = int(info[5])
                y_res = int(info[6])
                utm_zone = int(info[7])
                utm_hemisphere = info[8]
            else:
                if(line[0:7] == "samples"):
                    num_col = line.replace(" ","").split("=")[1]
                    print("there are " + str(num_col) + " columns")
                    num_col = int(num_col)
                else:
                    if(line[0:5] == "lines"):
                        num_lines = line.replace(" ","").split("=")[1]
                        print("there are " + str(num_lines) + " lines")
                        num_lines = int(num_lines)

    # Now I calculate the size of the dem
    x_max = x_min + x_res*num_col
    y_min = y_max - y_res*num_lines
    # Conversion UTM to lat/long
    inProj = Proj(init='epsg:'+str(EPSG_code))
    outProj = Proj(init='epsg:4326')
    long_min,lat_min = transform(inProj,outProj,x_min,y_min)
    long_max,lat_max = transform(inProj,outProj,x_max,y_max)

    # data sorting
    df = df[df.longitude<long_max]
    df = df[df.latitude<lat_max]
    df = df[df.latitude>lat_min]
    df = df[df.longitude>long_min]
    df.to_csv(csv_file[:-4]+"_"+raster_name+"_filtered.csv", index = False)


    return csv_file[:-4]+"_"+raster_name+"_filtered.csv"