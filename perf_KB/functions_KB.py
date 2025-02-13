from datetime import date
from pathlib import Path
"""knolwedge base related functions stored here"""

"""po is shortened term for possible options. gets populated by def populate with lists in file """
po = {
    "category": [],
    "affordance": [],
    "property": {
        "state": [],
        "shape": [],
        "color": [],
        "material": [],
        "weight": [],
        "hardness": [],
        "hazardous": [],
        "texture": []
    }
        # state, shape, color, material, weight, hardness, hazardous

}


def populate():
    # populating categories
    f = open("categories", "r")
    lines = f.readlines()
    for each in lines:
        each=each.replace("\n", "")
        if each not in po["category"]:
            po["category"].append(each)
    f.close()

    # populating affordance
    f = open("affordance", "r")
    lines = f.readlines()
    for each in lines:
        each = each.replace("\n", "")
        if each not in po["affordance"]:
            po["affordance"].append(each)
    f.close()

    # populating physical property
    f = open("physical", "r")
    lines = f.readlines()
    for each in lines:
        # state, shape, color, material, weight, hardness, hazardous
        if "state" in each:
            each = each.replace("\n", "")
            po["property"]["state"].append(each)
        elif "shape" in each:
            each = each.replace("\n", "")
            po["property"]["shape"].append(each)
        elif "color" in each:
            each = each.replace("\n", "")
            po["property"]["color"].append(each)
        elif "material" in each:
            each = each.replace("\n", "")
            po["property"]["material"].append(each)
        elif "weight" in each:
            each = each.replace("\n", "")
            po["property"]["weight"].append(each)
        elif "hardness" in each:
            each = each.replace("\n", "")
            po["property"]["hardness"].append(each)
        elif "hazardous" in each:
            each = each.replace("\n", "")
            po["property"]["hazardous"].append(each)
        elif "texture" in each:
            each = each.replace("\n", "")
            po["property"]["texture"].append(each)
    f.close()



def append_choice(element, list):
    command = input("new element: " , element, "detected. ","\n","TYPE Y if adding to list:")
    if command == "Y":
        list.append(element)
        #TODO: before closing the file, check if the list matches the original content. if not, append


def split_kb(ordered, key_list):
    dictionary = open("../dicts/dictionary_1", "w")
    for i in range(0, 199):
        dictionary.write(key_list[i])
        dictionary.write("\n")
        dictionary.write(ordered[key_list[i]])
        dictionary.write("\n")
    dictionary = open("../dicts/dictionary_2", "w")
    for i in range(200, 399):
        dictionary.write(key_list[i])
        dictionary.write("\n")
        dictionary.write(ordered[key_list[i]])
        dictionary.write("\n")
    dictionary = open("../dicts/dictionary_3", "w")
    for i in range(400, 599):
        dictionary.write(key_list[i])
        dictionary.write("\n")
        dictionary.write(ordered[key_list[i]])
        dictionary.write("\n")
    dictionary = open("../dicts/dictionary_4", "w")
    for i in range(600, 671):
        dictionary.write(key_list[i])
        dictionary.write("\n")
        dictionary.write(ordered[key_list[i]])
        dictionary.write("\n")


def check_existing_category(category):
    for item in  po["category"]:
        if category == item:
            return True
    else:
        return False


def check_existing_affordance(rest):
    for item in po["affordance"]:
        if rest == item:
            return True
    else:
        return False


def verify_affordance(input_afford):
    """verifying the new inputted affordance if they exist in the possible option"""
    counter = 0
    for item in po["affordance"]:
        if item.find(input_afford) != -1:
            print("replacing the old Affordance with ", item)
            return item
    else:
        return -1


def verify_property(possible, verifying, original_word):
    """function for verifying from the possible list and replace
    goal is to replace if the property is incorrect"""
    print(verifying)
    flag = False
    final ="has_property"
    for item in possible:
        if verifying == item:
            flag = True
    if flag == True:
        print("no change in physical property")
        final = final + "(" + original_word + ", " + verifying + ")"
        return final
    else:
        print("attributes needs change: select from avaliable property")
        #display options...with number and get input of number
        for i in range(0, len(possible)):
            print(i, ". ", possible[i])
        index = input("Enter the index of property desired, if the property needs to be added enter 100 : \n")
        if index != "100":
            final = final + "(" + original_word +", " + possible[int(index)] + ")\n"
        else:
            f = open("New_Physical", "a")
            f.write(original_word)
            f.write(verifying)
        print(final)
        return final


def perfecting_category(filename):
    replace = ["is_a", "(", ")", " ", ".", ",", "\n"]
    choice_list = po["category"]
    f = open(filename, "r")
    # getting today's date and adding to file name
    today = date.today()
    newfile = filename + "_perf_" + str(today)
    path = Path(newfile)
    flag = True
    # uncomment when the file is all perfected
    # if path.is_file():
    #     print("file have been previously perfected")
    #     return None
    # else:
    if flag is True:
        f2 = open(newfile, "w")
        lines = f.readlines()
        word = ""
        for each_line in lines:
            if "is_a" not in each_line and "has_" not in each_line and "has_function" not in each_line and "has_affordance" not in each_line and "%definition:" not in each_line and "has_Affordance" not in each_line and "." not in each_line:
                word = each_line.replace("\n", "")
                word = word.lower()
                print(word)
            if "%def" in each_line:
                definition = each_line
            if "is_a" in each_line:
                category = each_line
                for item in replace:
                    category = category.replace(word, '')
                    category = category.replace(item, '')
                if check_existing_category(category) is False:
                    print("---> incorrect category please reconfigure category to replace ", category, "for ", word)
                    print(definition)
                    print(choice_list)
                    new_category = input("---> enter new category: ")
                    if new_category not in choice_list:
                        print("**new category** keeping the original category \n")

                    else:
                        each_line = "is_a(%s, %s).\n" % (word, new_category)
            f2.write(each_line)


def perfecting_affordance(filename):
    """take in dictionary_#_perf, and replace the function part to affordance and fix the errors"""
    replace = ["has_affordance", "has_Affordance", "has_accordance", "(", ")", " ", ".", ",", "\n"]
    new_filename = ("New_Affordances") + str(date.today())
    #fnew == prothas new affordances
    fnew = open(new_filename, "w")
    f = open(filename, "r")
    today = str(date.today())
    temp = filename+"_temp"+today
    f2 = open(temp, "w")
    for each_line in f:
        # combining the function with affordance
        if len(each_line) < 15:
            word = each_line.replace("\n","")
            word = word.lower()
            replace.append(word)
        if "%def" in each_line:
            definition = each_line
        check = each_line[:12:]
        rest = each_line[12::]
        if check!="has_function":
            f2.write(each_line)
        else:
            for item in replace:
                rest = rest.replace(item, '')
            if check_existing_affordance(rest) is False:
                newline = ""
                # TODO: must support the case where having affordance does not make sense... ex) superman.
                print("---> incorrect AFFORDANCE please reconfigure Affordance to replace ", rest, " for ", word)
                print(definition)
                print(po["affordance"])
                # TODO: new affordance adding feature supported?
                new_category = input("---> enter new Affordance. if new affordance, enter 'add' : ")
                if new_category == "add":
                    print("do smth to handle the new affordance being added")
                    #keeping the original
                    newline = each_line
                    f2.write(newline)
                    fnew.write(word)
                    fnew.write("\n")
                    fnew.write(newline)
                else:
                    verified = verify_affordance(new_category)
                    if verified != -1:
                        new_affordance = verified
                        rest = "(" + word + ", " + new_affordance + ")"
                        newline = "has_affordance" + rest + "\n"
                    else:
                        print("*** affordance not specified ***")
                    if verified != "delete, delete":
                        f2.write(newline)
    f2.close()
    fnew.close()


def perfecting_property(filename):
    """physical attributes are attributes that defines the characteristic of an object
    for example, shape, color, weight etc.
    in the kb physical attributes are labeled with has_property
    """
    #TODO: popualte the po with "physical", make the perfecting easier by looking labels like color, shape etc.
    replace = ["has_property","(",")"," ",".",",","\n"]

    #read the file and separate out the definition, word, and the physical property in order to perf it
    f = open(filename, "r")
    today = str(date.today())
    temp = filename + "_phy_" + today
    f2 = open(temp, "w")
    for each_line in f:
        if len(each_line) < 15:
            word = each_line.replace("\n", "")
            word = word.lower()
            replace.append(word)
        if "%def" in each_line:
            definition = each_line
        check =each_line[:12:]
        rest =each_line[12::]
        property_line = ""
        #TODO: add functionality where some categories do not need an property field! - refer to the planning on Notion
        if check!="has_property":
            #if not has_property, continue
            f2.write(each_line)
        elif check =="has_property":
            print(word, "\n", definition)
            #if it is property, check property (state, shape, color, material, weight, hardness, hazardous)
            if "state" in rest:
                property_line = verify_property(po["property"]["state"], rest, word)
            elif "shape" in rest:
                property_line = verify_property(po["property"]["shape"], rest, word)
            elif "color" in rest:
                property_line = verify_property(po["property"]["color"], rest, word)
            elif "material" in rest:
                property_line = verify_property(po["property"]["material"], rest, word)
            elif "weight" in rest:
                property_line = verify_property(po["property"]["weight"], rest, word)
            elif "hardness" in rest:
                property_line = verify_property(po["property"]["hardness"], rest, word)
            elif "hazardous" in rest:
                property_line = verify_property(po["property"]["hazardous"], rest, word)
            elif "texture" in rest:
                property_line = verify_property(po["property"]["texture"],rest, word)
            f2.write(property_line)
