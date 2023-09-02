#implementazione albero
#albero -> value (operatore o termine); boolean: assegnazione del valore di verità (se termine)
#          può essere termine solo se foglia
#          figli o figlio sx/dx
class Formula:
    
    def __init__(self, root):
        self.termini = []
        self.root = root
        

        #self.root2 = self.Node("¬")
        #implica1 = self.Node("->")
        #self.root2.childs.append(implica1)
        #or1 = self.Node("||")
        #and1 = self.Node("&&")
        #implica1.childs.append(or1)
        #implica1.childs.append(and1)
        """ 
        q = self.Node("q")
        p = self.Node("p")
        or1.childs.append(q)
        or1.childs.append(p)
        and1.childs.append(q)
        and1.childs.append(p)

 """
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
    

#IDEA ALTERNATIVA
#tableaux non è un metodo di formula ma una classe a se stante che prende come parametro una formula
#vantaggio principale analisi della formula ricorsiva e possibilità di creare un nuovo albero che rappresenta il tableaux stesso
#svantaggio utilizzo della memoria (sti cazzi per ora) e vedere come vengono assegnati i vari valori
#IDEA MIGLIORE A MIO AVVISO E QUELLA SU CUI LAVORERò per ora
#va generalizzata l'idea di albero
#le idee dell'analisi delle varie formule sono le stesse di sopra
#PER FAR FUNZIONARE QUESTO VA RIVISTA TUTTA LA PARTE PRIMA
#idea principale del codice: creare un albero di analisi della formula; si cerca in ordine l'appilcazione di doppia negazione/assegnazione, poi si verifica l'applicabilità di alpha rule, poi di beta rule; ogni volta verifico sul set principale e poi verifico sui vari figli

#ins_formula è un nodo che contiene un set di formule
#si lo mo è una lista e non un insieme ma pace
class Tableaux():

    class Nodo():
        def __init__(self, ins_formula):
            self.ins_formula = ins_formula
            self.childs = []

    def __init__(self, ins_formula):
        self.ret = False
        self.terms = []
        self.terms_len = len(self.terms)
        self.root = self.Nodo(ins_formula)
        self.last_nodes = [self.root]

    def risolvi(self, nodo):
        if self.ret == False:
            if nodo.ins_formula is None:
                return
            #salva i nodi con i termini di ins_formula
            for formula in nodo.ins_formula:
                for termine in formula.termini:
                    if termine not in self.terms:
                        self.terms.append(termine)
            #inizio controllo dei nodi
            #1 CONTROLLO: DOPPIA NEGAZIONE/ASSEGNAZOINE BOOLEAN
            for formula in nodo.ins_formula:
                #controllo se c'è "¬"
                if formula.root.value == "¬":
                    #se si controllo i figli
                    #se è uno ed è "¬"
                    if formula.root.childs[0].value == "¬":
                        #applico semplificazione di doppia negazione
                        #creo un nodo con solamente il figlio senza negazioni a ins_formula
                        new_formula = Formula(formula.root.childs[0].childs[0])
                        new_nodo = self.Nodo([new_formula])
                        for node in self.last_nodes:
                            node.childs.append(new_nodo)
                        self.last_nodes = [new_nodo]
                    #se è un termine
                    if formula.root.childs[0].estTermine():
                        termine = formula.root.childs[0]
                        #controllo il suo boolean
                        #se è true chiudo la branch
                        if termine.boolean == True:
                            return
                        else:
                            #boolean = false
                            termine.boolean = False
                            count = 0
                            #controlla i boolean dei termini id ins_formula
                            for term in self.terms:
                                #se sono tutti diversi da None return true
                                if term.boolean is not None:
                                    count += 1
                            if count == self.terms_len:
                                self.ret = True
                                return
                if formula.root.childs[0].estTermine():
                        termine = formula.root.childs[0]
                        #controllo il suo boolean
                        #se è true chiudo la branch
                        if termine.boolean == False:
                            return
                        else:
                            #boolean = true
                            termine.boolean = True
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
                        new_ins_formula = []
                        #aggiungi un nodo al set con "¬", a cui aggiugni un figlio con il nodo sinistro di formula
                        phi = Node("¬")
                        phi.childs.append(Node(formula.root.childs[0].childs[0].value))
                        new_ins_formula.append(Formula(phi))
                        #aggiungi un nodo al set con "¬", a cui aggiugni un figlio con il nodo destro di formula
                        psi = Node("¬")
                        psi.childs.append(Node(formula.root.childs[0].childs[1].value))
                        new_ins_formula.append(Formula(psi))
                        #aggiungi un nodo a ins_formula che contiene un set vuoto
                        new_nodo = self.Nodo(new_ins_formula)
                        for node in self.last_nodes:
                            node.childs.append(new_nodo)
                        self.last_nodes = [new_nodo]
                    #se è un "->"
                    if formula.root.childs[0].value == "->":
                        new_ins_formula = []
                        #aggiungi un nodo al set con nodo sinistro di formula
                        phi = Node(formula.root.childs[0].childs[0].value)
                        new_ins_formula.append(Formula(phi))
                        #aggiungi un nodo al set con "¬", a cui aggiugni un figlio con il nodo destro di formula
                        psi = Node("¬")
                        psi.childs.append(Node(formula.root.childs[0].childs[1].value))
                        new_ins_formula.append(Formula(psi))
                        #aggiungi un nodo a ins_formula che contiene un set vuoto
                        new_nodo = self.Nodo(new_ins_formula)
                        for node in self.last_nodes:
                            node.childs.append(new_nodo)
                        self.last_nodes = [new_nodo]
                #controllo se c'è "&&"
                if formula.root.value == "&&":
                    new_ins_formula = []
                    #aggiungi un nodo con il figlio sinistro al set
                    phi = Node(formula.root.childs[0].childs[0].value)
                    new_ins_formula.append(Formula(phi))
                    #aggiungi un nodo con il figlio destro al set
                    psi = Node(formula.root.childs[0].childs[1].value)
                    new_ins_formula.append(Formula(psi))
                    #aggiungi un nodo a ins_formula con un set vuoto
                    new_nodo = self.Nodo(new_ins_formula)
                    for node in self.last_nodes:
                        node.childs.append(new_nodo)
                    self.last_nodes = [new_nodo]
            #3 CONTROLLO: BETA RULE
            for formula in nodo.ins_formula:
                #controllo se c'è "¬"
                if formula.root.value == "¬":
                    #se si controllo i figli
                    #verifica se applicabile una beta rule
                    #se è un "&&"
                    if formula.root.childs[0].value == "&&":
                        ins_formula_sx = []
                        ins_formula_dx = []
                        #aggiungi un figlio con un set vuoto a formula e aggiungi al set un nodo con "¬", a cui assegni un figlio con il nodo sinistro di formula
                        phi = Node("¬")
                        phi.childs.append(Node(formula.root.childs[0].childs[0].value))
                        ins_formula_sx.append(Formula(phi))
                        #aggiungi un figlio con un set vuoto a formula e aggiungi al set un nodo con "¬", a cui assegni un figlio con il nodo destro di formula
                        psi = Node("¬")
                        psi.childs.append(Node(formula.root.childs[0].childs[1].value))
                        ins_formula_dx.append(Formula(psi))
                        new_nodo_sx = self.Nodo(ins_formula_sx)
                        new_nodo_dx = self.Nodo(ins_formula_dx)
                        self.nodes = []
                        for node in self.last_nodes:
                            node.childs.append(new_nodo_sx)
                            node.childs.append(new_nodo_dx)
                            self.last_nodes.append(new_nodo_sx)
                            self.last_nodes.append(new_nodo_dx)
                #controllo se c'è "||"
                if formula.root.value == "||":
                    ins_formula_sx = []
                    ins_formula_dx = []
                    #aggiungi un figlio con un set vuoto a formula e aggiungi al set un nodo con il nodo sinistro di formula
                    phi = Node(formula.root.childs[0].childs[0].value)
                    ins_formula_sx.append(Formula(phi))
                    #aggiungi un figlio con un set vuoto a formula e aggiungi al set un nodo con il nodo destro di formula
                    psi = Node(formula.root.childs[0].childs[1].value)
                    ins_formula_dx.append(Formula(psi))
                    new_nodo_sx = self.Nodo(ins_formula_sx)
                    new_nodo_dx = self.Nodo(ins_formula_dx)
                    self.nodes = []
                    for node in self.last_nodes:
                        node.childs.append(new_nodo_sx)
                        node.childs.append(new_nodo_dx)
                        self.last_nodes.append(new_nodo_sx)
                        self.last_nodes.append(new_nodo_dx)
                #controllo se c'è "->"
                if formula.root.value == "->":
                    ins_formula_sx = []
                    ins_formula_dx = []
                    #aggiungi un figlio con un set vuoto a formula e aggiungi al set un nodo con "¬", a cui assegni un figlio con il nodo sinistro di formula
                    phi = Node("¬")
                    phi.childs.append(Node(formula.root.childs[0].childs[0].value))
                    ins_formula_sx.append(Formula(phi))
                    #aggiungi un figlio con un set vuoto a formula e aggiungi al set un nodo con il nodo destro di formula
                    psi = Node(formula.root.childs[0].childs[1].value)
                    ins_formula_dx.append(Formula(psi))
                    new_nodo_sx = self.Nodo(ins_formula_sx)
                    new_nodo_dx = self.Nodo(ins_formula_dx)
                    self.nodes = []
                    for node in self.last_nodes:
                        node.childs.append(new_nodo_sx)
                        node.childs.append(new_nodo_dx)
                        self.last_nodes.append(new_nodo_sx)
                        self.last_nodes.append(new_nodo_dx)
            for figlio in nodo.childs:
                self.risolvi(figlio)



#tocca trovare un modo per applicare la creazione di nodi solamente alle foglie dell'albero Tableaux
class Node:
    def __init__(self, value):
        self.childs = []
        self.value = value
        self.boolean = None

    def estTermine(self):
        return len(self.childs) == 0

ins_formula_exp = []
root = Node("¬")
esempio = Formula(root)
ins_formula_exp.append(esempio)
implica1 = Node("->")
root.childs.append(implica1)
or1 = Node("||")
or2 = Node("||")
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

tableaux = Tableaux(ins_formula_exp)
tableaux.risolvi(tableaux.root)
print(tableaux.ret)