#classe che rappresenta una formula in logica
class Formula:
    
    def __init__(self, root):
        #lista che ricorda isingoli termini all'interno della formula
        self.termini = []
        self.root = root

    #metodo per stampare una formula sotto forma di stringa
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
            if operator == "¬":
                return f"{operator}{children_strings[0]}"
            elif operator == "->":
                return f"({children_strings[0]} {operator} {children_strings[1]})"
            else:
                return f"({children_strings[0]} {operator} {children_strings[1]})"
        else:
            # Se il nodo è un termine, restituiamo il suo valore
            return node.value

class Node:
    def __init__(self, value):
        #eventuali figli
        self.childs = []
        #valore che può essere un operatore o un termine
        self.value = value
        #valore di veirtà che è stato assegnato a un termine
        self.boolean = None

    #metodo per sapere se ho un termine
    def estTermine(self):
        return len(self.childs) == 0
    
    #metodo per capire se un certo è un operatore
    def estOperator(self):
        operators = ["&&", "||", "¬", "->"] #and, or, not, not not, implica
        if self.value in operators:
            return True
        else:
            return False
    #metodo per rappresentare l'albero della formula logica
    def __str__(self, level=0):
        ret = "\t"*level+repr(self.value)+"\n"
        for child in self.childs:
            ret += child.__str__(level+1)
        return ret

#classe che implementa l'albero del tableaux
class Tableaux():

    #classe che rappresenta i nodi dell'albero tableaux
    class Nodo():

        def __init__(self, ins_formula):
            #le formule che appartengono al singolo nodo (come albero)
            self.ins_formula = ins_formula
            self.childs = []
            #le stesse formule ma in una lista per poter essere stampate (come stringa)
            self.formule = []
            for formula in ins_formula:
                self.formule.append(formula.to_string())

        #metodo per poter rappresentare l'albero del tableaux
        def __str__(self, level=0):
            ret = "\t"*level+repr(self.formule)+"\n"
            for child in self.childs:
                ret += child.__str__(level+1)
            return ret

    def __init__(self, ins_formula):
        #valore che indica la soddisfacibilità dell'insieme di formule: true indica la soddisfacibilità, false il contrario
        self.ret = False
        #una lista con tutti i termini nelle varie formule
        self.terms = []
        self.root = self.Nodo(ins_formula)
        for formula in ins_formula:
            for termine in formula.termini:
                if termine not in self.terms:
                    self.terms.append(termine)
        #numero di termini
        self.terms_len = len(self.terms)

    #metodo per eliminare doppie negazioni
    def doppia_negazione(self, node, formula, new_foglie):
        #crea una nuova formula che ha come root l'elemento dopo la doppia negazione
        new_formula = Formula(formula.root.childs[0].childs[0])
        #crea un nuovo nodo dell'albero tableaux
        new_nodo = self.Nodo([new_formula])
        node.childs.append(new_nodo)
        new_foglie.append(new_nodo)
    
    #metodo che fa side effect su self.ret, questa implementa ed analizza l'albero del tableaux, modificando opportunamente il valore self.ret 
    def risolvi(self, nodo, foglie):
        print("chiamata")
        #controllo per sapere quando fermarsi: se ottengo self.ret == True vuol dire che ho trovato una assegnazione dei valori di verità soddisfacibile e quindi non ho più bisogno di continuare l'analisi
        if self.ret == False:
            if nodo.ins_formula is None:
                return
            #inizio controllo dei nodi
            #1 CONTROLLO: DOPPIA NEGAZIONE/ASSEGNAZIONE BOOLEAN
            for formula in nodo.ins_formula:
                #controllo se c'è "¬"
                if formula.root.value == "¬":
                    print("ho trovato come primo elemento un not")
                    #se si controllo i figli
                    #se è uno ed è "¬"
                    if formula.root.childs[0].value == "¬":
                        print("ho trovato una doppia negazione")
                        #lista di supporto per sapere quali sono le foglie dell'albero tableaux
                        new_foglie = []
                        for node in foglie:
                            self.doppia_negazione(node, formula, new_foglie)
                        foglie = new_foglie
                    #se è un termine
                    if formula.root.childs[0].estTermine():
                        termine = formula.root.childs[0]
                        if termine.boolean == True:
                            #se il valore assegnato al termine è true avrei una contraddizione e perciò devo chiudere la branch
                            nodo.childs = [self.Nodo([Formula(Node("X"))])]
                            print("ho una contraddizione true/false")
                            return
                        else:
                            #non ho assegnato nessun valore di verità al termine e quindi posso dargli False
                            print("ho assegnano un false")
                            termine.boolean = False
                            #controllo una chiusura positiva della branch, che può avvenire se mi trovo in una foglia del tableaux e se ho finito di analizzare tutte le formule del nodo
                            if len(nodo.childs) == 0 and nodo.ins_formula.index(formula) == len(nodo.ins_formula) - 1:
                                count = 0
                                #controlla i boolean dei termini id ins_formula
                                for term in self.terms:
                                    #se sono tutti diversi da None return true
                                    if term.boolean is not None:
                                        count += 1
                                if count == self.terms_len:
                                    self.ret = True
                                    nodo.childs = [self.Nodo([Formula(Node("O"))])]
                                    return
                if formula.root.estTermine():
                    termine = formula.root
                    #se il valore assegnato al termine è false avrei una contraddizione e perciò devo chiudere la branch
                    if termine.boolean == False:
                        print("ho trovato una contradizzione false/true")
                        nodo.childs = [self.Nodo([Formula(Node("X"))])]
                        return
                    else:
                        #non ho assegnato nessun valore di verità al termine e quindi posso dargli True
                        print("ho assegnato un true")
                        termine.boolean = True
                        if len(nodo.childs) == 0 and nodo.ins_formula.index(formula) == len(nodo.ins_formula) - 1:
                            count = 0
                            #controlla i boolean dei termini id ins_formula
                            for term in self.terms:
                                #se sono tutti diversi da None return true
                                if term.boolean is not None:
                                    count += 1
                            if count == self.terms_len:
                                self.ret = True
                                nodo.childs = [self.Nodo([Formula(Node("O"))])]
                                return
            #2 CONTROLLO: ALPHA RULE
            for formula in nodo.ins_formula:
                #controllo se c'è "¬"
                if formula.root.value == "¬":
                    #se il figlio è un "||"
                    if formula.root.childs[0].value == "||":
                        print("ho trovato una alpha rule: not/or")
                        new_foglie = []
                        for node in foglie:
                            new_ins_formula = []
                            #crea una nodo della formula phi con il ¬ + figlio sinistro dell'||
                            phi = Node("¬")
                            phi.childs.append(formula.root.childs[0].childs[0])
                            new_ins_formula.append(Formula(phi))
                            print("figlio di phi in aplha rule not/or: ", phi.childs[0].value)
                            #crea una nodo della formula psi con il ¬ + figlio destro dell'||
                            psi = Node("¬")
                            psi.childs.append(formula.root.childs[0].childs[1])
                            new_ins_formula.append(Formula(psi))
                            print("figlio di psi in aplha rule not/or: ", psi.childs[0].value)
                            #crea un nodo di tableaux per ogni foglia e passalo come figlio ad ognuna
                            new_nodo = self.Nodo(new_ins_formula)
                            node.childs.append(new_nodo)
                            new_foglie.append(new_nodo)
                        foglie = new_foglie
                    #se è un "->"
                    if formula.root.childs[0].value == "->":
                        print("ho trovato una alpha rule: not/implica")
                        new_foglie = []
                        for node in foglie:
                            new_ins_formula = []
                            #crea un nodo della formula phi con il figlio sinistro dell' ->
                            phi = formula.root.childs[0].childs[0]
                            new_ins_formula.append(Formula(phi))
                            print("phi in alpha rule not/implica: ", phi.value)
                            #crea una nodo della formula psi con il ¬ + figlio destro dell'->
                            psi = Node("¬")
                            psi.childs.append(formula.root.childs[0].childs[1])
                            new_ins_formula.append(Formula(psi))
                            print("figlio di psi in aplha rule not/implica: ", psi.childs[0].value)
                            #crea un nodo di tableaux per ogni foglia e passalo come figlio ad ognuna
                            new_nodo = self.Nodo(new_ins_formula)
                            node.childs.append(new_nodo)
                            new_foglie.append(new_nodo)
                        foglie = new_foglie
                #controllo se c'è "&&"
                if formula.root.value == "&&":
                    new_foglie = []
                    for node in foglie:
                        new_ins_formula = []
                        #crea un nodo della formula phi con il figlio sinistro dell'&&
                        phi = formula.root.childs[0]
                        new_ins_formula.append(Formula(phi))
                        print("phi in alpha rule and: ", phi.value)
                        #crea un nodo della formula psi con il figlio destro dell'&&
                        psi = formula.root.childs[1]
                        new_ins_formula.append(Formula(psi))
                        print("psi in alpha rule and: ", psi.value)
                        #crea un nodo di tableaux per ogni foglia e passalo come figlio ad ognuna
                        new_nodo = self.Nodo(new_ins_formula)
                        node.childs.append(new_nodo)
                        new_foglie.append(new_nodo)
                    foglie = new_foglie
            #3 CONTROLLO: BETA RULE
            for formula in nodo.ins_formula:
                #controllo se c'è "¬"
                if formula.root.value == "¬":
                    #se il figlio è un "&&"
                    if formula.root.childs[0].value == "&&":
                        new_foglie = []
                        for node in foglie:
                            ins_formula_sx = []
                            ins_formula_dx = []
                            #crea un nodo della formula phi con ¬ + il figlio sinistro dell'&&
                            phi = Node("¬")
                            phi.childs.append(formula.root.childs[0].childs[0])
                            ins_formula_sx.append(Formula(phi))
                            print("phi di beta rule not/and: ", phi.childs[0].value)
                            #crea un nodo della formula psi con ¬ + il figlio destro dell'&&
                            psi = Node("¬")
                            psi.childs.append(formula.root.childs[0].childs[1])
                            print("psi di beta rule not/and: ", psi.childs[0].value)
                            ins_formula_dx.append(Formula(psi))
                            #crea un nodo del tableaux che ha come formula phi
                            new_nodo_sx = self.Nodo(ins_formula_sx)
                            #crea un nodo del tableaux che ha come formula psi
                            new_nodo_dx = self.Nodo(ins_formula_dx)
                            node.childs.append(new_nodo_sx)
                            node.childs.append(new_nodo_dx)
                            new_foglie.append(new_nodo_sx)
                            new_foglie.append(new_nodo_dx)
                        foglie = new_foglie
                #controllo se c'è "||"
                if formula.root.value == "||":
                    new_foglie = []
                    for node in foglie:
                        ins_formula_sx = []
                        ins_formula_dx = []
                        #crea un nodo della formula phi con il figlio sinistro dell'||
                        phi = formula.root.childs[0]
                        ins_formula_sx.append(Formula(phi))
                        print("phi in beta rule or: ", phi.value)
                        #crea un nodo della formula psi con il figlio destro dell'||
                        psi = formula.root.childs[1]
                        ins_formula_dx.append(Formula(psi))
                        print("psi in beta rule or: ", psi.value)
                        #crea un nodo del tableaux che ha come formula phi
                        new_nodo_sx = self.Nodo(ins_formula_sx)
                        #crea un nodo del tableaux che ha come formula psi
                        new_nodo_dx = self.Nodo(ins_formula_dx)
                        node.childs.append(new_nodo_sx)
                        node.childs.append(new_nodo_dx)
                        new_foglie.append(new_nodo_sx)
                        new_foglie.append(new_nodo_dx)
                    foglie = new_foglie
                #controllo se c'è "->"
                if formula.root.value == "->":
                    new_foglie = []
                    for node in foglie:
                        ins_formula_sx = []
                        ins_formula_dx = []
                        #crea un nodo della formula psi con ¬ + il figlio destro dell'->
                        phi = Node("¬")
                        phi.childs.append(formula.root.childs[0])
                        ins_formula_sx.append(Formula(phi))
                        print("phi in beta rule implica: ", phi.childs[0].value)
                        #crea un nodo della formula psi con il figlio destro dell'->
                        psi = formula.root.childs[1]
                        print("psi in beta rule implica: ", psi.value)
                        ins_formula_dx.append(Formula(psi))
                        #crea un nodo del tableaux che ha come formula phi
                        new_nodo_sx = self.Nodo(ins_formula_sx)
                        #crea un nodo del tableaux che ha come formula psi
                        new_nodo_dx = self.Nodo(ins_formula_dx)
                        node.childs.append(new_nodo_sx)
                        node.childs.append(new_nodo_dx)
                        new_foglie.append(new_nodo_sx)
                        new_foglie.append(new_nodo_dx)
                    foglie = new_foglie
            #a seconda del numero di figli del nodo attuale so come dividere le foglie
            #se ho un figlio gli passo tutte le foglie
            if len(nodo.childs) == 1:
                self.risolvi(nodo.childs[0], foglie)
            #se ne ho 2 passo la prima metà al figlio sinistro e la seconda al destro
            elif len(nodo.childs) == 2:
                self.risolvi(nodo.childs[0], foglie[:int(len(foglie)/2)])
                self.risolvi(nodo.childs[1], foglie[int(len(foglie)/2):])

#formula soddisfacibile

""" ins_formula_exp = []
root = Node("¬")
esempio = Formula(root)
ins_formula_exp.append(esempio)
implica1 = Node("->")
root.childs.append(implica1)
or1 = Node("||")
or2 = Node("&&")
implica1.childs.append(or1)
implica1.childs.append(or2)
q = Node("q")
esempio.termini.append(q)
p = Node("p")
esempio.termini.append(p)
or1.childs.append(q)
or1.childs.append(p)
or2.childs.append(q)
or2.childs.append(p)
 """
#formula non soddisfacibile

""" ins_formula_exp = []
root = Node("¬")
esempio = Formula(root)
ins_formula_exp.append(esempio)
implica1 = Node("->")
root.childs.append(implica1)
and1 = Node("&&")
implica2 = Node("->")
implica1.childs.append(and1)
implica1.childs.append(implica2)
p = Node("p")
esempio.termini.append(p)
q = Node("q")
esempio.termini.append(q)
r = Node("r")
esempio.termini.append(r)
implica2.childs.append(p)
implica2.childs.append(r)
implica3 = Node("->")
implica4 = Node("->")
and1.childs.append(implica3)
and1.childs.append(implica4)
implica3.childs.append(p)
implica3.childs.append(q)
and2 = Node("&&")
implica4.childs.append(and2)
implica4.childs.append(r)
and2.childs.append(p)
and2.childs.append(q) """

#non soddisfacibile

""" ins_formula_exp = []
root1 = Node("->")
esempio1 = Formula(root1)
p = Node("p")
esempio1.termini.append(p)
q = Node("q")
esempio1.termini.append(q)
r = Node("r")
esempio1.termini.append(r)
and1 = Node("&&")
root1.childs.append(p)
root1.childs.append(and1)
and1.childs.append(q)
and1.childs.append(r)
root2 = Node("||")
esempio2 = Formula(root2)
ins_formula_exp.append(esempio2)
ins_formula_exp.append(esempio1)
not1 = Node("¬")
not2 = Node("¬")
root2.childs.append(not1)
root2.childs.append(not2)
not1.childs.append(q)
not2.childs.append(r)
root3 = Node("¬")
esempio3 = Formula(root3)
ins_formula_exp.append(esempio3)
not3 = Node("¬")
root3.childs.append(not3)
not3.childs.append(p) """

#non soddisfacibile

""" ins_formula_exp = []
root = Node("¬")
esempio = Formula(root)
ins_formula_exp.append(esempio)
implica1 = Node("->")
p = Node("p")
q = Node("q")
esempio.termini.append(p)
esempio.termini.append(q)
root.childs.append(implica1)
implica2 = Node("->")
implica1.childs.append(implica2)
implica1.childs.append(p)
implica3 = Node("->")
implica2.childs.append(implica3)
implica2.childs.append(p)
implica3.childs.append(p)
implica3.childs.append(q) """

#non soddisfacibile
ins_formula_exp = []
root1 = Node("&&")
esempio1 = Formula(root1)
a = Node("a")
esempio1.termini.append(a)
b = Node("b")
esempio1.termini.append(b)
c = Node("c")
esempio1.termini.append(c)
or1 = Node("||")
root1.childs.append(or1)
root1.childs.append(c)
or1.childs.append(a)
or1.childs.append(b)
root2 = Node("||")
esempio2 = Formula(root2)
not1 = Node("¬")
not1.childs.append(b)
root2.childs.append(not1)
not2 = Node("¬")
not2.childs.append(c)
root2.childs.append(not2)
root3 = Node("¬")
esempio3 = Formula(root3)
root3.childs.append(a)
ins_formula_exp.append(esempio1)
ins_formula_exp.append(esempio2)
ins_formula_exp.append(esempio3)

tableaux = Tableaux(ins_formula_exp)
tableaux.risolvi(tableaux.root, [tableaux.root])
print(tableaux.ret)
print(str(tableaux.root))