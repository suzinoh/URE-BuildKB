# TODO: import the files and organize by alphabetical ord
import os

import database
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
        elif not len(each_line) < 3:
            definition = definition + each_line
        else:
            ordered[word] = definition
            definition = ""
            if word not in key_list:
                key_list.append(word)
# total length of the words are  672, splitting it by 100, use function_KB, split_kb if needed

# TODO: need to make sure each dict item's description is valid, options should be limited
functions_KB.populate()
#"dictionary_1_perf_2022-09-07"
#"dictionary_2_perf_2022-09-12"
#"dictionary_3_perf_2022-09-12"
#"dictionary_4_perf_2022-09-13"
dict_list = ["dictionary_1_perf_2022-09-07_temp2022-09-15", "dictionary_2_perf_2022-09-12_temp2022-09-19",
             "dictionary_3_perf_2022-09-12_temp2022-09-20","dictionary_4_perf_2022-09-13_temp2022-09-21"]
# perfecting the category, last perfected 09092022
# for item in dict_list:
#     functions_KB.perfecting_category(item)
#     print("finished the dictionary: ", item)
# functions_KB.perfecting_affordance("dictionary_2")
# functions_KB.perfecting_property("dictionary_2")

# perfecting the affordance,
# dict list updated to the category_perfected dictionaries
#       "dictionary_1_perf_2022-09-07", "dictionary_2_perf_2022-09-12", "dictionary_3_perf_2022-09-12", "dictionary_4_perf_2022-09-13"

# database.new_affordance_insert("New_Affordances2022-09-15")

# for item in dict_list:
#     functions_KB.perfecting_affordance(item)

functions_KB.perfecting_property(dict_list[1])

#TODO: onhold, 09212022 for the linking part :<
# database.inserting_linked_affordance()




# adding to the database: commented ones are already done
# TODO: get object in and relations in. (needs perf)
# db.add_category(functions_KB.po["category"])
# db.add_affordance(functions_KB.po["affordance"])
# db.add_physical(functions_KB.po["property"])
# database.add_object()
# combine them into one file instead of separate files
