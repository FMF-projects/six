import logging

#######################################################
#                      PARAMETRI                      #
#######################################################

PRAZNO = ''
NEODLOCENO = "neodločeno"
NI_KONEC = "ni konec"

# VELIKOST IGRALNEGA POLJA
# nastavi gui ob začetku igre glede na željeno izbiro
velikost_matrike = None

# barva igralca_1 in igralca_2
# nastavi gui ob začetku igre, glede na izbrano barvno kombinacijo
prvi = None
drugi = None

#######################################################
#                        IGRA                         #
#######################################################

class Igra():

    def __init__(self):

        # SEZNAM ŠESTKOTNIKOV
        self.igralno_polje = [[PRAZNO for j in range(velikost_matrike)] for i in range(velikost_matrike)]

        self.na_potezi = drugi

        self.zgodovina = []
        
        
    ##############
    # VELJAVNOST #
    ##############
    def veljavnost_poteze(self, i, j):
        '''vrne True, če je poteza veljavna'''
        if self.na_potezi == None:
            assert False, "gledamo veljavnost poteze, ko nihče ni na potezi"

        if self.igralno_polje[i][j] != PRAZNO:
            return False
        else:
            # gledamo, ali je kak neprazen sosed
            stevilo_sosedov = 0
            for (x,y) in seznam_sosedov(i, j):
                if self.igralno_polje[x][y] != PRAZNO:
                    return True
            # ni bilo nepraznega soseda
            return False
            
    def veljavne_poteze(self):
        '''vrne seznam veljavnih potez'''
        poteze = set()
        for i in range(velikost_matrike):
            for j in range(velikost_matrike):
                if self.igralno_polje[i][j] != PRAZNO:
                    for (x,y) in seznam_sosedov(i,j):
                        if self.igralno_polje[x][y] == PRAZNO:
                            poteze.add((x,y))
        return poteze  

        
    ##################
    # IZVEDBA POTEZE #
    ##################
    
    def zmagovalni_vzorci(self, i, j):
        '''vrne seznam zmagovalnih vzorcev glede na sodost/lihost vrstice'''
        # rožica
        rozica_liha = [(i, j), (i, j+1), (i+1, j+1), (i+2, j+1), (i+2, j), (i+1, j-1)]
        rozica_soda = [(i, j), (i, j+1), (i+1, j+2), (i+2, j+1), (i+2, j), (i+1, j)]

        # vodoravna črta
        vodoravna_crta = [(i, j), (i, j+1), (i, j+2), (i, j+3), (i, j+4), (i, j+5)]

        # naraščajoča črta
        narascajoca_crta_liha = [(i, j), (i+1, j-1), (i+2, j-1), (i+3, j-2), (i+4, j-2), (i+5, j-3)]
        narascajoca_crta_soda = [(i, j), (i+1, j), (i+2, j-1), (i+3, j-1), (i+4, j-2), (i+5, j-2)]

        # padajoča črta
        padajoca_crta_liha = [(i, j), (i+1, j), (i+2, j+1), (i+3, j+1), (i+4, j+2), (i+5, j+2)]
        padajoca_crta_soda = [(i, j), (i+1, j+1), (i+2, j+1), (i+3, j+2), (i+4, j+2), (i+5, j+3)]

        # trikotnik
        trikotnik_lih = [(i, j), (i+1, j-1), (i+1, j), (i+2, j-1), (i+2, j), (i+2, j+1)]
        trikotnik_sod = [(i, j), (i+1, j), (i+1, j+1), (i+2, j-1), (i+2, j), (i+2, j+1)]

        # trikotnik obrnjen na glavo
        trikotnik_na_glavo_lih = [(i, j), (i, j+1), (i, j+2), (i+1, j), (i+1, j+1), (i+2, j+1)]
        trikotnik_na_glavo_sod = [(i, j), (i, j+1), (i, j+2), (i+1, j+1), (i+1, j+2), (i+2, j+1)]

        if i % 2 == 0: # lihe vrstice
            kandidati = [rozica_liha, vodoravna_crta, narascajoca_crta_liha,
                         padajoca_crta_liha, trikotnik_lih, trikotnik_na_glavo_lih]
        else: # sode vrstice
            kandidati = [rozica_soda, vodoravna_crta, narascajoca_crta_soda,
                        padajoca_crta_soda, trikotnik_sod, trikotnik_na_glavo_sod]
        
        # vrnemo le tiste vzorce, ki v katerih so vsa polja veljavna (obstajajo)
        return [k for k in kandidati if veljavna_sestka(k)]
    
    def zabelezi_spremembo_barve(self, i, j, barva):
        '''na (i,j) mesto v igralnem polju zapiše barvo'''
        self.igralno_polje[i][j] = barva

    def izvedi_potezo(self, i, j):
        '''če je poteza veljavna jo izvede in vrne (zmagovalec, zmagovalna_polja), sicer vrne None'''
        
        # poteza je veljavna
        if self.veljavnost_poteze(i, j) == True:
            
            # shranimo igralno polje preden izvedemo potezo
            kopija = [self.igralno_polje[i][:] for i in range(velikost_matrike)]
            barva = self.na_potezi
            self.zgodovina.append((kopija, barva))

            # zabelezimo spremembo barve
            self.zabelezi_spremembo_barve(i, j, barva)

            # preverimo, ali je igre morda ze konec
            (zmagovalec, zmagovalna_polja) = self.stanje_igre()
            if zmagovalec == NI_KONEC:
                # spremenimo igralca na potezi
                self.na_potezi = nasprotnik(barva)
            else:
                # spremenimo igralca na potezi na None
                self.na_potezi = None

            return (zmagovalec, zmagovalna_polja)
        
        # poteza ni veljavna
        else:
            return None


    ###############
    # STANJE IGRE #
    ###############

    def stanje_igre(self):
        '''Vrne (zmagovalec, zmagovalna_polja), ce je nekdo zmagal, (NEODLOCENO, None) ce je plosca polna
        in ni zmagovalca, sicer vrne (NI_KONEC, None)'''

        # gledamo, ce je celotno polje polno, ce ni, bomo True spremenili v False
        je_polno = True 

        for i in range(velikost_matrike):
            for j in range(velikost_matrike):

                polje = self.igralno_polje[i][j]
                je_polno = je_polno and (polje != PRAZNO)

                if polje != PRAZNO:
                    # pregledamo vzorce za to polje
                    for vzorec in self.zmagovalni_vzorci(i, j):
                        stevilo_polj_iste_barve = 0
                        # shranimo si koordinate polj, ki tvorijo zmagovalni vzorec
                        zmagovalna_polja = []
                        for (x, y) in vzorec:
                            if self.igralno_polje[x][y] == polje:
                                stevilo_polj_iste_barve += 1
                                zmagovalna_polja.append((x,y))
                            else:
                                break
                        if stevilo_polj_iste_barve == 6:
                            # našli smo vzorec sestavljen iz šestih polj
                            # enake barve, torej imamo zmagovalca "polje"
                            return (polje, zmagovalna_polja)

        # igralno polje je polno
        if je_polno == True:
            return (NEODLOCENO, None)

        # zmagovalca ni in igralno polje ni polno
        else:
            return (NI_KONEC, None)
            
    ########
    # .... #
    ########

    def razveljavi(self):
        self.igralno_polje, self.na_potezi = self.zgodovina.pop()

    def kopija(self):
        '''vrne kopijo igre'''
        k = Igra()
        k.igralno_polje = [self.igralno_polje[i][:] for i in range(velikost_matrike)]
        k.na_potezi = self.na_potezi
        return k

#######################################################
#                  OSTALE FUNKCIJE                    #
#######################################################

def veljavno_polje(x,y):
    '''Vrne True, če polje obstaja, sicer False'''
    return (0 <= x < velikost_matrike and 0 <= y < velikost_matrike)

def veljavna_sestka(lst):
    '''Vrne True, če so vsa polja v šestki veljavna'''
    for (x,y) in lst:
        if not veljavno_polje(x,y):
            return False
    return True

def seznam_sosedov(i, j):
        '''vrne seznam koordinat veljavnih sosedov'''
        if i % 2 == 0: # lihe (steti zacnemo z 0)
            kandidati = [(i-1, j-1), (i, j-1), (i+1, j-1), (i+1, j), (i, j+1), (i-1, j)]
        else: # sode
            kandidati = [(i-1, j), (i, j-1), (i+1, j), (i+1, j+1), (i, j+1), (i-1, j+1)]
        return [(i,j) for (i,j) in kandidati if veljavno_polje(i,j)]

def nasprotnik(igralec):
    """Vrne nasprotnika od igralca."""
    if igralec == prvi:
        return drugi
    elif igralec == drugi:
        return prvi
    else:
        assert False, "neveljaven nasprotnik"
