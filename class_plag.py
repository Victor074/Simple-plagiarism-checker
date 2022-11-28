import ast
from _ast import *
from munkres import Munkres

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
        self.leaf_1 = None
        self.leaf_2 = None
        self.leaf_of_leaf_1 = None
        self.leaf_of_leaf_2 = None
        self.path1 = path1
        self.path2 = path2

    def load_scripts(self,path1,path2):

        # self.path1 = "C:/Users/valc2/Documents/GitHub/Simple-plagiarism-checker/actividad5.py"
        # self.path2 = "C:/Users/valc2/Documents/GitHub/Simple-plagiarism-checker/actividad5-c.py"
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
    

    def compare_ASTs (self, ast_a : AST , ast_b : AST , reorder_depth : int ) -> int :#done
        children_a = list ( ast . iter_child_nodes ( ast_a ))
        children_b = list ( ast . iter_child_nodes ( ast_b ))
        if (( type ( ast_a ) == type ( ast_b ))
                and len ( list ( children_a )) == 0
                and len ( list ( children_b )) == 0) :
            return 1
        
        if (( type ( ast_a ) != type ( ast_b ))
                or ( len ( children_a ) != len ( children_b )) ):
            return 0

        if reorder_depth == 0:
            match_index = sum ( map ( lambda pairs : self.compare_ASTs (
                pairs [0] , pairs [1] , reorder_depth ) ,
                zip ( children_a , children_b ) ))
            return match_index + 1
        
        elif reorder_depth > 0:
            match_index = self.reorder_children_compare (
                ast_a , ast_b , reorder_depth - 1)
            return match_index + 1

    def reorder_children_compare (self, ast_a : AST , ast_b : AST ,reorder_depth : int ) -> int :
        comparison_matrix = []
        cost_matrix = []
        best_match_value = 0
        children_a = list ( ast . iter_child_nodes ( ast_a ))
        children_b = list ( ast . iter_child_nodes ( ast_b ))
        if len ( children_a ) <= 1 or len ( children_b ) <= 1:
            for child_a in children_a :
                for child_b in children_b :
                    best_match_value += self.compare_ASTs( child_a, child_b , reorder_depth )
        else:
            for child_a in children_a :
                row = []
                cost_row = []
                for child_b in children_b :
                    similarity = self.compare_ASTs ( child_a , child_b , reorder_depth )
                    row.append( similarity )
                    cost_row . append (10000000 - similarity )
                comparison_matrix . append ( row )
                cost_matrix . append ( cost_row )
            m = Munkres()
            indices = m. compute ( cost_matrix )
            for row , col in indices :
                best_match_value += comparison_matrix [ row ][ col ]
        return best_match_value

    def get_leaf(self,tree):
        return list[ast.iter_child_nodes(tree)] #posible fallo por corchetes

    def compare_subtrees (self, sig_subtrees_p1 : list , sig_subtrees_p2 : list , reorder_depth : int ) -> tuple :
        comparison_matrix = []
        cost_matrix = []
        best_match = []
        best_match_value = 0
        best_match_weight = 0
        children_a = sig_subtrees_p1 . copy ()
        children_b = sig_subtrees_p2 . copy ()

        if len ( children_a ) <= 1 or len ( children_b ) <= 1:
            for child_a in children_a:
                best_match += [ child_a ]
                for child_b in children_b :
                    best_match_value += self.compare_ASTs ( child_a ,child_b , reorder_depth )
                    best_match += [ child_b ]
        else :
            for child_a in children_a :
                row = []
                cost_row = []
                for child_b in children_b :
                    similarity = self.compare_ASTs ( child_a , child_b , reorder_depth )
                    row . append ( similarity )
                    cost_row . append (10000000 - similarity )

                comparison_matrix . append ( row )
                cost_matrix . append ( cost_row )

            m = Munkres ()
            indices = m. compute ( cost_matrix )

            for row , col in indices :
                best_match_weight += self.apply_weights_to_subtrees_mult (
                    comparison_matrix [ row ][ col ] , sig_subtrees_p1 [ row ] ,
                    sig_subtrees_p2 [ col ])
                best_match += [ sig_subtrees_p1 [ row ] , sig_subtrees_p2 [ col ]]

        all_subtrees_weight = (sum ( map ( lambda tree : self.apply_weights_to_subtrees ( self.get_num_nodes ( tree ) , tree ) , sig_subtrees_p1 ))
            + sum( map ( lambda tree : self.apply_weights_to_subtrees ( self.get_num_nodes ( tree ) ,
            tree ) ,
            sig_subtrees_p2 )))

        similarity = 2 * best_match_weight / all_subtrees_weight
        return round ( similarity , 4) , best_match

    def get_num_nodes (self, root : AST ) -> int :
        """ Find the number of nodes for a given tree .
        197
        Args :
        root : The root of the tree whose size we want .
        200
        Returns :
        The number of nodes in the tree .
        """
        return len ( list ( ast . walk ( root )))

    def apply_weights_to_subtrees (self, weight : float , subtree : AST ) -> float :
        """ Apply weights to subtrees according to the time por their roots .
        209
        Args :
        weight : The number of nodes in the subtree .
        subtree : The subtree .
        213
        Returns :
        The weighed weight of the tree .
        """
        new_weight = weight
        if isinstance ( subtree , Import ):
            new_weight *= 0.3   
        elif isinstance ( subtree , Module ) :
            new_weight *= 1
        elif isinstance ( subtree , FunctionDef ) :
            new_weight *= 1.2
        elif isinstance ( subtree , If ):
            new_weight *= 0.5
        elif isinstance ( subtree , ClassDef ):
            new_weight *= 1
        elif isinstance ( subtree , While ):
            new_weight *= 1
        elif isinstance ( subtree , For ):
            new_weight *= 1
        elif isinstance ( subtree , comprehension ):
            new_weight *= 1
        elif isinstance ( subtree , Return ) :
            new_weight *= 1
        return new_weight

    def apply_weights_to_subtrees_mult (self, weight : float , ast_1 : AST , ast_2 : AST ) -> float :
        if weight == 0:
            return 0
        else :
            return (( self.apply_weights_to_subtrees ( weight , ast_1 ) + self.apply_weights_to_subtrees ( weight , ast_2 ) ) / 2)

    def compare_many (self, programs : list ) -> list :
        """ Compare all of the programs in the list .

        Args :
        programs : A list of strings with python programs .

        Returns :
        A matrix with the similarity rating of between all the programs .
        """
        tree_list = list ( map(
            lambda prog : self.get_significant_subtrees ( ast . parse ( prog )) ,
            programs ) )

        matrix = []
        for program_1_tree_num in range (0 , len ( tree_list )):
            for program_2_tree_num in range ( program_1_tree_num , len( tree_list )):
                if program_1_tree_num == program_2_tree_num :
                    continue
                print(f"comparing { program_1_tree_num } to { program_2_tree_num }")

                subtrees1 = tree_list [ program_1_tree_num ]
                subtrees2 = tree_list [ program_2_tree_num ]

                result = self.compare_subtrees ( subtrees1 , subtrees2 , 1000) [0]

                matrix . append (( program_1_tree_num , program_2_tree_num , result ))
                matrix . append (( program_2_tree_num , program_1_tree_num , result ))

        return matrix

    def main(self,path1,path2):

        self.clean()
        self.load_scripts(path1,path2)
        self.sub_tree()
        similarity = self.compare_subtrees ( self.sub_tree_1 , self.sub_tree_2 , 10000) [0]
        print(f"The index of similarity between { path1 } and { path2 } is: { similarity }")
        return similarity
    
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
    start.main(path1,path2)