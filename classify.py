import json
import pandas as pd




#### UGLY SCRIPT!


# First get data in dict

#init keys
minMedianSalaryKey = "minMedianSalary"
maxMedianSalaryKey = "maxMedianSalary"
nameKey = "name"

#institutes with median salary < 20 lakh
res = {'0 - 5 Lakh': {}, '5 Lakh - 10 Lakh': {}, '10 Lakh - 15 Lakh': {}, '15 Lakh - 20 Lakh': {}, 'Greater than 20 Lakh': {}, 'Data Not Available': {}}

for i in range(1, 50):
# for i in range(1, 2):
    # Specify the path to your JSON file
    json_file_path = f'./data/maharashtra/{i}.json'

    # Open the JSON file and load the data
    with open(json_file_path, 'r') as file:
        data = json.load(file)

    # Now, 'data' contains the loaded JSON content as a Python dictionary
    instituteDict = data['data']['instituteTuples']
    for instituteData in instituteDict:
    
        #extract data
        maxMedianSalary = instituteData[maxMedianSalaryKey] if maxMedianSalaryKey in instituteData else 'Not Provided'
        minMedianSalary = instituteData[minMedianSalaryKey] if minMedianSalaryKey in instituteData else 'Not Provided'
        instituteName = instituteData[nameKey]

        #categorize
        categoryDict = res['Data Not Available']
        if maxMedianSalary != 0 and maxMedianSalary != 'Not Provided':
            if maxMedianSalary < 500000:
                categoryDict = res['0 - 5 Lakh']
            elif maxMedianSalary < 1000000: 
                categoryDict = res['5 Lakh - 10 Lakh']
            elif maxMedianSalary < 1500000: 
                categoryDict = res['10 Lakh - 15 Lakh']
            elif maxMedianSalary < 2000000:
                categoryDict = res['15 Lakh - 20 Lakh']
            else:
                categoryDict = res['Greater than 20 Lakh']

        #add to correct category
        categoryDict[instituteName] = {'Name': instituteName, 'MaxMedianSalary': maxMedianSalary, 'MinMedianSalary': minMedianSalary}





# Put into separate dict for pandas dataframe
finalRes = {'0 - 5 Lakh': {}, '5 Lakh - 10 Lakh': {}, '10 Lakh - 15 Lakh': {}, '15 Lakh - 20 Lakh': {}, 'Greater than 20 Lakh': {}, 'Data Not Available': {}}
for category in res:
    categoryData = res[category]
    if 'Institute Name' not in finalRes[category]:
        finalRes[category]['Institute Name'] = []
    if 'Median Salary Min' not in finalRes[category]:
        finalRes[category]['Median Salary Min'] = []
    if 'Median Salary Max' not in finalRes[category]:
        finalRes[category]['Median Salary Max'] = []
    for college in categoryData:
        name = categoryData[college]['Name']
        medsalmax = categoryData[college]['MaxMedianSalary']
        medsalmin = categoryData[college]['MinMedianSalary']
        finalRes[category]['Institute Name'].append(name)
        finalRes[category]['Median Salary Min'].append(medsalmin)
        finalRes[category]['Median Salary Max'].append(medsalmax)

        




#Save data

#Specify the path where you want to save the Excel file
excel_file_path = './maharashtrafinal.xlsx'
# Create an Excel writer object
dfs = []
with pd.ExcelWriter(excel_file_path, engine='xlsxwriter') as writer:
    for category in finalRes:
        dfs.append([category, pd.DataFrame(finalRes[category])])
    
    for dfObj in dfs:
        dfObj[1].to_excel(writer, sheet_name = dfObj[0], index=False)

print(f"Excel file with multiple sheets saved at: {excel_file_path}")




# Code snippets that maybe useful
```
# Rough printing code
# for category in res:
#     categoryData = res[category]
#     print(category)
#     for college in categoryData:
#         print(categoryData[college])



```