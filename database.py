import mariadb
import sys
Host = "localhost"
User = "root"
Password ="1234"
database = "ure-suzinoh"

try:
    conn =mariadb.connect(
        user="root",
        password="1234",
        host="127.0.0.1",
        port = 3306,
        database = "ure-suzinoh"
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB platform: {e}")
    sys.exit(1)

cur = conn.cursor()


def add_category(po: list):
    #done
    max_length = len(po)
    for i in range(0, max_length):
        category_id = i
        label = po[i]
        descript = 'empty'
        query = f"INSERT INTO category (category_id, category_label, category_description) VALUES ('{category_id}', '{label}', '{descript}')"
        cur.execute(query)
        conn.commit()


def split_affordance(string):
    """splitting the affordance with the label and active/passive option for inserting in db"""
    splitting = string.split(',')
    label = splitting[0]
    is_active = "true"
    if splitting[1] == " passive":
        is_active = "false"
    return label, is_active;


def add_affordance(po: list):
    index = 0
    #done
    for item in po:
        label, is_active = split_affordance(item)
        affordance_id = index
        descript = 'empty'
        query = f"INSERT INTO affordance (affordance_id, affordance_label, affordance_description, is_active)" \
                f" VALUES ('{affordance_id}', '{label}', '{descript}', {is_active})"
        cur.execute(query)
        index = index + 1
        conn.commit()


def split_physical(string):
    splitting = string.split(',')
    category = splitting[1].replace(" ", "")
    executeStr = "SELECT physical_category_id FROM physical_attributes WHERE physcial_category_label ='" + category + "'"
    cur.execute(executeStr)
    query_category = cur.fetchall()
    category_id = query_category[0]
    return splitting[0], category_id[0]


def add_physical(po: list):
    physical_id = 0
    for current_list in po:
        current_dictionary = po[current_list]
        for item in current_dictionary:
            label, category_id = split_physical(item)
            descript = 'empty'
            query = f"INSERT INTO physical (physical_id, physical_label, physical_description, physical_subcategory)" \
                    f" VALUES ({physical_id}, '{label}', '{descript}', {category_id})"
            cur.execute(query)
            physical_id = physical_id + 1
            conn.commit()


def get_object_category(filename):
    f = open(filename, "r")
    lines = f.readlines()
    pairs = []
    words = []
    iss = []
    defs = []
    replacing = ["(", ")", " ", "is_a", ".", "\n",","]
    word, definition, is_a = "", "",""
    for each_line in lines:
        if "is_a" not in each_line and "has_" not in each_line and "has_function" not in each_line and "has_affordance" not in each_line and "%definition:" not in each_line and "has_Affordance" not in each_line and "." not in each_line and len(each_line)!=1:
            # testing: print(each_line)
            word = each_line
            word = word.replace("\n", "")
            word = word.lower()
            words.append(word)
        if "%def" in each_line:
            definition = each_line
            definition = definition.replace("%definition: ", "")
            definition = definition.replace("\n", "")
            # testing: print(definition, "\n")
            defs.append(definition)
        if "is_a" in each_line:
            # print(each_line)
            is_a = each_line
            for item in replacing:
                is_a = is_a.replace(item, "")
                is_a = is_a.replace(word, "")
            # testing: print(word, is_a)
            iss.append(is_a)
            tup = (word, is_a, definition)
            pairs.append(tup)

    return pairs


def get_category_id(category):
    query = f"SELECT category_id FROM category WHERE category_label = '{category}'"
    cur.execute(query)
    categoryid = cur.fetchall()
    return categoryid[0][0]


def add_object():
    dictionaries = ["dictionary_1_perf_2022-09-07", "dictionary_2_perf_2022-09-12", "dictionary_3_perf_2022-09-12",
                    "dictionary_4_perf_2022-09-13"]
    #TODO: dict1, dict2 done
    dictionary = dictionaries[3]
    pairs = get_object_category(dictionary)
    id = 633
    for item in pairs:
        cat_id = get_category_id(item[1])
        if "'" not in item[2]:
            description = item[2]
        else:
            description = "empty : error handling"
        query = f"INSERT INTO object (object_id, object_label, object_description, object_category)" \
                 f" VALUES ('{id}', '{item[0]}', '{description}', '{cat_id}')"
        cur.execute(query)
        id = id+1
        print(cat_id, item[0])
        conn.commit()


def get_new_index(key):
    #TODO: get the function working with other tables too
    if key == "affordance":
        query = f"SELECT MAX(affordance_id) FROM affordance"
        cur.execute(query)
        index = cur.fetchall()
        return(index[0][0])
    elif key == "physical":
        query = f"SELECT MAX(physical_id) FROM physical"
        cur.execute(query)
        index = cur.fetchall()
        return(index[0][0])
    elif key =="relation":
        query = f"SELECT MAX(relation_id) FROM relation"
        cur.execute(query)
        index = cur.fetchall()
        return(index[0][0])

def new_affordance_insert(new_afford_file):
    """ def new_affordance_insert is a function that take in the file, "New_Affordance_xx",
    which contains the lists of new added affordances that were detected and deisred to be inserted
    to the database, and insert the rows to the database
    """
    replacing = ["has_affordance", "has_function", "(", ")", "."]
    read = open(new_afford_file, "r")
    word, afford = "", ""
    tuples=[]
    # TODO: get the max value from the affordance id column, increment the index, insert the affordance
    for each_line in read:
        if "has_" not in each_line:
            word = each_line
            word = word.replace("\n","")
        else:
            afford = each_line
            afford = afford.lower()
        if word and afford:
            #word and affordance detected, get label
            afford = afford.replace(word, "")
            for item in replacing:
                afford = afford.replace(item, "")
            afford = afford.replace(",", "", 1)
            segmented = afford.split(",")
            print(segmented)
            #removing the space from the first element of affordance
            label = segmented[0]
            if label[0] == " ":
                label = label.replace(" ", "", 1)
            is_active = segmented[1].replace("\n", "")
            is_active = is_active.replace(" ","")
            label = label.replace("'","")
            newtup = (label, is_active)
            tuples.append(newtup)
            word, afford = "",""
    f = open("affordance", "a")
    f.write("\n")
    index = get_new_index("affordance")+1
    descript = "empty"
    for items in tuples:
        if items[1] == "active":
            is_active = True
        else:
            is_active = False
        query = f"INSERT INTO affordance (affordance_id, affordance_label, affordance_description, is_active)" \
                f" VALUES ('{index}', '{items[0]}', '{descript}', {is_active})"
        print(query)
        cur.execute(query)
        index = index + 1
        conn.commit()
        newline = items[0] + ", " + items[1] + "\n"
        f.write(newline)
    #appedning the .txt
    f = open("affordance", "a")


def query_object(word):
    """queries the object from the object table"""
    query = f"SELECT object_id FROM object WHERE object_label = '{word}'"
    cur.execute(query)
    object_id = cur.fetchall()
    # object_id = object_id[0][0]
    print(object_id)
    return object_id

def query_affordance(affordance):
    query = f"SELECT affordance_id FROM affordance WHERE affordance_label = '{affordance}'"
    cur.execute(query)
    affordance_id = cur.fetchall()
    affordance_id = affordance_id[0][0]
    return affordance_id

def query_object_affordance(word, affordance):
    success = True

    # except:
    #     print("error at affordance")


def inserting_linked_affordance():
    replace = ["has_affordance", "has_", "has_function", ".", "'", "\n"]
    #steps: read each line by line get the object number and affordance number
    f = open("dictionary_1_perf_2022-09-07_temp2022-09-15", "r")
    lines = f.readlines()
    word, affordance = "", ""
    for each_line in lines:
        if len(each_line) < 15:
            word = each_line.replace("\n", "")
            word = each_line.replace(".", "")
            word = word.lower()
        elif "has_" in each_line:
            check = each_line[:12:].lower()
            affordance = each_line[12::].replace("\n","")
            if "function" in check or "afford" in check:
                if "active" in affordance:
                    affordance = affordance + " 1"
                    splitting = affordance.split(",")
                    affordance = splitting[1]
                if "passive" in affordance:
                    affordance = affordance + " 0"
                    splitting = affordance.split(",")
                    affordance = splitting[1]
                word = word.replace("\n","")
                affordance = affordance.replace("'","")
                affordance = affordance.replace(" ","",1)
                if "(" not in affordance:
                    print(word)
                    query_object(word)
                    # print(affordance)
                    # query_affordance(affordance)
                    # query_object_affordance(word, affordance)




def new_physical_insert(new_physicals):
    replacing = ["has_", "has_function", "(", ")", "."]