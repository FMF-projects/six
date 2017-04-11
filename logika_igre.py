import logging

#######################################################
#                      PARAMETRI                      #
#######################################################

IGRALEC_1 = 'red'
IGRALEC_2 = 'blue'
PRAZNO = ''

# neumno, ampak bolj razumljivo v večini primerov
BARVA_1 = IGRALEC_1
BARVA_2 = IGRALEC_2

NEODLOCENO = "neodločeno"
NI_KONEC = "ni konec"

# VELIKOST IGRALNEGA POLJA
STRANICA_SESTKOTNIKA = 20
VELIKOST_MATRIKE = 10


#######################################################
#                        IGRA                         #
#######################################################

class Igra():

    def __init__(self):

        # SEZNAM ŠESTKOTNIKOV
        self.igralno_polje = [[PRAZNO for j in range(VELIKOST_MATRIKE)] for i in range(VELIKOST_MATRIKE)]

        self.na_potezi = IGRALEC_2

        self.zgodovina = []

    def zabelezi_spremembo_barve(self, i, j, barva):
        '''nastavi barvo polja v igralnem polju'''        
        self.igralno_polje[i][j] = barva
    
    def izvedi_potezo(self, i, j):
        barva = self.na_potezi
        if self.veljavnost_poteze(i, j) == True:    
            # shranimo igralno polje preden izvedemo potezo
            kopija = [self.igralno_polje[i][:] for i in range(VELIKOST_MATRIKE)]
            self.zgodovina.append((kopija, barva))
            self.zabelezi_spremembo_barve(i, j, barva)
            

    def veljavnost_poteze(self, i, j):
        '''vrne True, če je poteza veljavna'''
        
        # če je igre konec je igralec nastavljen na None
        # torej je poteza neveljavna
        if self.na_potezi == None:
            return False
            
        okolica = self.seznam_sosedov(i, j)
        stevilo_sosedov = 0
        for sosed in okolica:
            x, y = sosed
            if polje_obstaja(x, y) == True:
                # preverimo barvo soseda
                if self.igralno_polje[x][y] != PRAZNO:
                    stevilo_sosedov += 1
        
        if stevilo_sosedov != 0:
            return True
        else:
            return False

    def veljavne_poteze(self):
        '''vrne seznam veljavnih potez'''
        poteze = []
        for i in range(VELIKOST_MATRIKE):
            for j in range(VELIKOST_MATRIKE):
                if self.veljavnost_poteze(i,j):
                    poteze.append((i, j))
        return poteze
        
    def seznam_sosedov(self, i, j):
        '''vrne seznam parov koordinat sosedov'''
        if i % 2 == 0: # lihe (steti zacnemo z 0)
            okolica = [(i-1, j-1), (i, j-1), (i+1, j-1), (i+1, j), (i, j+1), (i-1, j)]
        else: # sode
            okolica = [(i-1, j), (i, j-1), (i+1, j), (i+1, j+1), (i, j+1), (i-1, j+1)]
        return okolica

        
    def zmagovalni_vzorci(self, i, j):
        '''vrne nastavke zmagovalnih vzorcev glede na sodost/lihost vrstice'''
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
            return [rozica_liha, vodoravna_crta, narascajoca_crta_liha,
                        padajoca_crta_liha, trikotnik_lih, trikotnik_na_glavo_lih]
        else: # sode vrstice
            return [rozica_soda, vodoravna_crta, narascajoca_crta_soda,
                        padajoca_crta_soda, trikotnik_sod, trikotnik_na_glavo_sod]


    def stanje_igre(self):
        '''Vrne (zmagovalna_polja, zmagovalec), ce je nekdo zmagal, NEODLOCENO, ce je plosca polna
        in ni zmagovalca, sicer vrne NI_KONEC.'''
        
        barva = self.na_potezi
        
        je_polno = True #gledamo, ce je celotno polje polno, ce ni, bomo True spremenili v False

        for i in range(VELIKOST_MATRIKE):
            for j in range(VELIKOST_MATRIKE):
                
                polje = self.igralno_polje[i][j]
                je_polno = je_polno and (polje != PRAZNO)

                # funkcijo poklicemo po vsaki potezi, torej lahko pogledamo le barvo
                # igralca, ki je pravkar opravil potezo
                if polje != barva:
                    continue

                # vzorci, ki jih moramo pregledati
                za_pregled = self.zmagovalni_vzorci(i, j)

                for vzorec in za_pregled:
                    stevilo_polj_iste_barve = 0
                    # shranimo si koordinate polj, ki tvorijo zmagovalni vzorec
                    zmagovalna_polja = []

                    for (x, y) in vzorec:
                        if polje_obstaja(x, y) == True:
                            if self.igralno_polje[x][y] == barva:
                                stevilo_polj_iste_barve += 1
                                zmagovalna_polja.append((x,y))        
                        else:
                            break

                    # našli smo vzorec sestavljen iz šestih polj
                    # enake barve, torej imamo zmagovalca
                    if stevilo_polj_iste_barve == 6:
                        zmagovalec = barva
                        return (zmagovalec, zmagovalna_polja)
        
        # igralno polje je polno
        if je_polno == True:
            return (NEODLOCENO, None)
            
        # zmagovalca ni in igralno polje ni polno
        else:
            return (NI_KONEC, None)

    def razveljavi(self):
        self.igralno_polje, self.na_potezi = self.zgodovina.pop()

    def kopija(self):
        '''vrne kopijo igre'''
        k = Igra()
        k.igralno_polje = [self.igralno_polje[i][:] for i in range(VELIKOST_MATRIKE)]
        k.na_potezi = self.na_potezi
        return k

#######################################################
#                  OSTALE FUNKCIJE                    #
#######################################################

def polje_obstaja(x, y):
    '''vrne False, če polje ne obstaja in True, če obstaja'''
    if x < 0 or y < 0 or x > VELIKOST_MATRIKE - 1 or y > VELIKOST_MATRIKE - 1:
        return False
    else:
        return True

def nasprotnik(igralec):
    """Vrne nasprotnika od igralca."""
    if igralec == IGRALEC_1:
        return IGRALEC_2
    elif igralec == IGRALEC_2:
        return IGRALEC_1
    else:
        assert False, "neveljaven nasprotnik"
