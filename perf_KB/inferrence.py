import mariadb
import sys
from datetime import date
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
affordRuleBook = []
cateRuleBook = []
phyRuleBook = []

class cateRule:
    def __init__(self, originalCate, originalId):
        self.originalCate = originalCate
        self.originalCateId = originalId
        self.affordFeatures = []
        self.affordFrequency = []
        self.physicalFeatures = []
        self.physicalFrequency = []

    def appendAfford(self, affordLabel, affordId):
        # check if it is existing first, and if not append. if exits, append the frequency only
        counter = 0
        categoryFlag = False
        for exitsingAfford in self.affordFeatures:
            if affordLabel == exitsingAfford[0]:
                categoryFlag = True
                break
            else:
                counter = counter + 1
        if categoryFlag == True:
            self.affordFrequency[counter] = self.affordFrequency[counter] +1
        else:
            new_afford = (affordLabel, affordId)
            self.affordFeatures.append(new_afford)
            self.affordFrequency.append(1)

    def appendPhysical(self, physicalLabel, physicalId):
        counter = 0
        physicalFlag = False
        for existingPhysical in self.physicalFeatures:
            if physicalLabel == existingPhysical[0]:
                physicalFlag = True
                break
            else:
                counter = counter + 1
        if physicalFlag == True:
            self.physicalFrequency[counter] = self.physicalFrequency[counter] + 1
        else:
            new_physical = (physicalLabel, physicalId)
            self.physicalFeatures.append(new_physical)
            self.physicalFrequency.append(1)


class affordRule:
    def __init__(self, originalAfford, originalId):
        self.originalAfford = originalAfford
        self.originalAffordId = originalId
        self.categoryFeatures = []
        self.categoryFrequency = []
        self.physicalFeatures = []
        self.physicalFrequency = []

    def appendCategory(self, categoryLabel, categoryId):
        # check if it is existing first, and if not append. if exits, append the frequency only
        counter = 0
        affordanceFlag = False
        for exitsingCategory in self.categoryFeatures:
            if categoryLabel == exitsingCategory[0]:
                affordanceFlag = True
                break
            else:
                counter = counter + 1
        if affordanceFlag == True:
            self.categoryFrequency[counter] = self.categoryFrequency[counter] +1
        else:
            new_category = (categoryLabel, categoryId)
            self.categoryFeatures.append(new_category)
            self.categoryFrequency.append(1)

    def appendPhysical(self, physicalLabel, physicalId):
        counter = 0
        physicalFlag = False
        for existingPhysical in self.physicalFeatures:
            if physicalLabel == existingPhysical[0]:
                physicalFlag = True
                break
            else:
                counter = counter + 1
        if physicalFlag == True:
            self.physicalFrequency[counter] = self.physicalFrequency[counter] + 1
        else:
            new_physical = (physicalLabel, physicalId)
            self.physicalFeatures.append(new_physical)
            self.physicalFrequency.append(1)
    #def appendPhysical(self, physicalLabel, physicalId):

    def printing(self):
        print(self.originalAfford, self.originalAffordId, len(self.categoryFrequency), len(self.physicalFeatures),
              len(self.categoryFrequency), len(self.categoryFeatures))



class physRule:
    def __init__(self, originalAfford, originalId):
        self.originalPhy = originalAfford
        self.originalPhyId = originalId
        self.categoryFeatures = []
        self.categoryFrequency = []
        self.affordFeatures = []
        self.affordFrequency = []

    def appendCategory(self, categoryLabel, categoryId):
         # check if it is existing first, and if not append. if exits, append the frequency only
         counter = 0
         affordanceFlag = False
         for exitsingCategory in self.categoryFeatures:
             if categoryLabel == exitsingCategory[0]:
                 affordanceFlag = True
                 break
             else:
                 counter = counter + 1
         if affordanceFlag == True:
             self.categoryFrequency[counter] = self.categoryFrequency[counter] +1
         else:
             new_category = (categoryLabel, categoryId)
             self.categoryFeatures.append(new_category)
             self.categoryFrequency.append(1)

    def appendAfford(self, affordLabel, affordId):
        # check if it is existing first, and if not append. if exits, append the frequency only
        counter = 0
        categoryFlag = False
        for exitsingAfford in self.affordFeatures:
            if affordLabel == exitsingAfford[0]:
                categoryFlag = True
                break
            else:
                ++counter
        if categoryFlag == True:
            self.affordFrequency[counter] = self.affordFrequency[counter] +1
        else:
            new_afford = (affordLabel, affordId)
            self.affordFeatures.append(new_afford)
            self.affordFrequency.append(1)





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
    # print(affordance_list)
    for items in affordance_list:
        object_list = create_get_object(str(items[1]), "affordance")
        if len(object_list) > 0:
            for each_id in object_list:
                object_id = str(each_id)
                query = "SELECT * FROM summary WHERE object_id = " + object_id + " AND affordance_label = 'null'"
                cur.execute(query)
                testingg = cur.fetchall()
                if len(testingg) > 0:
                    for testing in testingg:
                        flag = False
                        for x in affordRuleBook:
                            target = x.originalAfford
                            if items[0] == target:
                                flag = True
                        if flag is False:
                            """New affordance"""
                            rule = affordRule(items[0], str(items[1]))
                            rule.appendCategory(testing[10], testing[11])
                            rule.appendPhysical(testing[1], testing[7])
                            affordRuleBook.append(rule)
                            # print(items[0], items[1])
                            # print(rule.categoryFeatures, rule.categoryFrequency, rule.physicalFeatures, rule.physicalFrequency)
                            #
                            #
                            # new_pair = f"c___{each_result[10]}___{each_result[11]}"
                            # features.append(new_pair)
                            # new_pair = f"p___{each_result[1]}___{each_result[7]}"
                            # features.append(new_pair)
                        else:
                            for rule in affordRuleBook:
                                if rule.originalAfford == items[0]:
                                    #found
                                    rule.appendCategory(testing[10], testing[11])
                                    rule.appendPhysical(testing[1], testing[7])

    #TODO: UNCOMMENT for printing
    #print_DICT(affordRuleBook, "affordance")

                        #if entered this else, means there already exits the entry. therefore append the list
                    # create_DictLine(items, testing, "affordance")
                    #creating the line to insert in Rule Book
    #case 2 : category
    category_list = []
    query = "SELECT category_label, category_id FROM category"
    cur.execute(query)
    category_raw_list = cur.fetchall()
    for items in category_raw_list:
        each_tuple = (items[0], items[1])
        category_list.append(each_tuple)
    for items in category_list:
        object_list = create_get_object(str(items[1]), "category")
        if len(object_list) > 0:
            for each_id in object_list:
              object_id = str(each_id)
              query = "SELECT * FROM summary WHERE object_id = " + object_id + " AND category_id = " + str(items[1])
              cur.execute(query)
              testingg = cur.fetchall()
              #print(testing)
              if len(testingg) > 0:
                  for testing in testingg:
                      flag = False
                      for x in cateRuleBook:
                          target = x.originalCate
                          if items[0] == target:
                              flag = True
                      if flag is False:
                        """New category"""
                        rule = cateRule(items[0], str(items[1]))
                        rule.appendAfford(testing[2], testing[8])
                        rule.appendPhysical(testing[1], testing[7])
                        cateRuleBook.append(rule)
                        # print(items[0], items[1])
                        # print(rule.categoryFeatures, rule.categoryFrequency, rule.physic
                        #
                        #
                        # new_pair = f"c___{each_result[10]}___{each_result[11]}"
                        # features.append(new_pair)
                        # new_pair = f"p___{each_result[1]}___{each_result[7]}"
                        # features.append(new_pair)
                      else:
                        for rule in cateRuleBook:
                            if rule.originalCate == items[0]:
                                #found
                                rule.appendAfford(testing[2], testing[8])
                                rule.appendPhysical(testing[1], testing[7])
                                break

    #print_DICT(cateRuleBook, "category")


    #case 3 : physical
    physical_list = []
    query = "SELECT physical_label, physical_id FROM physical"
    cur.execute(query)
    physical_raw_list = cur.fetchall()
    for items in physical_raw_list:
        each_tuple = (items[0], items[1])
        physical_list.append(each_tuple)
    for items in physical_list:
        object_list = create_get_object(str(items[1]), "physical")
        if len(object_list) > 0:
             for each_id in object_list:
               object_id = str(each_id)
               query = "SELECT * FROM summary WHERE object_id = " + object_id + " AND physical_id = " + str(items[1])
               cur.execute(query)
               testingg = cur.fetchall()
               # print(testingg)
               if len(testingg) > 0:
                   for testing in testingg:
                       flag = False
                       for x in phyRuleBook:
                           target = x.originalPhy
                           if items[0] == target:
                               flag = True
                       if flag is False:
                         """New physical"""
                         rule = physRule(items[0], str(items[1]))
                         rule.appendAfford(testing[2], testing[8])
                         rule.appendCategory(testing[10], testing[11])
                         phyRuleBook.append(rule)
                         # print(items[0], items[1])
                         # print(rule.categoryFeatures, rule.categoryFrequency, rule.physic
                         #
                         #
                         # new_pair = f"c___{each_result[10]}___{each_result[11]}"
                         # features.append(new_pair)
                         # new_pair = f"p___{each_result[1]}___{each_result[7]}"
                         # features.append(new_pair)
                       else:
                         for rule in phyRuleBook:
                             if rule.originalPhy == items[0]:
                                 #found
                                 rule.appendAfford(testing[2], testing[8])
                                 rule.appendCategory(testing[10], testing[11])
                                 break

    #print_DICT(phyRuleBook, "physical")
    
def print_DICT(dictionary, kind):
    if kind == "affordance":
        for items in dictionary:
            print(items.originalAfford, items.originalAffordId, items.categoryFrequency,
                  items.categoryFeatures, items.physicalFrequency, items.physicalFeatures)
    if kind == "category":
        for items in dictionary:
            print(items.originalCate, items.originalCateId, items.affordFrequency, items.affordFeatures)
    if kind == "physical":
        for items in dictionary:
            print(items.originalPhy, items.originalPhyId, items.categoryFrequency, items.categoryFeatures)


def create_DictLine():
    """append the content to the dictionary
        <label>___<id>
        /features: c___<sample1>.<id1>___<frequency>, p___<sample2>___<id2>, ... continues if more
        dictionary naming : today's date/time_<category,physical,affordance>RuleBook
    """
    time_stamp = date.today()

    # affordRuleBook = []
    # cateRuleBook = []
    # phyRuleBook = []

    # affordance
    filename = "Afford Rule Book " + str(time_stamp)
    f = open(filename, "w")
    for items in affordRuleBook:
        line = items.originalAfford + "___" + items.originalAffordId + "\n"
        line = line + "/features: "
        for i in range(len(items.categoryFrequency)):
            # print(items.originalAfford, items.categoryFrequency[i], items.categoryFeatures[i])
            line = line + "c___" + (items.categoryFeatures[i])[0] + "." + str((items.categoryFeatures[i])[1]) + "___" + str((items.categoryFrequency[i])) + ", "
        for j in range(len(items.physicalFeatures)):
            # print(items.physicalFeatures[i], items.physicalFrequency[i])
            line = line + "p___" + (items.physicalFeatures[j])[0] + "." + str((items.physicalFeatures[j])[1]) + "___" + str((items.physicalFrequency[i])) + ", "
        line = line + "\n"
        print(line)
        f.writelines(line)

    # category
    filename = "Category Rule Book " + str(time_stamp)
    f2 = open(filename, "w")
    for items in cateRuleBook:
        line = items.originalCate + "___" + items.originalCateId + "\n"
        line = line + "/features: "
        for i in range(len(items.affordFrequency)):
            line = line + "a___" + (items.affordFeatures[i])[0] + "." + str((items.affordFeatures[i])[1]) + "___" + str((items.affordFrequency[i])) + ", "
        for j in range(len(items.physicalFrequency)):
            line = line + "p___" + (items.physicalFeatures[j])[0] + "." + str((items.physicalFeatures[j])[1]) + "___" + str((items.physicalFrequency[j])) + ", "
        line = line + "\n"
        f2.writelines(line)

    # physical
    filename = "Physical Rule Book " + str(time_stamp)
    f3 = open(filename, "w")
    for items in phyRuleBook:
        line = items.originalPhy + "___" + items.originalPhyId + "\n"
        line = line + "/features: "
        for i in range(len(items.affordFrequency)):
            line = line + "a___" + (items.affordFeatures[i])[0] + "." + str((items.affordFeatures[i])[1]) + "___" +\
                   str((items.affordFrequency[i])) + ", "
        for j in range(len(items.categoryFeatures)):
            line = line + "c___" + (items.categoryFeatures[j])[0] + "." + str((items.categoryFeatures[j])[1]) + "___" +\
                   str((items.categoryFrequency[j])) + ", "
        line = line + "\n"
        f3.writelines(line)








def create_get_object(id, kind):
    """purpose of the function is to return the list of objects that are applicable
    returns the list of object_id associated with the attribute
     case 1: affordance perspective
     case 2: category perspective
     case 3: physical perspective
     """
    object_list = []
    if kind == "affordance":
        query = "SELECT relation.object_id FROM relation WHERE relation.affordance_id =" + id
        cur.execute(query)
        object_acquired = cur.fetchall()
        for items in object_acquired:
            object_list.append(items[0])
        return object_list
    elif kind == "category":
        query = "SELECT summary.object_id FROM summary WHERE summary.category_id =" + id 
        cur.execute(query)
        object_acquired = cur.fetchall()
        for items in object_acquired:
            object_list.append(items[0])
        return object_list
    elif kind == "physical":
        query = "SELECT summary.object_id FROM summary WHERE summary.physical_id =" + id
        cur.execute(query)
        object_acquired = cur.fetchall()
        for items in object_acquired:
            object_list.append(items[0])
        return object_list
