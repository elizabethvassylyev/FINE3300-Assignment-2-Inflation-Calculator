import numpy as np #imports NumPy for numerical operations
import pandas as pd #imports Pandas for data manipulation and analysis
import matplotlib.pyplot as plt #imports Matplotlib for creating graphs and visualizing data

DATA_FILE = "STATIC_INFLATIONCALC.csv" #stores the name of the CPI data file
GRAPH_FILE = "CPI_Graph.png" #stores the name of the output graph file

#this section checks if the user enters a valid date in the format YYYY-MM and if the date exists in the CPI data
def get_date(prompt, cpi_data): #creates a function to get and check the user's inputted date
    while True: #repeats until a valid date is entered
        date_text = input(prompt).strip() #gets the user's date and removes extra spaces
        valid_format = (len(date_text) == 7 and date_text[4] == "-" and date_text[0:4].isdigit() and date_text[5:7].isdigit()) #checks if the date follows YYYY-MM format
        if not valid_format: #checks if the date format is invalid
            print("Invalid Date Format. Please Use YYYY-MM, for Example 2005-08.") #tells the user the correct format
            continue #returns to the beginning of the loop to ask again
        month = int(date_text[5:7]) #takes the month from the entered date and changes it to an integer
        if month < 1 or month > 12: #checks if the month is outside the range of 1 to 12
            print("Invalid Month. Please Enter a Month from 01 to 12.") #tells the user the valid month range
            continue #returns to the beginning of the loop to ask again
        matching_row = cpi_data[cpi_data["month_year"] == date_text] #finds the row in the CPI data that matches the entered date
        if len(matching_row) == 0: #checks if no matching date was found in the CPI data
            first_month = cpi_data["month_year"].iloc[0] #gets the earliest month available in the CPI data
            last_month = cpi_data["month_year"].iloc[-1] #gets the latest month available in the CPI data
            print(f"Date Not Found. Please Enter a Month Between {first_month} and {last_month}.") #tells the user the available date range (this allows for future updates to the CPI data without changing the code)
            continue #returns to the beginning of the loop to ask again
        cpi_value = float(matching_row["STATIC_INFLATIONCALC"].iloc[0]) #gets the CPI value for the entered date and changes it to a decimal number
        return date_text, cpi_value #returns the valid date and its CPI value

#this section reads the CPI data and prepares the dates
cpi_data = pd.read_csv(DATA_FILE, skiprows=8) #reads the CPI data from the CSV file, skipping the first 8 rows which contain introductory information
cpi_data["date"] = pd.to_datetime(cpi_data["date"]) #changes the dates from text into a date format
cpi_data["month_year"] = cpi_data["date"].dt.strftime("%Y-%m") #creates a new column with dates in YYYY-MM format for easier comparison with user input

#this section displays the calculator title
print("") #formatting, blank line before title
print("Canadian Inflation Calculator") #prints the calculator title
print("") #formatting, blank line after title

#this section asks the user for the original price and two dates
while True: #repeats until the user enters a valid price
    try: #tries to convert the user's input into a number
        original_price = float(input("Step 1 | Enter the Original Price in CAD: ")) #asks for the original price and changes it to a decimal number
        if original_price > 0: #checks if the price is greater than zero
            break #stops the loop when a valid price is entered
    except ValueError: #checks if the input cannot be converted into a number
        pass #skips the error and continues to the next line
    print("Invalid Amount. Please Enter a Number Greater Than Zero (No Commas or $ Signs).") #tells the user how to enter a valid price

first_date, first_cpi = get_date("Step 2 | Enter the First Date (YYYY-MM): ", cpi_data) #gets the first date and its CPI value using the get_date function
second_date, second_cpi = get_date("Step 3 | Enter the Second Date (YYYY-MM): ", cpi_data) #gets the second date and its CPI value using the get_date function

#this section calculates the adjusted cost, percentage change, elapsed time and average annual rate of change using the selected CPI values
adjusted_cost = original_price * (second_cpi / first_cpi) #calculates the adjusted cost by multiplying the original price by the ratio of the second CPI to the first CPI
percentage_change = ((adjusted_cost - original_price) / original_price) * 100 #calculates the percentage change by subtracting the original price from the adjusted cost, dividing by the original price and multiplying by 100
first_year = int(first_date[0:4]) #takes the year from the first date and changes it to an integer
first_month = int(first_date[5:7]) #takes the month from the first date and changes it to an integer
second_year = int(second_date[0:4]) #takes the year from the second date and changes it to an integer
second_month = int(second_date[5:7]) #takes the month from the second date and changes it to an integer
elapsed_months = abs((second_year - first_year) * 12 + second_month - first_month) #calculates the total number of months between the two dates by finding the difference in years, multiplying by 12 and adding the difference in months, then taking the absolute value to ensure a positive result
elapsed_years = elapsed_months / 12 #calculates the total number of years between the two dates by dividing the total months by 12

if elapsed_months == 0: #checks if the two dates are the same, which would result in a division by zero error when calculating the average annual rate of change
    annual_rate = 0.0 #sets the annual rate to zero if the two dates are the same, as there is no change over time
else: #runs if the two dates are different
    annual_rate = ((adjusted_cost / original_price) ** (1 / elapsed_years) - 1) * 100 #calculates the average annual rate of change using the compound annual growth rate formula, then multiplies by 100 to convert it to a percentage

#this section displays the calculated inflation results
print("") #formatting, blank line before divider
print("---------------------------------------------------------------") #formatting, separates the inputs from the results
print("") #formatting, blank line before results title
print("Inflation Calculator Results") #prints the results title
print("") #formatting, blank line after results title
print(f"${original_price:,.2f} CAD in {first_date} is equal to ${adjusted_cost:,.2f} CAD in {second_date}") #prints the original and adjusted cost with dates, formatted to two decimal places
print("") #formatting, blank line after the main result
print(f"Total Percentage Change: {percentage_change:,.2f}%") #prints the total percentage change rounded to two decimal places
print(f"Elapsed Time: {elapsed_years:,.2f} years ({elapsed_months} months)") #prints the elapsed time in years and months
print(f"Average Annual Rate of Change: {annual_rate:,.2f}%") #prints the average annual rate of change rounded to two decimal places
print("") #formatting, blank line before CPI values
print(f"CPI for {first_date}: {first_cpi:,.2f}") #prints the CPI value for the first date
print(f"CPI for {second_date}: {second_cpi:,.2f}") #prints the CPI value for the second date
print("") #formatting, blank line after CPI values

#this section creates a graph showing monthly CPI values and annual percentage changes
cpi_values = np.array(cpi_data["STATIC_INFLATIONCALC"]) #stores the CPI values from the data in a NumPy array
annual_change = ((cpi_values[12:] / cpi_values[:-12]) - 1) * 100 #calculates the annual percentage change by comparing each month's CPI to the same month in the previous year
figure, cpi_axis = plt.subplots(figsize=(12, 6)) #creates the graph with a size of 12 by 6 inches
inflation_axis = cpi_axis.twinx() #creates a second (vertical) y-axis on the right side of the same graph for the annual percentage change
cpi_line = cpi_axis.plot(cpi_data["date"], cpi_values, color="#004F71", label="Monthly CPI") #plots the monthly CPI values in Bank of Canada blue
inflation_line = inflation_axis.plot(cpi_data["date"].iloc[12:], annual_change, color="#651D32", label="Annual percentage change") #plots the annual percentage changes in Bank of Canada maroon
base_line = cpi_axis.axhline(y=100, color="gray", linestyle=":", label="CPI base level (100)") #adds a gray dotted line at the CPI base level of 100
cpi_axis.set_title("Canadian Consumer Price Index and Annual Percentage Change") #adds the graph title
cpi_axis.set_xlabel("Date") #labels the (horizontal) x-axis
cpi_axis.set_ylabel("Consumer Price Index (2002 = 100)") #labels the (left vertical) y-axis
inflation_axis.set_ylabel("Annual Percentage Change (%)") #labels the (right vertical) y-axis
cpi_axis.legend([cpi_line[0], inflation_line[0], base_line], ["Monthly CPI", "Annual Percentage Change", "CPI Base Level (100)"], loc="upper right") #adds a legend identifying the three lines
figure.tight_layout() #adjusts the spacing so the graph labels fit properly
figure.savefig(GRAPH_FILE, dpi=300) #saves the graph as a PNG image
plt.close(figure) #closes the graph after saving it

print("---------------------------------------------------------------") #formatting, divider after the results
print("") #formatting, blank line before graph confirmation message
print(f"CPI Graph Saved as {GRAPH_FILE}.") #confirms that the graph was saved under the specified filename
print("") #formatting, blank line after graph confirmation message