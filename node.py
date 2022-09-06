"""
node.py contains class defnition for the Node Object, and different functions needed for differentiating nodes

something to consider:
    1. not all categories should be made into same node
        a. object node - objects, plant, etc.. most
        b. classes that need to be differentiated :
            action
            term
            property
            for now, just focus on the object node and deal with any category with action etc. later
    2. before getting into object, make nodes for the category, affordance, and physical first
        a. make them first so we can later conenct
    3. how are we storing the network
"""
class category:

class physical:

class affordance:

class Node:
    def __init__(self, type, name, description, category, physical, affordance):
        self.type = type
        self.id
        self.name = name
        self.description = description
        self.category = category
        self.physical = physical
        self.affordance = affordance
