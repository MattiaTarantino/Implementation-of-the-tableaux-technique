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
    
    def tableaux(self):
        if self.root1 is None:                      #se si fa in generale va modificato con "if self.root is None"
            return False
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