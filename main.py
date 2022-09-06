# TODO: import the files and organize by alphabetical ord
import os
import functions_KB as functions_KB
import database as db
# from data_structure import ObjectNode

directory = 'C:/Users/suzin/OneDrive/Documents/WSU/Research/KnolwedgeBase'
filelist = []
for filename in os.scandir(directory):
    if filename.is_file():
        filelist.append(filename)
ordered = {}
key_list = []
# reading the file using the file list name
# TODO: have some check (amount of lines in the files accumulated is same length as total line outputted)
for i in range(len(filelist)):
    f = open(filelist[i], 'r')
    lines = f.readlines()
    for each_line in lines:
        if "%word" in each_line:
            word = each_line[6:-1:]
            replace = ""
            for character in word:
                if (character != " ") and (character != ":"):
                    replace = replace + character
            word = replace
        elif "%def" in each_line:
            definition = each_line
        elif not len(each_line)<3:
            definition = definition + each_line
        else:
            ordered[word] = definition
            definition = ""
            if word not in key_list:
                key_list.append(word)
#total length of the words are  672, splitting it by 100, use function_KB, split_kb if needed

# TODO: need to make sure each dict item's description is valid, options should be limited
functions_KB.populate()
#functions_KB.perfecting_category("dictionary_1")
#functions_KB.perfecting_affordance("dictionary_2")
#functions_KB.perfecting_property("dictionary_2")

#adding to the database: commented ones are already done
#db.add_category(functions_KB.po["category"])
#db.add_affordance(functions_KB.po["affordance"])
db.add_physical(functions_KB.po["property"])
# combine them into one file instead of separate files
