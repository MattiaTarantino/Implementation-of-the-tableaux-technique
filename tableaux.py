class Formula:
    
    def __init__(self, root):
        self.termini = []
        self.root = root

    #definire lista di operatori
    def estOperator(self, nodo):
        operators = ["&&", "||", "¬", "->"] #and, or, not, not not, implica
        if nodo.value in operators:
            return True
        else:
            return False

    def estTermine(self, nodo):
        if len(nodo.childs) == 0:
            return True
        else:
            return False

class Tableaux():

    class Nodo():
        def __init__(self, ins_formula):
            self.ins_formula = ins_formula
            self.childs = []
        def __str__(self, level=0):
            ret = "\t"*level+repr(self.ins_formula[0].root.value)+"\n"
            for child in self.childs:
                ret += child.__str__(level+1)
            return ret

    def __init__(self, ins_formula):
        self.ret = False
        self.terms = []
        self.root = self.Nodo(ins_formula)
        #salva i nodi con i termini di ins_formula
        for formula in ins_formula:
            for termine in formula.termini:
                if termine not in self.terms:
                    self.terms.append(termine)
        self.terms_len = len(self.terms)

    def risolvi(self, nodo, foglie):
        print("chiamata")
        if self.ret == False:
            if nodo.ins_formula is None:
                return
            #inizio controllo dei nodi
            #1 CONTROLLO: DOPPIA NEGAZIONE/ASSEGNAZOINE BOOLEAN
            for formula in nodo.ins_formula:
                #controllo se c'è "¬"
                if formula.root.value == "¬":
                    print("ho trovato come primo elemento un not")
                    #se si controllo i figli
                    #se è uno ed è "¬"
                    if formula.root.childs[0].value == "¬":
                        print("ho trovato una doppia negazione")
                        #applico semplificazione di doppia negazione
                        #creo un nodo con solamente il figlio senza negazioni a ins_formula
                        new_foglie = []
                        for node in foglie:
                            new_formula = Formula(formula.root.childs[0].childs[0])
                            new_nodo = self.Nodo([new_formula])
                            node.childs.append(new_nodo)
                            new_foglie.append(new_nodo)
                        foglie = new_foglie
                    #se è un termine
                    if formula.root.childs[0].estTermine():
                        termine = formula.root.childs[0]
                        #controllo il suo boolean
                        #se è true chiudo la branch
                        if termine.boolean == True:
                            nodo.childs = []
                            print("ho una contraddizione true/false")
                            return
                        else:
                            #boolean = false
                            print("ho assegnano un false")
                            termine.boolean = False
                            if len(nodo.childs) == 0 and nodo.ins_formula.index(formula) == len(nodo.ins_formula) - 1:
                                count = 0
                                #controlla i boolean dei termini id ins_formula
                                for term in self.terms:
                                    #se sono tutti diversi da None return true
                                    if term.boolean is not None:
                                        count += 1
                                if count == self.terms_len:
                                    self.ret = True
                                    return
                if formula.root.estTermine():
                    termine = formula.root
                    #controllo il suo boolean
                    #se è true chiudo la branch
                    if termine.boolean == False:
                        print("ho trovato una contradizzione false/true")
                        nodo.childs = []
                        return
                    else:
                        #boolean = true
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
                                return
            #2 CONTROLLO: ALPHA RULE
            for formula in nodo.ins_formula:
                #controllo se c'è "¬"
                if formula.root.value == "¬":
                    #se si controllo i figli
                    #verifica se applicabile alpha rule
                    #se è un "||"
                    if formula.root.childs[0].value == "||":
                        print("ho trovato una alpha rule: not/or")
                        new_foglie = []
                        for node in foglie:
                            new_ins_formula = []
                            #aggiungi un nodo al set con "¬", a cui aggiugni un figlio con il nodo sinistro di formula
                            phi = Node("¬")
                            phi.childs.append(formula.root.childs[0].childs[0])
                            new_ins_formula.append(Formula(phi))
                            print("figlio di phi in aplha rule not/or: ", phi.childs[0].value)
                            #aggiungi un nodo al set con "¬", a cui aggiugni un figlio con il nodo destro di formula
                            psi = Node("¬")
                            psi.childs.append(formula.root.childs[0].childs[1])
                            new_ins_formula.append(Formula(psi))
                            print("figlio di psi in aplha rule not/or: ", psi.childs[0].value)
                            #aggiungi un nodo a ins_formula che contiene un set vuoto
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
                            #aggiungi un nodo al set con nodo sinistro di formula
                            phi = formula.root.childs[0].childs[0]
                            new_ins_formula.append(Formula(phi))
                            print("phi in alpha rule not/implica: ", phi.value)
                            #aggiungi un nodo al set con "¬", a cui aggiugni un figlio con il nodo destro di formula
                            psi = Node("¬")
                            psi.childs.append(formula.root.childs[0].childs[1])
                            new_ins_formula.append(Formula(psi))
                            print("figlio di psi in aplha rule not/implica: ", psi.childs[0].value)
                            #aggiungi un nodo a ins_formula che contiene un set vuoto
                            new_nodo = self.Nodo(new_ins_formula)
                            node.childs.append(new_nodo)
                            new_foglie.append(new_nodo)
                        foglie = new_foglie
                #controllo se c'è "&&"
                if formula.root.value == "&&":
                    new_foglie = []
                    for node in foglie:
                        new_ins_formula = []
                        #aggiungi un nodo con il figlio sinistro al set
                        phi = formula.root.childs[0]
                        new_ins_formula.append(Formula(phi))
                        print("phi in alpha rule and: ", phi.value)
                        #aggiungi un nodo con il figlio destro al set
                        psi = formula.root.childs[1]
                        new_ins_formula.append(Formula(psi))
                        print("psi in alpha rule and: ", psi.value)
                        #aggiungi un nodo a ins_formula con un set vuoto
                        new_nodo = self.Nodo(new_ins_formula)
                        node.childs.append(new_nodo)
                        new_foglie.append(new_nodo)
                    foglie = new_foglie
            #3 CONTROLLO: BETA RULE
            for formula in nodo.ins_formula:
                #controllo se c'è "¬"
                if formula.root.value == "¬":
                    #se si controllo i figli
                    #verifica se applicabile una beta rule
                    #se è un "&&"
                    if formula.root.childs[0].value == "&&":
                        new_foglie = []
                        for node in foglie:
                            ins_formula_sx = []
                            ins_formula_dx = []
                            #aggiungi un figlio con un set vuoto a formula e aggiungi al set un nodo con "¬", a cui assegni un figlio con il nodo sinistro di formula
                            phi = Node("¬")
                            phi.childs.append(formula.root.childs[0].childs[0])
                            ins_formula_sx.append(Formula(phi))
                            print("phi di beta rule not/and: ", phi.childs[0].value)
                            #aggiungi un figlio con un set vuoto a formula e aggiungi al set un nodo con "¬", a cui assegni un figlio con il nodo destro di formula
                            psi = Node("¬")
                            psi.childs.append(formula.root.childs[0].childs[1])
                            print("psi di beta rule not/and: ", psi.childs[0].value)
                            ins_formula_dx.append(Formula(psi))
                            new_nodo_sx = self.Nodo(ins_formula_sx)
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
                        #aggiungi un figlio con un set vuoto a formula e aggiungi al set un nodo con il nodo sinistro di formula
                        phi = formula.root.childs[0]
                        ins_formula_sx.append(Formula(phi))
                        print("phi in beta rule or: ", phi.value)
                        #aggiungi un figlio con un set vuoto a formula e aggiungi al set un nodo con il nodo destro di formula
                        psi = formula.root.childs[1]
                        ins_formula_dx.append(Formula(psi))
                        print("psi in beta rule or: ", psi.value)
                        new_nodo_sx = self.Nodo(ins_formula_sx)
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
                        #aggiungi un figlio con un set vuoto a formula e aggiungi al set un nodo con "¬", a cui assegni un figlio con il nodo sinistro di formula
                        phi = Node("¬")
                        phi.childs.append(formula.root.childs[0])
                        ins_formula_sx.append(Formula(phi))
                        print("phi in beta rule implica: ", phi.childs[0].value)
                        #aggiungi un figlio con un set vuoto a formula e aggiungi al set un nodo con il nodo destro di formula
                        psi = formula.root.childs[1]
                        print("psi in beta rule implica: ", psi.value)
                        ins_formula_dx.append(Formula(psi))
                        new_nodo_sx = self.Nodo(ins_formula_sx)
                        new_nodo_dx = self.Nodo(ins_formula_dx)
                        node.childs.append(new_nodo_sx)
                        node.childs.append(new_nodo_dx)
                        new_foglie.append(new_nodo_sx)
                        new_foglie.append(new_nodo_dx)
                    foglie = new_foglie
            if len(nodo.childs) == 1:
                print(foglie)
                self.risolvi(nodo.childs[0], foglie)
            elif len(nodo.childs) == 2:
                print(foglie)
                self.risolvi(nodo.childs[0], foglie[:int(len(foglie)/2)])
                self.risolvi(nodo.childs[1], foglie[int(len(foglie)/2):])



#tocca trovare un modo per applicare la creazione di nodi solamente alle foglie dell'albero Tableaux
class Node:
    def __init__(self, value):
        self.childs = []
        self.value = value
        self.boolean = None

    def estTermine(self):
        return len(self.childs) == 0
    
    def __str__(self, level=0):
        ret = "\t"*level+repr(self.value)+"\n"
        for child in self.childs:
            ret += child.__str__(level+1)
        return ret

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
or2.childs.append(p) """

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

tableaux = Tableaux(ins_formula_exp)
tableaux.risolvi(tableaux.root, [tableaux.root])
print(tableaux.ret)
print(str(tableaux.root))