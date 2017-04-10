import copy

#######################################################
#                      PARAMETRI                      #
#######################################################

IGRALEC_1 = '1'
IGRALEC_2 = '2'

BARVA1 = 'red'
BARVA2 = 'blue'

NEODLOCENO = "neodločeno"
NI_KONEC = "ni konec"

# barva za zmagovalna polja
BARVA3 = 'black'

# VELIKOST IGRALNEGA POLJA
STRANICA_SESTKOTNIKA = 20
VELIKOST_MATRIKE = 3

        
#######################################################
#                        IGRA                         # 
#######################################################
        
class Igra():

    def __init__(self):

        # SEZNAM ŠESTKOTNIKOV
        self.igralno_polje = [[0 for i in range(VELIKOST_MATRIKE)] for j in range(VELIKOST_MATRIKE)]
        #print(self.igralno_polje)

        self.na_potezi = IGRALEC_2
        
        self.zgodovina = []
 
    
    def veljavnost_poteze(self, id):
        '''vrne True, če je poteza veljavna'''
        for vrstica in self.igralno_polje:
            for polje in vrstica:
              if polje[0] == id:
                i, j, barva = polje[1], polje[2], polje[3]
                if barva != '':
                    continue
                elif barva == '':
                    if self.stevilo_sosedov(i, j) != 0:
                      return True
        

    def stevilo_sosedov(self, i, j):
        '''vrne stevilo pobarvanih sosedov izbranega polja'''
        st_sosedov = 0
        
        # koordinate sosedov se razlikujejo v sodih in lihih vrsticah
        if i % 2 == 0: # lihe (steti zacnemo z 0)
          okolica = [(i-1, j-1), (i, j-1), (i+1, j-1), (i+1, j), (i, j+1), (i-1, j)]
        else: # sode
          okolica = [(i-1, j), (i, j-1), (i+1, j), (i+1, j+1), (i, j+1), (i-1, j+1)]
        
        for sosed in okolica:
            x, y = sosed
            if x < 0 or y < 0:
              continue
            sosed_podatki = safe_list_get(self.igralno_polje, x, y)
            if sosed_podatki != None:
                if sosed_podatki[3] != '':
                    st_sosedov += 1
        return st_sosedov

                    
    def zmagovalni_vzorci(self, i, j):
        '''vrne nastavke zmagovalnih vzorcev glede na sodost/lihost vrstice'''
        # rožica
        ROZICA_liha = [(i, j+1), (i+1, j+1), (i+2, j+1), (i+2, j), (i+1, j-1)]
        ROZICA_soda = [(i, j+1), (i+1, j+2), (i+2, j+1), (i+2, j), (i+1, j)]

        # vodoravna črta
        VODORAVNA_CRTA = [(i, j+1), (i, j+2), (i, j+3), (i, j+4), (i, j+5)]

        # naraščajoča črta
        NARASCAJOCA_CRTA_liha = [(i+1, j-1), (i+2, j-1), (i+3, j-2), (i+4, j-2), (i+5, j-3)]
        NARASCAJOCA_CRTA_soda = [(i+1, j), (i+2, j-1), (i+3, j-1), (i+4, j-2), (i+5, j-2)]

        # padajoča črta
        PADAJOCA_CRTA_liha = [(i+1, j), (i+2, j+1), (i+3, j+1), (i+4, j+2), (i+5, j+2)]
        PADAJOCA_CRTA_soda = [(i+1, j+1), (i+2, j+1), (i+3, j+2), (i+4, j+2), (i+5, j+3)]

        # trikotnik
        TRIKOTNIK_lih = [(i+1, j-1), (i+1, j), (i+2, j-1), (i+2, j), (i+2, j+1)]
        TRIKOTNIK_sod = [(i+1, j), (i+1, j+1), (i+2, j-1), (i+2, j), (i+2, j+1)]

        # trikotnik obrnjen na glavo
        TRIKOTNIK_NA_GLAVO_lih = [(i, j+1), (i, j+2), (i+1, j), (i+1, j+1), (i+2, j+1)]
        TRIKOTNIK_NA_GLAVO_sod = [(i, j+1), (i, j+2), (i+1, j+1), (i+1, j+2), (i+2, j+1)]
        
        if i % 2 == 0: # lihe vrstice
            return [ROZICA_liha, VODORAVNA_CRTA, NARASCAJOCA_CRTA_liha,
                        PADAJOCA_CRTA_liha, TRIKOTNIK_lih, TRIKOTNIK_NA_GLAVO_lih]
        else: # sode vrstice
            return [ROZICA_soda, VODORAVNA_CRTA, NARASCAJOCA_CRTA_soda,
                        PADAJOCA_CRTA_soda, TRIKOTNIK_sod, TRIKOTNIK_NA_GLAVO_sod]
        

    def je_morda_konec(self, barva):
        '''Vrne [zmagovalna_polja, zmagovalec], ce je nekdo zmagal, NEODLOCENO, ce je plosca polna
        in ni zmagovalca, sicer vrne NI_KONEC.'''
        je_polno = True #gledamo, ce je celotno polje polno, ce ni, bomo True spremenili v False
        print(self.igralno_polje)
        for vrstica in self.igralno_polje:
            for polje in vrstica:
                print(polje)
                id, i, j, barva_polja = polje
                
                # funkcijo poklicemo po vsaki potezi, torej lahko pogledamo le barvo
                # igralca, ki je pravkar opravil potezo
                if barva_polja != barva:
                    continue
                
                # prav tako ne bomo preverjali vzorcev za prazna polja
                if barva_polja == '':
                    je_polno = False
                    continue
                
                # vzorci, ki jih moramo pregledati
                za_pregled = self.zmagovalni_vzorci(i, j)
                    
                for vzorec in za_pregled:
                    stevilo_polj_iste_barve = 1
                    # shranimo si id polj, ki tvorijo zmagovalni vzorec
                    zmagovalna_polja = [id]
                    
                    for sosednje_polje in vzorec:
                        m, n = sosednje_polje
                        sosednje_polje_podatki = safe_list_get(self.igralno_polje, m, n)
                        
                        if sosednje_polje_podatki != None:
                            if sosednje_polje_podatki[3] == barva:
                                stevilo_polj_iste_barve += 1
                                zmagovalna_polja.append(sosednje_polje_podatki[0])
                        else:
                            break
                                
                    if stevilo_polj_iste_barve == 6:
                        if barva_polja == BARVA1:
                            zmagovalec = IGRALEC_1
                        else:
                            zmagovalec = IGRALEC_2
                        return [zmagovalna_polja, zmagovalec]
        if je_polno == True:
            return NEODLOCENO
        else:
            return NI_KONEC
            
    def razveljavi(self):
        self.igralno_polje, self.na_potezi = self.zgodovina.pop()
        
    def kopija(self):
        '''vrne kopijo igre'''
        k = Igra()
        k.igralno_polje = copy.deepcopy(self.igralno_polje)
        k.na_potezi = self.na_potezi
        return k

    def stanje_igre(self):
        barva = barva_na_potezi(self.na_potezi)
        stanje = self.je_morda_konec(barva)
        if type(stanje) == list:
            return (stanje[0], stanje[1])
        elif stanje == NEODLOCENO:
            return (NEODLOCENO, None)
        elif stanje == NI_KONEC:
            return (NI_KONEC, None)

    
    
#######################################################
#                  OSTALE FUNKCIJE                    # 
#######################################################

def barva_na_potezi(igralec):
    if igralec == IGRALEC_1:
        return BARVA1
    elif igralec == IGRALEC_2:
        return BARVA2

def safe_list_get(matrika, i, j):
    '''preveri, če je polje (i,j) v matriki (seznamu)'''
    try:
        return matrika[i][j]
    except IndexError:
        return None

def nasprotnik(igralec):
    """Vrne nasprotnika od igralca."""
    if igralec == IGRALEC_1:
        return IGRALEC_2
    elif igralec == IGRALEC_2:
        return IGRALEC_1
    else:
        assert False, "neveljaven nasprotnik"
