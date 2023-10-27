from logics.utils.parsers import classical_parser
from logics.instances.propositional.languages import classical_language

classical_language.atomics.extend(['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'])
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
            children_strings = [self._node_to_string(child) for child in node.children]
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


def build_tree(expression_list, termini):
    # se la lista è vuota restituisco None
    if not expression_list:
        return None

    # Analizziamo il primo elemento della lista
    root_value = expression_list[0]
    root = Node(root_value)

    # se il valore non è un operatore lo aggiungo alla lista dei termini
    if root_value not in ["∧", "∨", "~", "→"]:
        for term in termini:
            if term.value == root_value:
                # passo il nodo termine già presente nella lista dei termini
                root = term
        # se il termine non è presente nella lista dei termini lo aggiungo
        if root not in termini:
            termini.append(root)

    # se la lista ha più di un elemento, ricorsivamente costruiamo l'albero
    if len(expression_list) > 1:
        for child_expression_list in expression_list[1:]:
            child_tree, termini = build_tree(child_expression_list, termini)
            root.children.append(child_tree)

    return root, termini


def print_tree(node, level=0):
    if node:
        print("  " * level + str(node.value))
        for child in node.children:
            print_tree(child, level + 1)


class Node:
    def __init__(self, value):
        # eventuali figli
        self.children = []
        # valore che può essere un operatore o un termine
        self.value = value
        # valore di verità che è stato assegnato a un termine
        self.boolean = None

    # metodo per sapere se ho un termine
    def estTermine(self):
        return len(self.children) == 0

    # metodo per capire se un certo è un operatore
    def estOperator(self):
        operators = ["∧", "∨", "~", "→"]  # and, or, not, implica
        if self.value in operators:
            return True
        else:
            return False

    # metodo per rappresentare l'albero della formula logica
    def __str__(self, level=0):
        ret = "\t" * level + repr(self.value) + "\n"
        for child in self.children:
            ret += child.__str__(level + 1)
        return ret


# classe che implementa l'albero del tableaux
class Tableaux():
    # classe che rappresenta i nodi dell'albero tableaux
    class Nodo():

        def __init__(self, ins_formula):
            # le formule che appartengono al singolo nodo (come albero)
            self.ins_formula = ins_formula
            self.children = []
            # le stesse formule ma in una lista per poter essere stampate (come stringa)
            self.formule = []
            for formula in ins_formula:
                self.formule.append(formula.to_string())

        # metodo per poter rappresentare l'albero del tableaux
        def __str__(self, level=0):
            ret = "\t" * level + repr(self.formule) + "\n"
            for child in self.children:
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
        new_formula = Formula(formula.root.children[0].children[0])
        # crea un nuovo nodo dell'albero tableaux
        new_nodo = self.Nodo([new_formula])
        node.children.append(new_nodo)
        new_foglie.append(new_nodo)

    # metodo che fa side effect su self.ret, questa implementa ed analizza l'albero del tableaux, modificando opportunamente il valore self.ret
    def risolvi(self, nodo, foglie):
        # controllo per sapere quando fermarsi: se ottengo self.ret == True vuol dire che ho trovato una assegnazione dei valori di verità soddisfacibile e quindi non ho più bisogno di continuare l'analisi
        if self.ret == False:
            if nodo.ins_formula is None:
                return
            # inizio controllo dei nodi
            # 1° CONTROLLO: DOPPIA NEGAZIONE
            for formula in nodo.ins_formula:
                # controllo se c'è "~"
                if formula.root.value == "~":
                    # se si controllo i figli
                    # se è uno ed è "~"
                    if formula.root.children[0].value == "~":
                        # lista di supporto per sapere quali sono le foglie dell'albero tableaux
                        new_foglie = []
                        for node in foglie:
                            self.doppia_negazione(node, formula, new_foglie)
                        foglie = new_foglie
            # 2° CONTROLLO: ALPHA RULE
            for formula in nodo.ins_formula:
                # controllo se c'è "~"
                if formula.root.value == "~":
                    # se il figlio è un "∨" abbiamo ~(ϕ ∨ ψ)
                    if formula.root.children[0].value == "∨":
                        new_foglie = []
                        for node in foglie:
                            new_ins_formula = []
                            # crea una nodo della formula ~ϕ
                            phi = Node("~")
                            phi.children.append(formula.root.children[0].children[0])
                            new_ins_formula.append(Formula(phi))
                            # crea una nodo della formula ~ψ
                            psi = Node("~")
                            psi.children.append(formula.root.children[0].children[1])
                            new_ins_formula.append(Formula(psi))
                            # crea un nodo di tableaux per ogni foglia e lo passa come figlio a ognuna
                            new_nodo = self.Nodo(new_ins_formula)
                            node.children.append(new_nodo)
                            new_foglie.append(new_nodo)
                        foglie = new_foglie
                    # se il figlio è un "→" abbiamo ~(ϕ → ψ)
                    if formula.root.children[0].value == "→":
                        new_foglie = []
                        for node in foglie:
                            new_ins_formula = []
                            # crea un nodo della formula ϕ
                            phi = formula.root.children[0].children[0]
                            new_ins_formula.append(Formula(phi))
                            # crea una nodo della formula ~ψ
                            psi = Node("~")
                            psi.children.append(formula.root.children[0].children[1])
                            new_ins_formula.append(Formula(psi))
                            # crea un nodo di tableaux per ogni foglia e lo passa come figlio a ognuna
                            new_nodo = self.Nodo(new_ins_formula)
                            node.children.append(new_nodo)
                            new_foglie.append(new_nodo)
                        foglie = new_foglie
                # controllo se c'è "∧" se si abbiamo ϕ ∧ ψ
                if formula.root.value == "∧":
                    new_foglie = []
                    for node in foglie:
                        new_ins_formula = []
                        # crea un nodo della formula ϕ
                        phi = formula.root.children[0]
                        new_ins_formula.append(Formula(phi))
                        # crea un nodo della formula ψ
                        psi = formula.root.children[1]
                        new_ins_formula.append(Formula(psi))
                        # crea un nodo di tableaux per ogni foglia e lo passo come figlio a ognuna
                        new_nodo = self.Nodo(new_ins_formula)
                        node.children.append(new_nodo)
                        new_foglie.append(new_nodo)
                    foglie = new_foglie
            # 3° CONTROLLO: BETA RULE
            for formula in nodo.ins_formula:
                # controllo se c'è "~"
                if formula.root.value == "~":
                    # se il figlio è un "∧" abbiamo ~(ϕ ∧ ψ)
                    if formula.root.children[0].value == "∧":
                        new_foglie = []
                        for node in foglie:
                            ins_formula_sx = []
                            ins_formula_dx = []
                            # crea un nodo della formula ~ϕ
                            phi = Node("~")
                            phi.children.append(formula.root.children[0].children[0])
                            ins_formula_sx.append(Formula(phi))
                            # crea un nodo della formula ~ψ
                            psi = Node("~")
                            psi.children.append(formula.root.children[0].children[1])
                            ins_formula_dx.append(Formula(psi))
                            # crea un nodo del tableaux che ha come formula ~ϕ
                            new_nodo_sx = self.Nodo(ins_formula_sx)
                            # crea un nodo del tableaux che ha come formula ~ψ
                            new_nodo_dx = self.Nodo(ins_formula_dx)
                            node.children.append(new_nodo_sx)
                            node.children.append(new_nodo_dx)
                            new_foglie.append(new_nodo_sx)
                            new_foglie.append(new_nodo_dx)
                        foglie = new_foglie
                # controllo se c'è "∨" se si abbiamo ϕ ∨ ψ
                if formula.root.value == "∨":
                    new_foglie = []
                    for node in foglie:
                        ins_formula_sx = []
                        ins_formula_dx = []
                        # crea un nodo della formula ϕ
                        phi = formula.root.children[0]
                        ins_formula_sx.append(Formula(phi))
                        # crea un nodo della formula ψ
                        psi = formula.root.children[1]
                        ins_formula_dx.append(Formula(psi))
                        # crea un nodo del tableaux che ha come formula ϕ
                        new_nodo_sx = self.Nodo(ins_formula_sx)
                        # crea un nodo del tableaux che ha come formula ψ
                        new_nodo_dx = self.Nodo(ins_formula_dx)
                        node.children.append(new_nodo_sx)
                        node.children.append(new_nodo_dx)
                        new_foglie.append(new_nodo_sx)
                        new_foglie.append(new_nodo_dx)
                    foglie = new_foglie
                # controllo se c'è "→" se si abbiamo ϕ → ψ
                if formula.root.value == "→":
                    new_foglie = []
                    for node in foglie:
                        ins_formula_sx = []
                        ins_formula_dx = []
                        # crea un nodo della formula ~ϕ
                        phi = Node("~")
                        phi.children.append(formula.root.children[0])
                        ins_formula_sx.append(Formula(phi))
                        # crea un nodo della formula ψ
                        psi = formula.root.children[1]
                        ins_formula_dx.append(Formula(psi))
                        # crea un nodo del tableaux che ha come formula ~ϕ
                        new_nodo_sx = self.Nodo(ins_formula_sx)
                        # crea un nodo del tableaux che ha come formula ψ
                        new_nodo_dx = self.Nodo(ins_formula_dx)
                        node.children.append(new_nodo_sx)
                        node.children.append(new_nodo_dx)
                        new_foglie.append(new_nodo_sx)
                        new_foglie.append(new_nodo_dx)
                    foglie = new_foglie
            # 4° CONTROLLO: TERMINI
            for formula in nodo.ins_formula:
                if formula.root.value == "~":
                    if formula.root.children[0].estTermine():
                        termine = formula.root.children[0]
                        if termine.boolean == True:
                            # se il valore assegnato al termine è true avrei una contraddizione e perciò devo chiudere la branch
                            nodo.children = [self.Nodo([Formula(Node("X"))])]
                            return
                        else:
                            # non ho assegnato nessun valore di verità al termine e quindi posso dargli False
                            termine.boolean = False
                            # controllo una chiusura positiva della branch, che può avvenire se mi trovo in una foglia del tableaux e se ho finito di analizzare tutte le formule del nodo
                            if len(nodo.children) == 0:
                                count = 0
                                # controlla i boolean dei termini id ins_formula
                                for term in self.terms:
                                    # se sono tutti diversi da None return true
                                    if term.boolean is not None:
                                        count += 1
                                if count == self.terms_len:
                                    self.ret = True
                                    nodo.children = [self.Nodo([Formula(Node("O"))])]
                                    return
                if formula.root.estTermine():
                    termine = formula.root
                    # se il valore assegnato al termine è false avrei una contraddizione e perciò devo chiudere la branch
                    if termine.boolean == False:
                        nodo.children = [self.Nodo([Formula(Node("X"))])]
                        return
                    else:
                        # non ho assegnato nessun valore di verità al termine e quindi posso dargli True
                        termine.boolean = True
                        if len(nodo.children) == 0:
                            count = 0
                            # controlla i boolean dei termini id ins_formula
                            for term in self.terms:
                                # se sono tutti diversi da None return true
                                if term.boolean is not None:
                                    count += 1
                            if count == self.terms_len:
                                self.ret = True
                                nodo.children = [self.Nodo([Formula(Node("O"))])]
                                return
            # a seconda del numero di figli del nodo attuale so come dividere le foglie
            # se ho un figlio gli passo tutte le foglie
            if len(nodo.children) == 1:
                self.risolvi(nodo.children[0], foglie)
            # se ne ho due passo la prima metà al figlio sinistro e la seconda al destro
            elif len(nodo.children) == 2:
                self.risolvi(nodo.children[0], foglie[:int(len(foglie) / 2)])
                self.risolvi(nodo.children[1], foglie[int(len(foglie) / 2):])


ins_formula_exp = []
termini = []
print("1) !((q | p) --> (p | q))")
print("2) !(((p --> q) --> p) --> p)")
print("3) ! ( ( (p --> q) & ( (p & q) --> r) ) --> (p --> r) )")
print("4) !( (q | p) --> (q & p) )")
print("5) p --> (q & r) , !q | !r , !!p")
print("6) (a | b) & c , !b | !c , !a")
print("7) Enter formulas from input")
inp = int(input("Choose a formula on which to apply the tableaux technique: "))
if inp < 5:
    if inp == 0:
        to_parse = str(input("Type in the formula: "))
    elif inp == 1:
        to_parse = '!((q | p) --> (p | q))'
    elif inp == 2:
        to_parse = '!(((p --> q) --> p) --> p)'
    elif inp == 3:
        to_parse = '! ( ( (p --> q) & ( (p & q) --> r) ) --> (p --> r) )'
    elif inp == 4:
        to_parse = '!( (q | p) --> (q & p) )'
    print("The formula is " + to_parse)
    parsed = classical_parser.parse(to_parse)
    root, termini = build_tree(parsed, termini)
    formula = Formula(root)
    formula.termini = termini
    print("Representation of the formula as a tree:")
    print_tree(formula.root)
    ins_formula_exp.append(formula)
elif inp == 5 or inp == 6:
    if inp == 5:
        to_parse1 = 'p --> (q & r)'
        to_parse2 = '!q | !r'
        to_parse3 = '!!p'
    elif inp == 6:
        to_parse1 = '(a | b) & c'
        to_parse2 = '!b | !c'
        to_parse3 = '!a'
    print("The formulas are : " + to_parse1 + "  ,  " + to_parse2 + "  ,  " + to_parse3)
    parsed1 = classical_parser.parse(to_parse1)
    parsed2 = classical_parser.parse(to_parse2)
    parsed3 = classical_parser.parse(to_parse3)
    root1, termini = build_tree(parsed1, termini)
    root2, termini = build_tree(parsed2, termini)
    root3, termini = build_tree(parsed3, termini)
    formula1 = Formula(root1)
    formula2 = Formula(root2)
    formula3 = Formula(root3)
    formula1.termini = termini
    formula2.termini = termini
    formula3.termini = termini
    print("Representation of formulas as a tree:")
    print_tree(formula1.root)
    print("--------------------")
    print_tree(formula2.root)
    print("--------------------")
    print_tree(formula3.root)
    print("--------------------")
    ins_formula_exp.append(formula1)
    ins_formula_exp.append(formula2)
    ins_formula_exp.append(formula3)
elif inp == 7:
    to_parse = str(input("Type the formula (empty string to end): "))
    while to_parse != "":
        parsed = classical_parser.parse(to_parse)
        root, termini = build_tree(parsed, termini)
        formula = Formula(root)
        formula.termini = termini
        print("Representation of the formula as a tree:")
        print_tree(formula.root)
        ins_formula_exp.append(formula)
        to_parse = str(input("Type the formula (empty string to end): "))

tableaux = Tableaux(ins_formula_exp)
tableaux.risolvi(tableaux.root, [tableaux.root])
print("\n")
print("Representation of the tableaux tree:\n")
print(str(tableaux.root))
if tableaux.ret:
    print("The formula is satisfiable\n")
    for term in tableaux.terms:
        print(term.value + " = " + str(term.boolean))
else:
    print("The formula is not satisfiable\n")

