from logics.utils.parsers import classical_parser
from logics.instances.propositional.languages import classical_language

classical_language.atomics.extend(['a', 'b', 'c'])
classical_parser.parse_replacement_dict.update({'!': '~'})
classical_parser.unparse_replacement_dict.update({'~': '!'})
classical_parser.parse_replacement_dict.update({'|': '∨'})
classical_parser.unparse_replacement_dict.update({'∨': '|'})


# classe che rappresenta una formula in logica
class Formula:

    def __init__(self, root):
        # lista che ricorda i singoli termini all'interno della formula
        self.termini = []
        self.root = root

    # metodo per stampare una formula sotto forma di stringa
    def to_string(self):
        if self.root is not None:
            return self._node_to_string(self.root)
        else:
            return "Formula vuota"

    def _node_to_string(self, node):
        if node is None:
            return ""

        if node.estOperator():
            # Se il nodo è un operatore, ricorsivamente otteniamo la rappresentazione delle sottoformule
            children_strings = [self._node_to_string(child) for child in node.childs]
            operator = node.value
            if operator == "~":
                return f"{operator}{children_strings[0]}"
            elif operator == "→":
                return f"({children_strings[0]} {operator} {children_strings[1]})"
            else:
                return f"({children_strings[0]} {operator} {children_strings[1]})"
        else:
            # Se il nodo è un termine, restituiamo il suo valore
            return node.value


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
        print("  " * level + str(node.value))
        for child in node.childs:
            print_tree(child, level + 1)


class Node:
    def __init__(self, value):
        # eventuali figli
        self.childs = []
        # valore che può essere un operatore o un termine
        self.value = value
        # valore di verità che è stato assegnato a un termine
        self.boolean = None

    # metodo per sapere se ho un termine
    def estTermine(self):
        return len(self.childs) == 0

    # metodo per capire se un certo è un operatore
    def estOperator(self):
        operators = ["∧", "∨", "~", "→"]  # and, or, not, not not, implica
        if self.value in operators:
            return True
        else:
            return False

    # metodo per rappresentare l'albero della formula logica
    def __str__(self, level=0):
        ret = "\t" * level + repr(self.value) + "\n"
        for child in self.childs:
            ret += child.__str__(level + 1)
        return ret


# classe che implementa l'albero del tableaux
class Tableaux():
    # classe che rappresenta i nodi dell'albero tableaux
    class Nodo():

        def __init__(self, ins_formula):
            # le formule che appartengono al singolo nodo (come albero)
            self.ins_formula = ins_formula
            self.childs = []
            # le stesse formule ma in una lista per poter essere stampate (come stringa)
            self.formule = []
            for formula in ins_formula:
                self.formule.append(formula.to_string())

        # metodo per poter rappresentare l'albero del tableaux
        def __str__(self, level=0):
            ret = "\t" * level + repr(self.formule) + "\n"
            for child in self.childs:
                ret += child.__str__(level + 1)
            return ret

    def __init__(self, ins_formula):
        # valore che indica la soddisfacibilità dell'insieme di formule: true indica la soddisfacibilità, false il contrario
        self.ret = False
        # una lista con tutti i termini nelle varie formule
        self.terms = []
        self.root = self.Nodo(ins_formula)
        for formula in ins_formula:
            for termine in formula.termini:
                if termine not in self.terms:
                    self.terms.append(termine)
        # numero di termini
        self.terms_len = len(self.terms)

    # metodo per eliminare doppie negazioni
    def doppia_negazione(self, node, formula, new_foglie):
        # crea una nuova formula che ha come root l'elemento dopo la doppia negazione
        new_formula = Formula(formula.root.childs[0].childs[0])
        # crea un nuovo nodo dell'albero tableaux
        new_nodo = self.Nodo([new_formula])
        node.childs.append(new_nodo)
        new_foglie.append(new_nodo)

    # metodo che fa side effect su self.ret, questa implementa ed analizza l'albero del tableaux, modificando opportunamente il valore self.ret
    def risolvi(self, nodo, foglie):
        # controllo per sapere quando fermarsi: se ottengo self.ret == True vuol dire che ho trovato una assegnazione dei valori di verità soddisfacibile e quindi non ho più bisogno di continuare l'analisi
        if self.ret == False:
            if nodo.ins_formula is None:
                return
            # inizio controllo dei nodi
            # 1 CONTROLLO: DOPPIA NEGAZIONE/ASSEGNAZIONE BOOLEAN
            for formula in nodo.ins_formula:
                # controllo se c'è "!"
                if formula.root.value == "~":
                    # se si controllo i figli
                    # se è uno ed è "!"
                    if formula.root.childs[0].value == "~":
                        # lista di supporto per sapere quali sono le foglie dell'albero tableaux
                        new_foglie = []
                        for node in foglie:
                            self.doppia_negazione(node, formula, new_foglie)
                        foglie = new_foglie
                    # se è un termine
                    if formula.root.childs[0].estTermine():
                        termine = formula.root.childs[0]
                        if termine.boolean == True:
                            # se il valore assegnato al termine è true avrei una contraddizione e perciò devo chiudere la branch
                            nodo.childs = [self.Nodo([Formula("X")])]
                            return
                        else:
                            # non ho assegnato nessun valore di verità al termine e quindi posso dargli False
                            termine.boolean = False
                            # controllo una chiusura positiva della branch, che può avvenire se mi trovo in una foglia del tableaux e se ho finito di analizzare tutte le formule del nodo
                            if len(nodo.childs) == 0 and nodo.ins_formula.index(formula) == len(nodo.ins_formula) - 1:
                                count = 0
                                # controlla i boolean dei termini id ins_formula
                                for term in self.terms:
                                    # se sono tutti diversi da None return true
                                    if term.boolean is not None:
                                        count += 1
                                if count == self.terms_len:
                                    self.ret = True
                                    nodo.childs = [self.Nodo([Formula("O")])]
                                    return
                if formula.root.estTermine():
                    termine = formula.root
                    # se il valore assegnato al termine è false avrei una contraddizione e perciò devo chiudere la branch
                    if termine.boolean == False:
                        nodo.childs = [self.Nodo([Formula("X")])]
                        return
                    else:
                        # non ho assegnato nessun valore di verità al termine e quindi posso dargli True
                        termine.boolean = True
                        if len(nodo.childs) == 0 and nodo.ins_formula.index(formula) == len(nodo.ins_formula) - 1:
                            count = 0
                            # controlla i boolean dei termini id ins_formula
                            for term in self.terms:
                                # se sono tutti diversi da None return true
                                if term.boolean is not None:
                                    count += 1
                            if count == self.terms_len:
                                self.ret = True
                                nodo.childs = [self.Nodo([Formula("O")])]
                                return
            # 2 CONTROLLO: ALPHA RULE
            for formula in nodo.ins_formula:
                # controllo se c'è "!"
                if formula.root.value == "~":
                    # se il figlio è un "|"
                    if formula.root.childs[0].value == "∨":
                        new_foglie = []
                        for node in foglie:
                            new_ins_formula = []
                            # crea una nodo della formula phi con il ! + figlio sinistro dell'|
                            phi = Node("~")
                            phi.childs.append(formula.root.childs[0].childs[0])
                            new_ins_formula.append(Formula(phi))
                            # crea una nodo della formula psi con il ! + figlio destro dell'|
                            psi = Node("~")
                            psi.childs.append(formula.root.childs[0].childs[1])
                            new_ins_formula.append(Formula(psi))
                            # crea un nodo di tableaux per ogni foglia e passalo come figlio a ognuna
                            new_nodo = self.Nodo(new_ins_formula)
                            node.childs.append(new_nodo)
                            new_foglie.append(new_nodo)
                        foglie = new_foglie
                    # se è un "-->"
                    if formula.root.childs[0].value == "→":
                        new_foglie = []
                        for node in foglie:
                            new_ins_formula = []
                            # crea un nodo della formula phi con il figlio sinistro dell' -->
                            phi = formula.root.childs[0].childs[0]
                            new_ins_formula.append(Formula(phi))
                            # crea una nodo della formula psi con il ! + figlio destro dell'-->
                            psi = Node("~")
                            psi.childs.append(formula.root.childs[0].childs[1])
                            new_ins_formula.append(Formula(psi))
                            # crea un nodo di tableaux per ogni foglia e passalo come figlio a ognuna
                            new_nodo = self.Nodo(new_ins_formula)
                            node.childs.append(new_nodo)
                            new_foglie.append(new_nodo)
                        foglie = new_foglie
                # controllo se c'è "&"
                if formula.root.value == "∧":
                    new_foglie = []
                    for node in foglie:
                        new_ins_formula = []
                        # crea un nodo della formula phi con il figlio sinistro dell'&
                        phi = formula.root.childs[0]
                        new_ins_formula.append(Formula(phi))
                        # crea un nodo della formula psi con il figlio destro dell'&
                        psi = formula.root.childs[1]
                        new_ins_formula.append(Formula(psi))
                        # crea un nodo di tableaux per ogni foglia e passalo come figlio a ognuna
                        new_nodo = self.Nodo(new_ins_formula)
                        node.childs.append(new_nodo)
                        new_foglie.append(new_nodo)
                    foglie = new_foglie
            # 3 CONTROLLO: BETA RULE
            for formula in nodo.ins_formula:
                # controllo se c'è "!"
                if formula.root.value == "~":
                    # se il figlio è un "&"
                    if formula.root.childs[0].value == "∧":
                        new_foglie = []
                        for node in foglie:
                            ins_formula_sx = []
                            ins_formula_dx = []
                            # crea un nodo della formula phi con ! + il figlio sinistro dell'&
                            phi = Node("~")
                            phi.childs.append(formula.root.childs[0].childs[0])
                            ins_formula_sx.append(Formula(phi))
                            # crea un nodo della formula psi con ! + il figlio destro dell'&
                            psi = Node("~")
                            psi.childs.append(formula.root.childs[0].childs[1])
                            ins_formula_dx.append(Formula(psi))
                            # crea un nodo del tableaux che ha come formula phi
                            new_nodo_sx = self.Nodo(ins_formula_sx)
                            # crea un nodo del tableaux che ha come formula psi
                            new_nodo_dx = self.Nodo(ins_formula_dx)
                            node.childs.append(new_nodo_sx)
                            node.childs.append(new_nodo_dx)
                            new_foglie.append(new_nodo_sx)
                            new_foglie.append(new_nodo_dx)
                        foglie = new_foglie
                # controllo se c'è "|"
                if formula.root.value == "∨":
                    new_foglie = []
                    for node in foglie:
                        ins_formula_sx = []
                        ins_formula_dx = []
                        # crea un nodo della formula phi con il figlio sinistro dell'|
                        phi = formula.root.childs[0]
                        ins_formula_sx.append(Formula(phi))
                        # crea un nodo della formula psi con il figlio destro dell'|
                        psi = formula.root.childs[1]
                        ins_formula_dx.append(Formula(psi))
                        # crea un nodo del tableaux che ha come formula phi
                        new_nodo_sx = self.Nodo(ins_formula_sx)
                        # crea un nodo del tableaux che ha come formula psi
                        new_nodo_dx = self.Nodo(ins_formula_dx)
                        node.childs.append(new_nodo_sx)
                        node.childs.append(new_nodo_dx)
                        new_foglie.append(new_nodo_sx)
                        new_foglie.append(new_nodo_dx)
                    foglie = new_foglie
                # controllo se c'è "-"
                if formula.root.value == "→":
                    new_foglie = []
                    for node in foglie:
                        ins_formula_sx = []
                        ins_formula_dx = []
                        # crea un nodo della formula psi con ! + il figlio destro dell'-->
                        phi = Node("~")
                        phi.childs.append(formula.root.childs[0])
                        ins_formula_sx.append(Formula(phi))
                        # crea un nodo della formula psi con il figlio destro dell'-->
                        psi = formula.root.childs[1]
                        ins_formula_dx.append(Formula(psi))
                        # crea un nodo del tableaux che ha come formula phi
                        new_nodo_sx = self.Nodo(ins_formula_sx)
                        # crea un nodo del tableaux che ha come formula psi
                        new_nodo_dx = self.Nodo(ins_formula_dx)
                        node.childs.append(new_nodo_sx)
                        node.childs.append(new_nodo_dx)
                        new_foglie.append(new_nodo_sx)
                        new_foglie.append(new_nodo_dx)
                    foglie = new_foglie
            # a seconda del numero di figli del nodo attuale so come dividere le foglie
            # se ho un figlio gli passo tutte le foglie
            if len(nodo.childs) == 1:
                self.risolvi(nodo.childs[0], foglie)
            # se ne ho due passo la prima metà al figlio sinistro e la seconda al destro
            elif len(nodo.childs) == 2:
                self.risolvi(nodo.childs[0], foglie[:int(len(foglie) / 2)])
                self.risolvi(nodo.childs[1], foglie[int(len(foglie) / 2):])


# inp = str(input("Digita la formula: "))
ins_formula_exp = []
inp = input("Scegli una formula : ")
if inp == '1':
    to_parse = '!(q | p) --> (q | p)'
    print("La formula è " + to_parse)
    parsed = classical_parser.parse(to_parse)
    root = build_tree(parsed)
    formula = Formula(root)
    formula.termini = map(Node, list(parsed.atomics_inside(classical_language)))
    print("Rappresentazione della formula come albero:")
    print_tree(formula.root)
    ins_formula_exp.append(formula)
if inp == '2':
    to_parse = '!(((p --> q) --> p) --> p)'
    print("La formula è " + to_parse)
    parsed = classical_parser.parse(to_parse)
    root = build_tree(parsed)
    formula = Formula(root)
    formula.termini = map(Node, list(parsed.atomics_inside(classical_language)))
    print("Rappresentazione della formula come albero:")
    print_tree(formula.root)
    ins_formula_exp.append(formula)
if inp == '3':
    to_parse = '! ( ( (p --> q) & ( (p & q) --> r) ) --> (p --> r) )'
    print("La formula è " + to_parse)
    parsed = classical_parser.parse(to_parse)
    root = build_tree(parsed)
    formula = Formula(root)
    formula.termini = map(Node, list(parsed.atomics_inside(classical_language)))
    print("Rappresentazione della formula come albero:")
    print_tree(formula.root)
    ins_formula_exp.append(formula)
if inp == '4':
    to_parse = '! ((q | p) --> (q & p))'
    print("La formula è " + to_parse)
    parsed = classical_parser.parse(to_parse)
    root = build_tree(parsed)
    formula = Formula(root)
    formula.termini = map(Node, list(parsed.atomics_inside(classical_language)))
    print("Rappresentazione della formula come albero:")
    print_tree(formula.root)
    ins_formula_exp.append(formula)
if inp == '5':
    to_parse1 = 'p --> (q & r)'
    to_parse2 = '!q | !r'
    to_parse3 = '!!p'
    print("Le formula sono : " + to_parse1 + "  ,  " + to_parse2 + "  ,  " + to_parse3)
    parsed1 = classical_parser.parse(to_parse1)
    parsed2 = classical_parser.parse(to_parse2)
    parsed3 = classical_parser.parse(to_parse3)
    root1 = build_tree(parsed1)
    root2 = build_tree(parsed2)
    root3 = build_tree(parsed3)
    formula1 = Formula(root1)
    formula2 = Formula(root2)
    formula3 = Formula(root3)
    formula1.termini = map(Node, list(parsed1.atomics_inside(classical_language)))
    formula2.termini = map(Node, list(parsed2.atomics_inside(classical_language)))
    formula3.termini = map(Node, list(parsed3.atomics_inside(classical_language)))
    print("Rappresentazione della formule come albero:")
    print_tree(formula1.root)
    print_tree(formula2.root)
    print_tree(formula3.root)
    ins_formula_exp.append(formula1)
    ins_formula_exp.append(formula2)
    ins_formula_exp.append(formula3)
if inp == '6':
    to_parse1 = '(a | b) & c'
    to_parse2 = '!b | !c'
    to_parse3 = '!a'
    print("Le formula sono : " + to_parse1 + "  ,  " + to_parse2 + "  ,  " + to_parse3)
    parsed1 = classical_parser.parse(to_parse1)
    parsed2 = classical_parser.parse(to_parse2)
    parsed3 = classical_parser.parse(to_parse3)
    root1 = build_tree(parsed1)
    root2 = build_tree(parsed2)
    root3 = build_tree(parsed3)
    formula1 = Formula(root1)
    formula2 = Formula(root2)
    formula3 = Formula(root3)
    formula1.termini = map(Node, list(parsed1.atomics_inside(classical_language)))
    formula2.termini = map(Node, list(parsed2.atomics_inside(classical_language)))
    formula3.termini = map(Node, list(parsed3.atomics_inside(classical_language)))
    print("Rappresentazione della formule come albero:")
    print_tree(formula1.root)
    print_tree(formula2.root)
    print_tree(formula3.root)
    ins_formula_exp.append(formula1)
    ins_formula_exp.append(formula2)
    ins_formula_exp.append(formula3)

tableaux = Tableaux(ins_formula_exp)
tableaux.risolvi(tableaux.root, [tableaux.root])
print(tableaux.ret, "\n")
print(str(tableaux.root))
