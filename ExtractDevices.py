import pya
import csv
import math


def get_info():
    print("Enter Layer Value")
    try:
        layer = input()
    except EOFError as e:
        layer = 10
        print("Error reading input defaulting to layer 10")

    print("Enter Data Type")
    try:
        datatype = input()
    except EOFError as e:
        datatype = 0
        print("Error reading input defaulting to data type 0")

    print("Enter Top Cell")
    try:
        topcell = input()
    except EOFError as e:
        topcell = "ECSyD_Layout_V1"
        print("Error reading input defaulting to topcell ECSyD_Layout_V1")

    print("Enter Filename")
    try:
        filenameonly = input()
    except EOFError as e:
        filename = "/Users/josephthompson/Desktop/DEBUG_testring_labels_june_26.csv"
        print("Error reading input defaulting to 'no_name'")


# layout coresponds to ly, findLay coresponds to input, and cellIter coresponds to si in the original ruby file


def make_layer():
    layout = MainWindow().instance().current_view().active_cellview().layout()  # create layout

    findLay = layout.find_layer(layer, datatype)  # find layout

    if (findLay == None):  # throws error if input layer doesn't exist
        raise AttributeError("Input layer not found")

    initialCell = layout.cell(layout.cell_by_name(topcell))  # first cell number

    cellIter = initialCell.begin_shapes_rec(findLay)  # create iterator for cells

    arr = [[None] * 7] * 10000  # create array large enough to hold data
    size = 0;


def load_data():
    while (cellIter.at_end() != True):  # loops through literator of cells

        if (cellIter.shape().is_text() != True):
            cellIter.next()  # if cell is not text, skip iterator

        else:
            bbox = cellIter.shape().bbox().transformed(cellIter.trans())  # create shape object with data we want
            name = cellIter.shape().text_string  # get name
            xcoor = ((bbox.center().x) * (layout.dbu))
            ycoor = ((bbox.center().y) * (layout.dbu))

            if (("doi" not in name) and ("SiEPIC" not in name) and (
                    "TE Oxide" not in name)):  # skips cells with these names
                if (size == 0):
                    arr.insert(0, [xcoor, ycoor, "TE", "1550", "Grating Coupler", name,
                                   "no comment"])  # base case of empty array
                    # arr[0]=[xcoor,ycoor,"TE","1550","Grating Coupler",name,"no comment"]
                    size += 1;
                    cellIter.next()
                else:
                    k = 0
                    while (k <= size):
                        if (k == size):
                            arr.insert(k, [xcoor, ycoor, "TE", "1550", "Grating Coupler", name,
                                           "no comment"])  # as we iterate trought the array if x value of device we want to add
                            # arr[k] = [xcoor,ycoor,"TE","1550","Grating Coupler",name,"no comment"] #is less than the x value in the array ahead of it
                            cellIter.next()  # we add the device at this location.
                            size += 1  # if two devices have the same x value, then they
                            k = size + 1  # are sorted by y value from least to greatest
                        elif (abs(xcoor - float(arr[k][0])) < 0.0001):
                            if (abs(ycoor - float(arr[k][1])) < 0.0001 or ycoor < float(arr[k][1])):
                                arr.insert(k, [xcoor, ycoor, "TE", "1550", "Grating Coupler", name, "no comment"])
                                size += 1
                                cellIter.next()
                                k = size + 1
                            else:
                                k += 1
                        elif (xcoor < float(arr[k][0])):
                            arr.insert(k, [xcoor, ycoor, "TE", "1550", "Grating Coupler", name, "no comment"])
                            size += 1
                            cellIter.next()
                            k = size + 1
                        else:
                            k += 1
            else:
                cellIter.next()


print(arr)
print(size)


# size += 1000;

def print_csv():
    f = open(filename, "w")  # create CSV file
    writer = csv.DictWriter(
        f, fieldnames=["<X-coord>", "<Y-coord>", "<Polarization>", "<wavelength>", "<type>", "<deviceID>", "<comment>"])
    writer.writeheader()  # create header
    i = 0;
    while (i < size):  # loops through literator of cells
        writer.writerow(
            {"<X-coord>": arr[i][0], "<Y-coord>": arr[i][1], "<Polarization>": arr[i][2], "<wavelength>": arr[i][3],
             "<type>": arr[i][4], "<deviceID>": arr[i][5], "<comment>": arr[i][6]})
        i += 1


get_info()
filename = "/Users/josephthompson/Desktop/DEBUG6_testring_labels_june_26.csv"
make_layer()
get_info()
print_csv()











