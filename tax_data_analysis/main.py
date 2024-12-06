######################################################
# Project: Project 3
# UIN: 662265995
# repl.it URL: https://replit.com/@CS111-Fall2021/Project-3-FilipToloczko#main.py

# For this project, I received help from the following members of CS111.
# Vladyslav Symonenko, netID Vsymon2: help with retrieving data from files and internet.
# David Cardenas, netID Dcard4: help with creating my functions.
 
######################################################
#importing the imports
import json
import csv
import requests
import matplotlib.pyplot as plt
#defining the functions
def get_data_from_file(fn, format=""):
  """return data from a file in python format"""
  if format == "":
    typefile = fn.split('.')
    format = typefile[1]
  else:
    pass
  if format == "csv":
    data = []
    f = open(fn)
    info = csv.reader(f)
    for i in info:
      data.append(i)
    f.close()
  elif format == "json":
    f = open(fn)
    data = json.load(f)
    f.close()
  return(data)

def get_data_from_internet(url, format="json"):
  """returns data from internet in python format"""
  if format == "json":
    r = requests.get(url)
    data = r.json()
  elif format == "csv":
    r = requests.get(url)
    text = r.text
    data = text.split("\n")
  return(data)
    

def get_index_for_column_label(header_row, column_label):
  """returns the index position of an item in a header"""
  index = header_row.index(column_label)
  return(index)

def get_state_name(state_names, state_code):
  """returns the name of the state whose code has been entered"""
  lst_states = []
  for i in state_names:
    lst_states.append(i)
  for i in lst_states:
    if i["abbreviation"] == state_code:
      return(i["name"])
    else:
      pass


def get_state_population(state_populations, state_name):
  """returns the population of a state"""
  lst = []
  for dics in state_populations:
    lst.append(dics)
  for i in lst:
    for key in i:
      if key == '.'+state_name:
        return(i[key])


def answer_header(question_number, question_labels):
 ''' returns the header string for each answer'''
 header = "\n"*2
 header += "="*60 + "\n"
 header += "Question " + str(question_number) + "\n"
 header += question_labels[question_number] + "\n"
 header += "="*60 + "\n"
 return header

#defining the main function
def main():
  """the main function"""
  #defining the variables
  state_populations_list = get_data_from_internet('https://raw.githubusercontent.com/heymrhayes/class_files/main/state_populations_2018.txt', format="json")

  state_codes = get_data_from_file('states_titlecase.json', format="json")

  tax_data = (get_data_from_file('tax_return_data_2018.csv', 'csv'))
  
  tax_data.pop(0)

  state_input = input("Enter a state code: ")

  question_labels = [
   "",
   "average taxable income per return across all groups",
   "average taxable income per return for each agi group",
   "average taxable income (per resident) per state",
   "average taxable income per return across all groups",
   "average taxable income per return for each agi group",
   "average dependents per return for each agi group",
   "percentage of returns with no taxable income per agi group",
   "average taxable income per resident",
   "percentage of returns for each agi_group",
   "percentage of taxable income for each agi_group"
 ]

  #*************************************************************************************
  # What is the average taxable income per return (all returns, not just returns with taxable income) across all groups?
  #*************************************************************************************
  
  number_of_returns = 0

  for i in tax_data:
    number_of_returns += int(i[4])

  amount_of_taxable_income = 0

  for i in tax_data:
    amount_of_taxable_income += int(i[96])

  answer1 = (((amount_of_taxable_income / number_of_returns)*1000))

  answer1 = "${:8.0f}".format( (answer1) )

  #writes the answer for #1 to the file
  file = open("answers" + state_input + ".txt", "w") 
  file.write(answer_header(1, question_labels))
  file.write(answer1) 
  file.close()

  #*************************************************************************************
  # What is the average taxable income per return (all returns, not just returns with taxable income) for each agi group?
  #*************************************************************************************

  dic_of_AGI_return_numbers = {"1":0}

  for i in tax_data:
    if i[3] in dic_of_AGI_return_numbers:
      dic_of_AGI_return_numbers[i[3]] += int(i[4])
    elif i[3] not in dic_of_AGI_return_numbers:
      dic_of_AGI_return_numbers[i[3]] = int(i[4])
  
  dic_of_AGI_income_amount = {"1":0}

  for i in tax_data:
    if i[3] in dic_of_AGI_income_amount:
      dic_of_AGI_income_amount[i[3]] += int(i[96])
    elif i[3] not in dic_of_AGI_income_amount:
      dic_of_AGI_income_amount[i[3]] = int(i[96])
  
  file = open("answers"+state_input+".txt", "a")
  
  file.write(answer_header(2, question_labels))
  #writes the answer for #2 to the file
  for i in dic_of_AGI_income_amount:
    x = ("Group "+i+ ": ${:8.0f}".format((dic_of_AGI_income_amount[i] / dic_of_AGI_return_numbers[i]) * 1000))
    file.write(x+"\n")

  file.close()


  #*************************************************************************************
  # What is the average taxable income (per resident) per state?
  #*************************************************************************************

  state_population_dictionary = {}

  list_of_state_names = []
  
  states_abbs = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", "HI","ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
  
  for i in state_codes:
    if i["abbreviation"] not in states_abbs:
      state_codes.remove(i)
    else:
      pass

  for dictionaries in state_codes:
    list_of_state_names.append(dictionaries["abbreviation"])

  for i in range(len(list_of_state_names)):
    list_of_state_names[i] = list_of_state_names[i]

  populations = []
  for i in state_populations_list:
    x = str(i.values())
    y = filter(str.isdigit, x)
    z = "".join(y)
    populations.append(z)

  state_population_dictionary = dict(zip(list_of_state_names, populations))

  state_return_dictionary = {}
  
  for i in tax_data:
    i[1] = i[1]
    if i[1] in state_return_dictionary:
      state_return_dictionary[i[1]] += int(i[96])
    elif i[1] not in state_return_dictionary:
      state_return_dictionary[i[1]] = int(i[96])

  file = open("answers"+state_input+".txt", "a")

  file.write(answer_header(3, question_labels))
  #writes the answer for #3 to the file
  for state in state_return_dictionary:
    if state in state_population_dictionary:
      answer3 = str(int(state_return_dictionary[state]) / int(state_population_dictionary[state])*1000) 
      file.write(state +": ${:8.0f}".format(float(answer3))+ "\n")

  file.close()

  #*************************************************************************************
  # What state are the following questions for?
  #*************************************************************************************

  file = open("answers"+state_input+".txt", "a")

  get_state_name(state_codes, state_input)
  header = "\n"*2
  header += "="*60 + "\n"
  header += "State level informtion for "+ str(get_state_name(state_codes, state_input)) + "\n"
  header += "="*60 + "\n"

  file.write(header)

  file.close()

  #*************************************************************************************
  # What is the average taxable income per return across all groups?
  #*************************************************************************************

  number_of_returns = 0

  for i in tax_data:
    i[1] = i[1]
    if i[1] == state_input:
      number_of_returns += int(i[4])
    else:
      pass

  amount_of_taxable_income = 0

  for i in tax_data:
    i[1] = i[1]
    if i[1] == state_input:
      amount_of_taxable_income += int(i[96])
    else:
      pass

  answer4 = ((amount_of_taxable_income / number_of_returns)*1000)

  file = open("answers"+state_input+".txt", "a")

  file.write(answer_header(4, question_labels))
  #writes the answer for #4 to the file
  file.write("${:8.0f}".format( answer4 ) + "\n")

  file.close()

  #*************************************************************************************
  # What is the average taxable income per return for each agi group?
  #*************************************************************************************

  dic_of_AGI_return_numbers = {"1":0}

  for i in tax_data:
    if i[1] == state_input:
      if i[3] in dic_of_AGI_return_numbers:
        dic_of_AGI_return_numbers[i[3]] += int(i[4])
      elif i[3] not in dic_of_AGI_return_numbers:
        dic_of_AGI_return_numbers[i[3]] = int(i[4])
    else:
      pass
  
  dic_of_AGI_income_amount = {"1":0}

  for i in tax_data:
    if i[1] == state_input:
      if i[3] in dic_of_AGI_income_amount:
        dic_of_AGI_income_amount[i[3]] += int(i[96])
      elif i[3] not in dic_of_AGI_income_amount:
        dic_of_AGI_income_amount[i[3]] = int(i[96])
    else:
      pass
  
  file = open("answers"+state_input+".txt", "a")

  file.write(answer_header(5, question_labels))
  #writes the answer for #5 to the file
  for i in dic_of_AGI_income_amount:
    answer5 = ((dic_of_AGI_income_amount[i] / dic_of_AGI_return_numbers[i]) * 1000)
    file.write("Group "+ i +": ${:8.0f}".format(float(answer5))+ "\n")

  file.close()

  #*************************************************************************************
  # What is the average dependents per return for each agi group?
  #*************************************************************************************

  dic_of_AGI_return_numbers = {"1":0}

  for i in tax_data:
    if i[1] == state_input:
      if i[3] in dic_of_AGI_return_numbers:
        dic_of_AGI_return_numbers[i[3]] += int(i[4])
      elif i[3] not in dic_of_AGI_return_numbers:
        dic_of_AGI_return_numbers[i[3]] = int(i[4])
    else:
      pass

  dic_of_AGI_dependents = {"1":0}

  for i in tax_data:
    if i[1] == state_input:
      if i[3] in dic_of_AGI_dependents:
        dic_of_AGI_dependents[i[3]] += int(i[13])
      elif i[3] not in dic_of_AGI_dependents:
        dic_of_AGI_dependents[i[3]] = int(i[13])
    else:
      pass
  
  file = open("answers"+state_input+".txt", "a")

  file.write(answer_header(6, question_labels))
  #writes the answer for #6 to the file
  for i in dic_of_AGI_income_amount:
    answer6 = (dic_of_AGI_dependents[i] / dic_of_AGI_return_numbers[i])
    file.write("Group "+i+": {:8.2f}".format( answer6 ) + "\n")

  file.close()

  #*************************************************************************************
  # What is the percentage of returns with no taxable income per agi group?
  #*************************************************************************************

  dic_of_AGI_return_numbers = {"1":0}

  for i in tax_data:
    if i[1] == state_input:
      if i[3] in dic_of_AGI_return_numbers:
        dic_of_AGI_return_numbers[i[3]] += int(i[4])
      elif i[3] not in dic_of_AGI_return_numbers:
        dic_of_AGI_return_numbers[i[3]] = int(i[4])
    else:
      pass
  
  dic_of_AGI_taxable = {"1":0}

  for i in tax_data:
    if i[1] == state_input:
      if i[3] in dic_of_AGI_taxable:
        dic_of_AGI_taxable[i[3]] += int(i[95])
      elif i[3] not in dic_of_AGI_taxable:
        dic_of_AGI_taxable[i[3]] = int(i[95])
    else:
      pass
  
  file = open("answers"+state_input+".txt", "a")

  file.write(answer_header(7, question_labels))
  #writes the answer for #7 to the file
  for i in dic_of_AGI_income_amount:
    answer7 = (100*(1-(dic_of_AGI_taxable[i] / dic_of_AGI_return_numbers[i])))
    file.write("Group "+i+": {:8.2f}%".format( answer7 ) + "\n")

  file.close()

  #*************************************************************************************
  # What is the average taxable income per resident?
  #*************************************************************************************

  state_residents = int(state_population_dictionary[state_input])

  amount_of_taxable_income = 0

  for i in tax_data:
    if i[1] == state_input:
      amount_of_taxable_income += int(i[96])
    else:
      pass

  file = open("answers"+state_input+".txt", "a")

  file.write(answer_header(8, question_labels))
  #writes the answer for #8 to the file
  answer8 = (((amount_of_taxable_income / state_residents)*1000))
  file.write("${:8.0f}".format( answer8 ))

  file.close()
  
  #*************************************************************************************
  #What is the percentage of returns for each agi_group?  (as a percentage of total returns for that state)
  #*************************************************************************************

  total_state_returns = 0

  for i in tax_data:
    if i[1] == state_input:
      total_state_returns += int(i[4])
    else:
      pass

  dic_of_AGI_return_numbers = {"1":0}

  for i in tax_data:
    if i[1] == state_input:
      if i[3] in dic_of_AGI_return_numbers:
        dic_of_AGI_return_numbers[i[3]] += int(i[4])
      elif i[3] not in dic_of_AGI_return_numbers:
        dic_of_AGI_return_numbers[i[3]] = int(i[4])
    else:
      pass

  answer9_list = []

  for i in dic_of_AGI_income_amount:
    answer9_list.append(( "{0:.2f}".format((dic_of_AGI_return_numbers[i] / total_state_returns)*100)))

  file = open("answers"+state_input+".txt", "a")

  file.write(answer_header(9, question_labels))
  #writes the answer for #9 to the file
  for i in dic_of_AGI_income_amount:
    answer9 = ((dic_of_AGI_return_numbers[i] / total_state_returns)*100)
    file.write("Group "+i+": {:8.2f}%".format( answer9 ) + "\n")

  file.close()  

  #*************************************************************************************
  #What is the percentage of taxable income for each agi_group? (as a percentage of total taxable income for that state)
  #*************************************************************************************
  
  amount_of_taxable_income = 0

  for i in tax_data:
    if i[1] == state_input:
      amount_of_taxable_income += int(i[96])
    else:
      pass

  dic_of_taxable_income_AGI = {"1":0}

  for i in tax_data:
    if i[1] == state_input:
      if i[3] in dic_of_taxable_income_AGI:
        dic_of_taxable_income_AGI[i[3]] += int(i[96])
      elif i[3] not in dic_of_taxable_income_AGI:
        dic_of_taxable_income_AGI[i[3]] = int(i[96])
    else:
      pass

  answer10_list = []

  for i in dic_of_taxable_income_AGI:
    answer10_list.append( "{0:.2f}".format((dic_of_taxable_income_AGI[i] / amount_of_taxable_income)*100))

  file = open("answers"+state_input+".txt", "a")

  file.write(answer_header(10, question_labels))
  #writes the answer for #10 to the file
  for i in dic_of_taxable_income_AGI:
      answer10 = ((dic_of_taxable_income_AGI[i] / amount_of_taxable_income)*100)
      file.write("Group "+i+": {:8.2f}%".format( answer10 ) + "\n")

  file.close()

  #*************************************************************************************
  #Pie Chart 1
  #*************************************************************************************
  
  # Pie chart, where the slices will be ordered and plotted counter-clockwise:
  labels = "Group: 1", "Group: 2", "Group: 3", "Group: 4", "Group: 5", "Group: 6"
  sizes = answer9_list
  explode = (0, 0, 0, 0, 0, 0)

  fig1, ax1 = plt.subplots()
  ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.2f%%',
          shadow=True, startangle=90)
  ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
  plt.title("What is the percentage of returns for each agi_group?")
  plt.savefig('pie1_'+state_input+".png")
  
  #*************************************************************************************
  #Pie Chart 2
  #*************************************************************************************

  # Pie chart, where the slices will be ordered and plotted counter-clockwise:
  labels = "Group: 1", "Group: 2", "Group: 3", "Group: 4", "Group: 5", "Group: 6"
  sizes = answer10_list
  explode = (0, 0, 0, 0, 0, 0)

  fig1, ax1 = plt.subplots()
  ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.2f%%',
          shadow=True, startangle=90)
  ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
  plt.title("What is the percentage of taxable income for each agi_group?")
  plt.savefig('pie2_'+state_input+".png")
    
main()

