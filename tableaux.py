#implementazione albero
#albero -> value (operatore o termine); boolean: assegnazione del valore di verità (se termine)
#          può essere termine solo se foglia
#          figli o figlio sx/dx
class Formula:
    class Node:
        def __init__(self, value):
            self.childs = []
            self.value = value
            self.boolean = None

        def estFoglia(self):
            return len(self.childs) == 0
        
    def __init__(self):
        self.root1 = self.Node("¬")
        implica1 = self.Node("->")
        self.root1.childs.append(implica1)
        or1 = self.Node("||")
        or2 = self.Node("||")
        implica1.childs.append(or1)
        implica1.childs.append(or2)
        q = self.node("q")
        p = self.node("p")
        or1.childs.append(q)
        or1.childs.append(p)
        or2.childs.append(q)
        or2.childs.append(p)

        self.root2 = self.Node("¬")
        implica1 = self.Node("->")
        self.root2.childs.append(implica1)
        or1 = self.Node("||")
        and1 = self.Node("&&")
        implica1.childs.append(or1)
        implica1.childs.append(and1)
        q = self.node("q")
        p = self.node("p")
        or1.childs.append(q)
        or1.childs.append(p)
        and1.childs.append(q)
        and1.childs.append(p)


    #definire lista di operatori
    def estOperator(self, nodo):
        operators = ["&&", "||", "¬", "¬¬", "->"] #and, or, not, not not, implica
        if nodo.value in operators:
            return True
        else:
            return False
    
    #def tableaux(self):
    #    if self.root1 is None:                      #se si fa in generale va modificato con "if self.root is None"
    #       return False
        #controllo del nodo se è un operatore o termine
        #controllo se l'operatore è ¬, nel caso controllo il numero di figli, se è uno vedo se è un termine o un ¬
        #caso 1: controllo il boolean del nodo per vedere se c'è cambio: se c'è retruna false per questa analisi, se non c'è assegna false;
        #caso 2: elimino i due nodi ¬
        #se ho un termine controllo il suo boolean: se è false return false, altrimneti assegna true
        #controllo l'applicazione di alpha rule attraverso l'operatore che ho; nel caso di ¬ e un figlio operatore non cambia, se ho precedentemente applicato una alpha rule vedo su quale parte posso applicarla prima
        #se posso applicarla lo faccio e divido l'analisi in due formule; come farlo? richiamo tableaux sulla formula nuova? lista di parti?
        #se non posso applicare alpha rule applico beta rule e applico il tableaux su entrambi i rami che si creano
        #cosa restituire? in teoria se ho una soluzione senza contraddizini: return true, altrimenti false

#tableau:
#scelta se ricorsivo o iterativo
#passo base: controllo se l'albero esiste altrimenti return false
#passo base 2: controllo se l'albero ha solo un nodo, ovvero un solo elemento: return true
#analizza se si può effettuare ¬¬elimination
#analizza primo nodo e suoi sottoalberi e verifica se è possibile attivare una alpha rule(controlla il value del padre e se c'è un not prima)
#se non si possono applicare alpha rule applicare beta rule
# a ogni rule applicata verificare se si ottiene un figlio con value = termine, se si dare valore boolean al termine
#verifica di non contraddizione sui boolean, se c'è chiudi il ramo
#return di base è false, ma se c'è un ramo che arriva alla foglia senza contraddizioni return true
#problemi: come si modifica l'albero con l'applicazione delle rule?; probabilmente ricorsivo >>> iterativo (tocca rivedere i passi base); come fare se ho un set di formule iniziali?

#tableaux deve essere un metodo a cui viene passata una formula (ovvero self); la formula la inseriamo inizialmente in modo statico e poi vediamo se farlo dinamico; statico quindi l'albero che rappresenta la formula deve già esistere.
#per farla già esistere creiamo tutto l'albero in __init__ di Formula e lo analizziamo da là (l'analisi si fa comunque generica perchè l'inizializzazione statica si può sempre cambiare)
#inizialmente ne creiamo un paio(quelle del prof)
#la versione dinamica richiederà un convertitore stringa -> albero delle formule (non ho idea di come si faccia)
# !!!!!!!!!!!!i nodi con i termini si possono usare dall'inizio e il controllo sulla non contraddizione si verifica con il metodo check_boolean!!!!!!!!!!!!!!!!!!!!!!!(potrebbe non funzionare perchè stesso nodo in memoria quindi va analizzato)
#verificare che gli alberi statici siano giusti
#da analizzare: per ora il passo base usa self.root ma per farlo ricorsivo bisogna guardare il nodo root del sottoalbero che stiamo analizzando
#vanno implementate funzioni di aggiunta/eliminazione di nodi in testa per far si di poter modificare i singoli sottoalberi quando si applicano le rule
#come fare la return ogni volta per capire il risultato finale?



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
    def __init__(self, ins_formula):
        self.ins_formula = ins_formula
    
    #def risolvi(self):
        #if ins_formula is None:
            #return false
        #salva i nodi con i termini di ins_formula
        #inizio controllo dei nodi
        #1 CONTROLLO: DOPPIA NEGAZIONE/ASSEGNAZOINE BOOLEAN
        #controllo se c'è "¬"
            #se si controllo i figli
                #se è uno ed è "¬"
                    #applico semplificazione di doppia negazione
                    #creo un nodo con solamente il figlio senza negazioni a ins_formula
                #se è un termine
                    #controllo il suo boolean
                        #se è true chiudo la branch(come fare?)
                        #return false
                        #else boolean = false
                            #controlla i boolean dei termini id ins_formula
                            #se sono tutti diversi da None return true
        #se ho un termine
            #controllo il suo boolean
                #se è false chiudo la branch(come fare?)
                #return false
                #else boolean = true
                    #controlla i boolean dei termini id ins_formula
                    #se sono tutti diversi da None return true
                #altrimenti vado avanti
        #vado avanti nel set finchè non finisco
        #2 CONTROLLO: ALPHA RULE
        #controllo se c'è "¬"
            #se si controllo i figli
                #verifica se applicabile alpha rule
                #se è un "||"
                    #aggiungi un nodo a ins_formula che contiene un set vuoto
                    #aggiungi un nodo al set con "¬", a cui aggiugni un figlio con il nodo sinistro di formula
                    #aggiungi un nodo al set con "¬", a cui aggiugni un figlio con il nodo destro di formula
                #se è un "->"
                    #aggiungi un nodo a formula che contiene un set vuoto
                    #aggiungi un nodo al set con nodo sinistro di formula
                    #aggiungi un nodo al set con "¬", a cui aggiugni un figlio con il nodo destro di formula
        #controllo se c'è "&&"
            #aggiungi un nodo a ins_formula con un set vuoto
            #aggiungi un nodo con il figlio sinistro al set
            #aggiungi un nodo con il figlio destro al set
        #3 CONTROLLO: BETA RULE
        #controllo se c'è "¬"
            #se si controllo i figli
                #verifica se applicabile una beta rule
                #se è un "&&"
                    #aggiungi un figlio con un set vuoto a formula e aggiungi al set un nodo con "¬", a cui assegni un figlio con il nodo sinistro di formula
                    #aggiungi un figlio con un set vuoto a formula e aggiungi al set un nodo con "¬", a cui assegni un figlio con il nodo destro di formula
        #controllo se c'è "||"
            #aggiungi un figlio con un set vuoto a formula e aggiungi al set un nodo con il nodo sinistro di formula
            #aggiungi un figlio con un set vuoto a formula e aggiungi al set un nodo con il nodo destro di formula
        #controllo se c'è "->"
            #aggiungi un figlio con un set vuoto a formula e aggiungi al set un nodo con "¬", a cui assegni un figlio con il nodo sinistro di formula
            #aggiungi un figlio con un set vuoto a formula e aggiungi al set un nodo con il nodo destro di formula
        #applica di nuovo sui figli di ins_formula

        #ultimo step quale è la return da fare? penso a qualcosa come self.res = false e se ho una return di una branch = true allora smetto di eseguire il codice e returno true, altrimenti analizzo tutte le branch e returno alla fine false





#tocca trovare un modo per applicare la creazione di nodi solamente alle foglie dell'albero Tableaux
#tocca trovare un modo per applicare le rule in ordine nel caso mi ritrovi un set di formule; un'idea è la creazione di una queue delle formule da analizzare a cui applicare le rule(con che ordine inserire?)