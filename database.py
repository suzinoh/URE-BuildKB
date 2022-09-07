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

def add_object(po: list):
    print("adding the object. roadblock: complete the perf. of the dictionary and laod the dictionary item in the future")