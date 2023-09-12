from logics.utils.parsers import classical_parser

classical_parser.parse_replacement_dict.update({'!': '~'})
classical_parser.unparse_replacement_dict.update({'~': '!'})
classical_parser.parse_replacement_dict.update({'|': '∨'})
classical_parser.unparse_replacement_dict.update({'∨': '|'})

class Formula:
    def __init__(self, root):
        self.root = root
        self.termini = []

def build_tree(expression_list):
    if not expression_list:
        return None

    root_value = expression_list[0]
    root = Node(root_value)

    if len(expression_list) > 1:
        for child_expression_list in expression_list[1:]:
            child_tree = build_tree(child_expression_list)
            root.childs.append(child_tree)

    return root

def print_tree(node, level=0):
    if node:
        print("  " * level + str(node.root))
        for child in node.termini:
            print_tree(child, level + 1)

#inp = str(input("Digita la formula: "))
formula = classical_parser.parse('!((q | p) --> (q | p))')
print(formula)
root = build_tree(formula)
formula = Formula(root)
