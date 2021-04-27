## import modules here 
import math
################# Question 0 #################

def add(a, b): # do not change the heading of the function
    return a + b


################# Question 1 #################

def nsqrt(x): # do not change the heading of the function
    # Using Binary Search
    # initialise the start and end integer
    start = 1
    end = x
    ans = 0
    while start <= end:
        # find the middle value of start and end
        mid = int((start+end)/2)
        # if res equal to target, return the value
        if mid*mid == x:
            return mid
        elif mid*mid < x:
            start = mid + 1 # if res smaller than x, we add 1 to start
            ans = mid # we need a floor value, we set ans to be the value that mid*mid smaller than x 
        else:
            end = mid - 1 # if res larger than x, we minus 1 to end
    return ans


################# Question 2 #################


# x_0: initial guess
# EPSILON: stop when abs(x - x_new) < EPSILON
# MAX_ITER: maximum number of iterations

## NOTE: you must use the default values of the above parameters, do not change them

def find_root(f, fprime, x_0=1.0, EPSILON = 1E-7, MAX_ITER = 1000): # do not change the heading of the function
    x = x_0
    i = 0
    while i < MAX_ITER:
        x_prev = x
        x = x - f(x)/fprime(x)
        if abs(x-x_prev) < EPSILON:
            return x
        i += 1
        
    return x


################# Question 3 #################

class Tree(object):
    def __init__(self, name='ROOT', children=None):
        self.name = name
        self.children = []
        if children is not None:
            for child in children:
                self.add_child(child)
    def __repr__(self):
        return self.name
    def add_child(self, node):
        assert isinstance(node, Tree)
        self.children.append(node)

def make_tree(tokens): # do not change the heading of the function
    # length of the string
    str_len = len(tokens)
    # define an index to walk through the tokens
    i = 0
    # level stands for the layer index of the tree
    level = 0
    # create a 2D list for each level to store nodes which are in the same level
    level_list = []
    level_list.insert(level,[])
    
    # create a list to store an index for each level 
    # which will be used to distinguish childern for different parents
    level_index_list = []
    level_index_list.insert(level, 0)
    
    # start the loop
    while i < str_len:
        # Whenever we meet a '[', it means the tree treverse to a new deeper level (Top to down)
        # And we need to create a new level in level_list
        # the default level_index will be 0
        if tokens[i] == '[':
            level += 1
            level_list.insert(level, [])
            level_index_list.insert(level, 0)
            
        # Whenever we meet a ']', it means one or a set of childern for a parent node have been determined
        # And we need to connect those childern to the parent
        # Since this is a pre-order tree,
        # we know that the parent node must be the last inserted node on the upper level
        # For the set of childern, we start from the level_index to the end 
        # because the childern we want to add must be those which add in the last place starting from level_index
        # because after we add a set of childern, we will move the index to the end 
        # for the preparation of next set of childern
        elif tokens[i] == ']':
            parent_node = level_list[level-1][-1]
            level_list[level-1][-1] = Tree(parent_node.name, level_list[level][level_index_list[level]:])
            level_index_list[level] += len(level_list[level])
            level -= 1
    
        # Whenever we meet a char that is not '[' or ']', 
        # it is a node in the tree
        else:
            level_list[level].append(Tree(tokens[i]))
        
        i += 1
    # return the root
    return level_list[0][0]
    
def max_depth(root): # do not change the heading of the function
    # Use recursion to find max_depth
    # Base case it is a leaf and it return 1
    if len(root.children) == 0:
        return 1
    # set a depth value to store max depth
    maxDepth = 0
    # Treverse all children
    for node in root.children:
        # maxDepth of this node is 1 + the max depth of its children
        child_depth = max_depth(node) + 1
        # replace maxDepth if it has a larger value
        if child_depth >= maxDepth:
            maxDepth = child_depth
            
    return maxDepth
