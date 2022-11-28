import ast
from _ast import *
from munkres import Munkres
global const
const =9999999999
class plag_checker:
    def __init__(self, path1=None, path2=None) -> None:
        self.code_1 = None
        self.code_2 = None
        self.sub_tree_1 = []
        self.sub_tree_2 = []
        self.important = [
                        Import,
                        FunctionDef,
                        While,
                        For,
                        comprehension,
                        Return,
                        If,
                        ClassDef,
                        ]
        self.important_weights ={
                        ClassDef:1.2,
                        Module:0.8,
                        While:1,
                        For:1,
                        comprehension:1,
                        Return:0.3,
                        Import:0.5,
                        FunctionDef:1.5,
                        If:0.5,
        }
        self.leaf_1 = None
        self.leaf_2 = None
        self.leaf_of_leaf_1 = None
        self.leaf_of_leaf_2 = None
        self.path1 = path1
        self.path2 = path2

    def load_scripts(self,path1,path2):

        self.path1 = path1
        self.path2 = path2

        with open(self.path1 , "r") as source:
            file1 = source.read()
        with open(self.path2 , "r") as source:
            file2 = source.read()
        self.code_1 = ast.parse(file1, mode = "exec")
        self.code_2 = ast.parse(file2, mode = "exec")

    def sub_tree(self):
        for nodo in ast.walk(self.code_1):
            for component in self.important:
                if isinstance(nodo, component):
                    self.sub_tree_1.append(nodo)
        for nodo in ast.walk(self.code_2):
            for component in self.important:
                if isinstance(nodo, component):
                    self.sub_tree_2.append(nodo)  
        self.leaf_1 = self.sub_tree_1.copy()
        self.leaf_2 = self.sub_tree_2.copy()
    

    def compare_tree (self, tree1=None, tree2=None, k=None):#done
        self.leaf_of_leaf_1 = self.get_leaf(tree1)
        self.leaf_of_leaf_2 = self.get_leaf(tree2)
        size_a = len(self.leaf_of_leaf_1)
        size_b = len(self.leaf_of_leaf_2)
        itera = zip ( self.leaf_of_leaf_1 , self.leaf_of_leaf_2 )
        if type ( tree1 ) != type ( tree2 ):
            return 0
        elif size_a!=size_b:
            return 0
        else:
            if size_a ==0 and size_b ==0:
                return 1

        if k == 0:
            pares = map (lambda sub_tree : self.compare_tree(sub_tree [0], sub_tree [1], k) ,itera)
            pares=sum(pares)
        
        elif k > 0:
            pares = self.compare_leaf(tree1 , tree2 , k - 1)
            
        return pares +1

    def compare_tree2(self,tree1,tree2,k): #done
        compare_list = []
        weight_list = []
        global const
        for node_1 in tree1:
            x = []
            cost_x = []
            for node_2 in tree2 :
                result = self.compare_tree ( node_1 , node_2 , k )
                x.append(result)
                cost_x.append(const-result)
            compare_list.append(x)
            weight_list.append(cost_x)
        return compare_list, weight_list

    def compare_leaf(self, tree1, tree2, k):
        compare_list = []
        weight_list = []
        
        leaf_depth_1 = self.get_leaf(tree1)
        leaf_depth_2 = self.get_leaf(tree2)
        size_a = len(leaf_depth_1)
        size_b = len(leaf_depth_2)

        compare_list, weight_list = self.compare_tree2(leaf_depth_1,leaf_depth_2,k)

        while size_a<=1 or size_b<=1:
            count = 0
            for node_1 in leaf_depth_1 :
                for node_2 in leaf_depth_2 :
                    count += self.compare_tree( node_1, node_2 , k )
            return count

        total_cost = self.hungarian(weight_list)
        count = 0
        for x , y in total_cost :
            count += compare_list[x][y]
        return count

    def get_leaf(self,tree):
        return list(ast.iter_child_nodes(tree))

    def hungarian(self,weight_list):
        hung=Munkres()
        return hung.compute(weight_list)


    def calculate_sim(self,tree_1,tree_2,last_weight,result_2):
        all_subtrees_weight = (sum(map(lambda total: self.pondera(len(list(ast.walk( total))),total),tree_1 ))+ sum(map(lambda tree : self.pondera(len(list(ast.walk(tree))),tree ) ,tree_2 )))
        result = last_weight / all_subtrees_weight
        result = round ( result*2 , 4) , result_2
        return result


    def Abstract_S_T (self, tree1, tree2, k):#done
        all_nodes_1 = tree1
        all_nodes_2 = tree2#copy
        size_a = len(all_nodes_1)
        size_b = len(all_nodes_2)
        compare_list=[]
        weight_list=[]
        result_2=[]
        tmp=0
        count=0
        last_weight=0
        while size_a<=1 or size_b<=1:
            for node_1 in all_nodes_1:
                result_2 += [ node_1 ]
                for node_2 in all_nodes_2 :
                    count += self.compare_tree ( node_1 ,node_2 , k )
                    result_2 += [ node_2 ]
            tmp=self.calculate_sim(tree1,tree2,last_weight,result_2)
            return tmp[0]

        for node_1 in all_nodes_1 :
            x = []
            cost_x = []
            for node_2 in all_nodes_2 :
                result = self.compare_tree( node_1 , node_2 , k )
                x.append( result )
                cost_x.append(10000000-result )

            compare_list.append( x )
            weight_list.append( cost_x )

        total_cost = self.hungarian(weight_list)

        for x, y in total_cost :
            tmp = self.pondera (compare_list[x][y], tree1[x])
            tmp2= self.pondera (compare_list[x][y], tree2[y])
            last_weight += (tmp+tmp2)/2
            result_2 += [tree1[x] ,tree2[y]]

        tmp=self.calculate_sim(tree1,tree2,last_weight,result_2)
        return tmp[0]


    def pondera (self, value, tree): #done
        for component in self.important:
            if isinstance(tree, component):
                w=self.important_weights[component]
        return value * w


    def run(self,path1,path2):

        self.clean()
        self.load_scripts(path1,path2)
        self.sub_tree()
        result = self.Abstract_S_T ( self.sub_tree_1 , self.sub_tree_2 , 999999)
        print(result)
        return result
    
    def clean(self):
        self.code_1 = None
        self.code_2 = None
        self.sub_tree_1 = []
        self.sub_tree_2 = []
        self.leaf_1 = None
        self.leaf_2 = None
        self.leaf_of_leaf_1 = None
        self.leaf_of_leaf_2 = None

if __name__ == "__main__":
    start=plag_checker()
    path1="C:/Users/valc2/Documents/GitHub/Simple-plagiarism-checker/actividad5.py"
    path2 = "C:/Users/valc2/Documents/GitHub/Simple-plagiarism-checker/actividad5-c.py"
    start.run(path1,path2)