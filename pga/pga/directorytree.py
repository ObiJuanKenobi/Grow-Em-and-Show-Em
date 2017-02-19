import os

'''
directorytree.py
@author Andrew Dailey
'''

'''
Directory node.
Keeps track of a directory and its children.
'''
class DirectoryNode:

    '''
    Create a DirectoryNode from a given name and depth.
    '''
    def __init__(self, name, depth):
        self.name = name    # String
        self.depth = depth  # Number
        self.subdirs = []   # Array of DirectoryNodes
        self.files = []     # Array of Strings

'''
Directory tree.
Populates automatically from a given root directory.
'''
class DirectoryTree:

    '''
    Creates root node and populates.
    Depth of root is 0 and therefore relative to the rootDir.
    Ex. If the rootDir is /home/adailey, all dirs within will have a depth of 0.
    '''
    def __init__(self, rootDir):
        self.maxDepth = 0
        self.root = DirectoryNode(rootDir, 0)
        self.__populate(self.root, 0)

    '''
    Populates the tree recursively.
    Also finds maximum depth.
    '''
    def __populate(self, node, depth):
        self.maxDepth = depth if depth > self.maxDepth else self.maxDepth

        with os.scandir(node.name) as iter:
            for entry in iter:
                if entry.is_dir():
                    subdir = DirectoryNode(node.name + '/' + entry.name, depth)
                    self.__populate(subdir, depth + 1)
                    node.subdirs.append(subdir)
                elif entry.is_file():
                    node.files.append(entry.name)

    '''
    Recursive helper method for printing trees.
    '''
    def __printTree(self, node):
        dirPadding = ' ' * 4 * node.depth
        filePadding = ' ' * 4 * (node.depth + 1)
        print(dirPadding + node.name)
        
        for f in node.files:
            print(filePadding + f)

        for d in node.subdirs:
            self.__printTree(d)

    '''
    Recursive helper method for getting all dirs at a specified depth.
    '''
    def __getDirectoriesAtDepth(self, depth, node, dirs):
        if node.depth == depth:
            dirs.append(node)

        for d in node.subdirs:
            self.__getDirectoriesAtDepth(depth, d, dirs)

    '''
    Prints all dirs and files in the tree.
    Formatting is similar to the 'tree' command.
    '''
    def printTree(self):
        self.__printTree(self.root)

    '''
    Get the max depth of the tree.
    '''
    def getMaxDepth(self):
        return self.maxDepth

    '''
    Get all directories at a certain depth.
    '''
    def getDirectoriesAtDepth(self, depth):
        dirs = []
        self.__getDirectoriesAtDepth(depth, self.root, dirs)
        return dirs

## Example usage
#tree = DirectoryTree('.')
#print('Max depth:')
#print(tree.getMaxDepth())
#
#print('\nTree structure:')
#tree.printTree()
#
#print('\nDirs at depth 1:')
#for d in tree.getDirectoriesAtDepth(1):
#    print(d.name)
