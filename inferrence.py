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

def create_rule_book():
    """using the relation that is already existing in the database, creating
     aka. rule book to check and use it as reference when inferring the unknown

     HOW:
        traversing through the list of all affordance,category, and physical labels.
        we will put them as WHERE clause in the query
        after getting the DISTICT ones, we can append them to the file

    THREE CASES: searching regarding...
        1. affordance
        2. category
        3. physical attributes

    FORMAT:
        how should i store it?
        <label>___<id>/features: <sample1>___<id1>, <sample2>___<id2>, ... continues if more
     """
    # open file as appending option
    affordance_book = open("Rule Book - affordance", "a")
    category_book = open("Rule Book - category", "a")
    physical_book = open("Rule Book - physical", "a")

    #case 1 : affordance
    affordance_list = []
    query = "SELECT affordance_label, affordance_id FROM affordance"
    cur.execute(query)
    affordance_raw_list = cur.fetchall()
    for items in affordance_raw_list:
        each_tuple = (items[0], items[1])
        affordance_list.append(each_tuple)
    for items in affordance_list:
        query = f"SELECT "
    #case 2 : category
    category_list = []
    query = "SELECT category_label, category_id FROM category"
    cur.execute(query)
    category_raw_list = cur.fetchall()
    for items in category_raw_list:
        each_tuple = (items[0], items[1])
        category_list.append(each_tuple)

    #case 3 : physical
    physical_list = []
    query = "SELECT physical_label, physical_id FROM physical"
    cur.execute(query)
    physical_raw_list = cur.fetchall()
    for items in physical_raw_list:
        each_tuple = (items[0], items[1])
        physical_list.append(each_tuple)


def create_get_object(id, kind):
    """purpose of the function is to return the list of objects that are applicable
    returns the list of object_id associated with the attribute
     case 1: affordance perspective
     case 2: category perspective
     case 3: physical perspective
     """
    object_list = []
    if kind is "affordance":
        query = "SELECT relation.object_id FROM relation WHERE relation.affordance_id =" + id
        cur.execute(query)
        object_acquired = cur.fetchall()
        for items in object_acquired:
            object_list.append(items[0])
        return object_list
    elif kind is "category":
        query = "SELECT relation.object_id FROM relation WHERE relation.affordance_id =" + id
    elif kind is "physical":
        query = "SELECT relation.object_id FROM relation WHERE relation.physical_id =" + id
        cur.execute(query)
        object_acquired = cur.fetchall()
        for items in object_acquired:
            object_list.append(items[0])
        return object_list