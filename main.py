import csv
import os
import statistics
import pandas as pd
from matplotlib import pyplot as plt
from collections import Counter


# NFF -- alot of the time was gone into 1) me trying to figure out how to seperate each column into a list, this can be easily done through pandas.. 2) Column detection logic, its still not perfect but i can work with it for now. 

IDENTIFIER_THRESHOLD = 0.9

def clearScreen():
    os.system('cls' if os.name == 'nt' else 'clear')

def loadDataset(file_location):
    try:
        with open(file_location, 'r') as read_file:
            reader = csv.DictReader(read_file)
            dataset = list(reader)
            
            return dataset

    except (FileNotFoundError, PermissionError, IsADirectoryError):
        return None


def informationAboutDataset(dataset):
    clearScreen()
    print()
    no_of_rows = len(dataset)
    no_of_columns = len(dataset[0])
    column_names = list(dataset[0].keys())

    print(f"Rows in the dataset: {no_of_rows}(+1)")
    print(f"Columns in the dataset: {no_of_columns}")
    print("Column names: ", *column_names)
    print("\nData Preview. Showing first five rows of the data..\n")
    for column in column_names:
        print(column, end = " ")
    print()
    for row in range(min(5, no_of_rows)):
        print(*(dataset[row].values()))
    print()

    input("Press Enter to return to the main menu..")


def columnDetection(dataset):
    clearScreen()
    no_of_rows = len(dataset)
    no_of_columns = len(dataset[0])
    column_names = list(dataset[0].keys())
    columns = {column_name : [] for column_name in column_names} # will contain all the values in each column
    
    #Turning each column into a set, and all sets reside inside a list. This is a check because there may be some columns which are completely unique so the program will assume them as "identifiers", remaining columns would be "numeric" or "categorical"

    for row in dataset:
        for column_name in column_names:
            columns[column_name].append(row[column_name])

    numeric_columns = []
    categorical_columns = []
    identifier_columns = []

    difference_of_one_count = 0
    identifier_check = False
    numeric_check = True
    temp_int = 0
    temp_float = 0.0

    
    #adding all numeric columns (including floats) in numeric_columns and all other columns to categorical_columns.
    for column_name, column in columns.items():
        numeric_check = True
        for value in column:
            try:
                temp_int = int(value)
            except ValueError:
                try:
                    temp_float = float(value)
                except:
                    numeric_check = False

        if numeric_check == True:
            numeric_columns.append(column_name)
        else:
            categorical_columns.append(column_name)
    
    #scanning numeric_columns list and categorical_columns list for any identifier columns
    for column_name, column in columns.items():
    
        if column_name in numeric_columns:
            if column_name.lower() in ['id', 'serial', 'sno', 'uid', 'empid', 'userid', 'index']:
                identifier_columns.append(column_name)
                numeric_columns.remove(column_name)
            else:
                difference_of_one_count = 0

                if all(value.isdigit() for value in column):
                    for i in range(len(column) - 1):
                    
                        if(int(column[i+1]) - int(column[i])) == 1:
                            difference_of_one_count += 1

                if difference_of_one_count > 0.9 * (len(column) - 1):
                    identifier_columns.append(column_name)
                    numeric_columns.remove(column_name)

        elif column_name in categorical_columns:
            if column_name.lower() in ['name', 'username', 'user', 'handle'] or (len(set(column)) > len(column) * IDENTIFIER_THRESHOLD):
                identifier_columns.append(column_name)
                categorical_columns.remove(column_name)

    loop_is_running = True

    print("Please check the column classification,..\nIf there's been a mistake in the auto-classification of identifiers.")


    while loop_is_running:
        print()

        print("Detected numeric columns: ", numeric_columns)
        print()

        print("Detected categorical columns: ", categorical_columns)
        print()

        print("Detected identifiers: ", identifier_columns)
        print()
        print()

        choice = input("Enter y or 1 to manually change (entering anything else cause the program to move forward): ")
    

        if choice not in ['y', '1'] :
            loop_is_running = False
            break;
        elif (choice.lower() == 'y'):
            print("\nBelow, please enter the name of the column which is an identifier but mis-classified as smth else OR Vice Versa.\n")
                
            column_choice = input("Column Name: ")

            if(column_choice in numeric_columns):
                print("Only go through if you are sure, this process might break things.\n")
                sure = input(f"Are you sure [{column_choice}] is an identifier?(y for yes): ")
                if (sure.lower() == 'y'):
                    numeric_columns.remove(column_choice)
                    identifier_columns.append(column_choice)
                    print(f"--- [{column_choice}] is now considered an identifier")
                else:
                    print("Abort")
                

                
            elif (column_choice in categorical_columns):
                print("Only go through if you are sure, otherwise this process might break things.\n")
                sure = input(f"Are you sure [{column_choice}] is an identifier?(y for yes): ")
                if (sure.lower() == 'y'):
                    categorical_columns.remove(column_choice)
                    identifier_columns.append(column_choice)
                    print(f"--- [{column_choice}] is now considered an identifier")
                else:
                    print("\n--- ABORT")
            

            elif (column_choice in identifier_columns):
                numeric_check = True
                for value in columns[column_choice]:
                    try:
                        temp_int = int(value)
                    except ValueError:
                        try:
                            temp_float = float(value)
                        except:
                            numeric_check = False

                if numeric_check == True:
                    numeric_columns.append(column_choice)
                    print(f"--- [{column_choice}] is now considered numeric")
                else:
                    categorical_columns.append(column_choice)
                    print(f"--- [{column_choice}] is now considered categorical")

                identifier_columns.remove(column_choice)


            else:
                clearScreen()
                print("\n---INVALID column name, column not present in the dataset.")
        else:
            clearScreen()
            print("\n---INVALID INPUT.\n")
        
    

    return columns, identifier_columns, numeric_columns, categorical_columns

def numericDataAnalysis(columns, numeric_columns):
    for column_name, column in columns.items():
        if column_name in numeric_columns:
            print(f"Column Name: [{column_name}]", end=' |\t')
            try:
                int_column = [int(value) for value in column]
                print(f"Min: {min(int_column)}\tMax: {max(int_column)}\tMean: {int(statistics.mean(int_column))}\tMedian: {statistics.median(int_column)}\tMode: {statistics.mode(int_column)}")
            except:
                float_column = [float(value) for value in column]
                print(f"Min: {min(float_column)}\tMax: {max(float_column)}\tMean: {statistics.mean(float_column) :.2f}\tMedian: {statistics.median(float_column) :.2f}\tMode: {statistics.mode(float_column)}")
            print()
        

def categoricalDataAnalysis(columns, categorical_columns):

    print("\nFrequency Count",end = '\n\n')

    for column_name, column in columns.items():
        if column_name in categorical_columns:
            print(f"Column: [{column_name}]",end='\n-----------\n')
            frequency_count = {}
            for value in column:
                if value in frequency_count:
                    frequency_count[value] += 1
                else:
                        frequency_count[value] = 1

            for value, frequency in frequency_count.items():
                print(f"{value} : {frequency}")
            print()
        


def analyzeData(dataset):
    clearScreen()

    columns, identifier_columns, numeric_columns, categorical_columns = columnDetection(dataset)
    print("Numeric columns: ", numeric_columns)
    print()

    print("Categorical columns: ", categorical_columns)
    print()
    print()

    is_running = True

    while is_running:
        print("1. Numeric columns - Sum, Mean, Median, Mode etc\n2. Categorical columns - Frequency count\n3. Exit\n")
        choice = input("Please select: ")
        print()

        if choice not in ['0', '1', '2', '3']:
            print("Invalid choice..\n")
        
        elif choice == '0':
            print("---EXITING..")
            is_running = False
            break

        elif choice == '1':
            clearScreen()
            numericDataAnalysis(columns, numeric_columns)
        
        elif choice == '2':
            clearScreen()
            categoricalDataAnalysis(columns, categorical_columns)
        
        elif choice == '3':
            return
        
def visualizationParser(text, numeric_columns, categorical_columns):
    words = text.split()

    if words[0].lower() == "distribute" and len(words) == 2:
        col = words[1]
        if col in numeric_columns:
            return ["distribute", 'numeric', col]
        elif col in categorical_columns:
            return ["distribute", 'categoric', col]
        else:
            return "Invalid column."

    elif words[0].lower() == "compare" and len(words) == 3:
        col1, col2 = words[1], words[2]
        if col1 in numeric_columns and col2 in numeric_columns:
            return ["compare", col1, col2]
        else:
            return "Invalid columns for comparison."

    else:
        return "Invalid input."




def Visualization(dataset):
    clearScreen()
    is_running = True
    print("Data Visualization")
    columns, identifier_columns, numeric_columns, categorical_columns = columnDetection(dataset)
    print('\n - - - - - - - - - - -\n')
    print("Numeric columns: ", numeric_columns)
    print()

    print("Categorical columns: ", categorical_columns)
    print()
    print()


    while is_running:
        print("Valud input format: \n- For individual column visualization: distribute [column_name]\n- For Comparison b/w two columns: compare [column_name 1] [column_name 2]\n")
        print("Note: For Categorical columns, only 'distribute' will work\n")
        print('0 to exit\n\n')


        choice = input("Input: ")

        if(choice == '0'):
            print("EXITING..")
            break

        parsed_input = visualizationParser(choice, numeric_columns, categorical_columns)
        
        if (parsed_input not in ['Invalid input.', 'Invalid columns for comparison.', 'Invalid column.']):
            
            if parsed_input[0] == 'distribute' and parsed_input[1] == 'numeric':
                #histogram
                column_data = columns[parsed_input[2]]
                column_data = [int(value) for value in column_data]
                
                plt.style.use('ggplot')
                plt.hist(column_data, bins=5, edgecolor='black')
                plt.xlabel(parsed_input[2])
                plt.ylabel('Frequency')
                plt.title(f'{parsed_input[2]} Distribution')
                plt.show()

            elif parsed_input[0] == 'distribute' and parsed_input[1] == 'categoric':
                counter = Counter(columns[parsed_input[2]])
                x_plane = list(counter.keys())
                y_plane = list(counter.values())

                plt.style.use('ggplot')
                plt.bar(x_plane, y_plane)
                plt.title(f'{parsed_input[2]} Distribution')
                plt.xlabel(parsed_input[2])
                plt.ylabel('Frequency')
                plt.show()

            elif parsed_input[0] == 'compare':
                while True:
                    print(f"Variables: {parsed_input[1]}, {parsed_input[2]}\n")
                    independent_variable = input("Variable at x-axis(the independent variable): ")
                    if independent_variable.lower() in [parsed_input[1].lower(), parsed_input[2].lower()]:
                        break
                
                dependent_variable = parsed_input[1] if (independent_variable == parsed_input[2]) else parsed_input[2] 

                x_plane = columns[independent_variable]
                x_plane = [int(x) for x in x_plane]

                y_plane = columns[dependent_variable]
                y_plane = [int(x) for x in y_plane]

                plt.style.use('fivethirtyeight')

                colors = [x/10 for x in x_plane]
                plt.scatter(x_plane, y_plane,s=100, c=colors, cmap='Greens', edgecolors='black', alpha=0.75)
                cbar = plt.colorbar()
                cbar.set_label(dependent_variable)
                plt.xlabel(independent_variable)
                plt.ylabel(dependent_variable)
                plt.title(f'Comparison: {independent_variable} | {dependent_variable}')

                plt.show()

            else:
                print("\nInvalid input. Try again..\n")
        else:
            print("\nInvalid input. Try again..\n")


if __name__ =='__main__':
    #print("\nLittle Data Analysis Program.\n")
    is_running = True
    while is_running:
        print("1. Load Dataset\n0. Exit\n")
        choice = input("Please select an option: ")
        if choice not in ['0', '1']:
            print("Invalid choice..\n")
        elif choice == '0':
            print("---EXITING..")
            is_running = False
            break
        elif choice == '1':
            print("\nPlease ensure the file is in .csv format in order for the program to work expectedly.\nAlso Enter the complete file location.\n\n", end='')
            file_location = input("File location: ")

            is_running2 = True
            dataset = loadDataset(file_location)

            if dataset is None:
                print("\nError: The File was not found, or it could not be opened.\n")
            else:
                while is_running and is_running2:
                    clearScreen()
                    print(f"\nFile {file_location} successfully loaded. Please proceed..")

                    print("\n1. Information about the dataset\n2. Data Analysis\n3. Filter/Search\n4. Visuals\n0. Exit\n")
                    choice = input("Please choose an option: ")

                    if choice not in ['0', '1', '2', '3', '4']:
                        print("\nInvalid choice.\n")
                    elif choice == '0':
                        print('Exiting to main menu..\n')
                        is_running2 = False
                        break
                    elif choice == '1':
                        informationAboutDataset(dataset)
                    elif choice == '2':
                        analyzeData(dataset)
                    elif choice == '3':
                        print("Not Implemented Yet.")
                        input('Press Enter..') 
                    elif choice == '4':
                        Visualization(dataset)

