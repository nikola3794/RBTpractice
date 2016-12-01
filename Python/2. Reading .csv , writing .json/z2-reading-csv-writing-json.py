import csv
import getopt, sys
import json

'''
function: productTypes
input:
    csvFile - opened .csv file object that needs to be processed

This function reads the .csv and prints all of the product categories
from the file and how much products are from that category.
'''
def productTypes(csvFile):
    # Creates a new dictionary to store the product categories
    types = dict()

    try:
        # Creates a reader object for the module csv
        fh = csv.reader(csvFile)

        # Iterates on each row of the .csv file
        # The row is stored in a list 'row', where every column is an element
        for row in fh:
            # If a given categorie key exists in the dictionary , increment its value
            # If it doesn't, set its value to 1
            try:
                types[row[8]] = 1 + types.get(row[8], 1)
            except IndexError as e:
                print(e)
                types['BADLY FILLED ROW'] = 1 + types.get('BADLY FILLED ROW',1)
    except csv.Error as e:
        print(e)

    for key in types:
        print(key, types[key])


'''
function: extractData
inputs:
    csvFile - opened .csv file object that needs to be processed
    data - an array to store the extracted information

This function reads the .csv file and extracts all of the products that are from the category:
Chairs & Chairmats, Tables, Storage & Organization, Office Furnishings and Bookcases
The function extracts all of the rows with the requested category as a list element dictionaries with the keys:
"Contact person", "Product name", "Location"
'''
def extractData(csvFile, data):
    # Categories of the elements to be extracted from the .csv file
    keywords=["Chairs & Chairmats", "Tables", "Storage & Organization", "Office Furnishings", "Bookcases"]

    try:
        # Creates a reader object for the module csv
        fh = csv.reader(csvFile)

        # Iterates on each row of the .csv file
        # Extract all of the rows with the requested category as a list element dictionaries with the keys:
        # "Contact person", "Product name", "Location"
        for row in fh:
            try:
                category = row[8]
            except IndexError as e:
                print(e)
                category = ''

            # Checks if the current row needs to be processed
            if category in keywords:
                try:
                    contact = row[2]
                except IndexError as e:
                    print(e)
                    contact=''
                try:
                    product = row[1]
                except IndexError as e:
                    print(e)
                    product=''
                try:
                    location = row[7]
                except IndexError as e:
                    print(e)
                    location=''

                # If all of the information is missing, do nothing
                if not (contact == '' and product == '' and location == ''):
                    data.append({
                    "Contact person" : contact,
                    "Product name" : product,
                    "Location" : location})

    except csv.Error as e:
        print(e)

def main():
    # Try's to read the command line arguments
    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:o:")
    except getopt.GetoptError as e:
        print(e)

    # Loads the input and output files names, from the command line arguments  (input:Address list.csv)
    inputFile = ''
    outputFile = ''
    for o,a in opts:
        if o=='-i':
            inputFile=a
        elif o=='-o':
            outputFile=a

    # An array where the extracted data will be stored
    data=[]

    # Trys to process the .csv file
    try:
        # Opens the.csv file that needs to be processed, creating a file object
        with open(inputFile, newline='') as csvfile:

            # Displays all of the different product categories and how many elements are contained in them
            productTypes(csvfile)

            # Resets the file pointer to the beginning of the file
            csvfile.seek(0)

            # Extract all of the rows with the requested category
            extractData(csvfile, data)

            csvfile.close()

    except IOError:
        print("The .csv file doesnt exist")

    # Try's to write the processed data into a json file
    try:
        fh = open(outputFile, 'w')
        fh.write(json.dumps(data, indent=4))
        fh.close()
    except IOError:
        print("There has been an error while trying to write to data.json")

    # Trys to import the data from the .json file into a list
    try:
        fh=open(outputFile,'r')
        newData=json.loads(fh.read())
        fh.close()
        print(newData)
    except IOError:
        print("There has been an error while trying to read from data.json")

if __name__ == "__main__":
    main()