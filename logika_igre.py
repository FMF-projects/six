def safe_list_get(matrika, i, j):
  '''preveri, če je polje (i,j) v matriki (seznamu)'''
  try:
    return matrika[i][j]
  except IndexError:
    return None

IGRALEC_1 = '1'
IGRALEC_2 = '2'
BARVA1 = 'red'
BARVA2 = 'black'

def nasprotnik(igralec):
    """Vrni nasprotnika od igralca."""
    if igralec == IGRALEC_1:
        return IGRALEC_2
    elif igralec == IGRALEC_2:
        return IGRALEC_1
    else:
        assert False, "neveljaven nasprotnik"

# VELIKOST IGRALNEGA POLJA
STRANICA_SESTKOTNIKA = 20
VELIKOST_MATRIKE = 15
    
class Igra():

    def __init__(self):

        # SEZNAM ŠESTKOTNIKOV
        self.igralno_polje = [[0 for i in range(VELIKOST_MATRIKE)] for j in range(VELIKOST_MATRIKE)]
        #print(self.igralno_polje)

        self.na_potezi = IGRALEC_1


        # ZACETNO IGRALNO POLJE (MORA BITI, SICER JE TEZKO ZACETI NOVO IGRO)
        #self.zacetno_igralno_polje = []
 
    
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

        # objekte zacne stevilciti z 1
        # vrstica = (id_sestkotnika - 1) // VELIKOST_MATRIKE
        # stolpec = (id_sestkotnika - 1) % VELIKOST_MATRIKE
        # polje = self.igralno_polje[vrstica][stolpec]
        # print(polje)
        # i, j, barva = polje[1], polje[2], polje[3]
        # if barva != '':
         # return False
        # elif barva == '':
         # if self.stevilo_sosedov(i, j) != 0:
           # return True
        

    def stevilo_sosedov(self, i, j):
        st_sosedov = 0
        # koordinate sosedov se razlikujejo v sodih in lihih vrsticah
        if i % 2 == 0: # sode
          okolica = [(i-1, j-1), (i, j-1), (i+1, j-1), (i+1, j), (i, j+1), (i-1, j)]
        else: # lihe
          okolica = [(i-1, j), (i, j-1), (i+1, j), (i+1, j+1), (i, j+1), (i-1, j+1)]
        for sosed in okolica:
            x, y = sosed
            #print(sosed)
            if x < 0 or y < 0:
              continue
            sosed_podatki = safe_list_get(self.igralno_polje, x, y)
            if sosed_podatki != None:
                if sosed_podatki[3] != '':
                    st_sosedov += 1
        return st_sosedov

    def je_morda_konec(self):
        for vrstica in self.igralno_polje:
            for polje in vrstica:
                if self.rozica(polje[1], polje[2]):
                    return True
                if self.vodoravna_crta(polje[1], polje[2]):
                    return True
                if self.padajoca_crta(polje[1], polje[2]):
                    return True
                if self.narascajoca_crta(polje[1], polje[2]):
                    return True

    def rozica(self, i, j):
        if i % 2 == 0: #lihe vrstice
            za_pregled = [(i, j + 1), (i + 1, j + 1), (i + 2, j + 1), (i + 2, j), (i + 1, j - 1)]
        else: #sode
            za_pregled = [(i, j + 1), (i + 1, j + 2), (i + 2, j + 1), (i + 2, j), (i + 1, j)]
        stevilo_polj_iste_barve = 1
        barva = BARVA1 if self.na_potezi == IGRALEC_1 else BARVA2
        for polje in za_pregled:
            m, n = polje
            polje_podatki = safe_list_get(self.igralno_polje, m, n)
            if polje_podatki != None:
                if polje_podatki[3] == barva:
                    stevilo_polj_iste_barve += 1
            else:
                break
        if stevilo_polj_iste_barve == 6:
            return True
        else:
            return False

    def vodoravna_crta(self, i, j):
        stevilo_polj_iste_barve = 1
        barva = BARVA1 if self.na_potezi == IGRALEC_1 else BARVA2
        za_pregled = [(i,j + k) for k in range(1,6)]
        for polje in za_pregled:
            m, n = polje
            polje_podatki = safe_list_get(self.igralno_polje, m, n)
            if polje_podatki != None:
                if polje_podatki[3] == barva:
                    stevilo_polj_iste_barve += 1
            else:
                break
        if stevilo_polj_iste_barve == 6:
            return True
        else:
            return False

    def padajoca_crta(self, i, j):
        if i % 2 == 0:  # lihe vrstice
            za_pregled = [(i+1, j), (i + 2, j + 1), (i + 3, j + 1), (i + 4, j+2), (i + 5, j +2)]
        else:  # sode
            za_pregled = [(i+1, j + 1), (i + 2, j + 1), (i + 3, j + 2), (i + 4, j+2), (i + 5, j+3)]
        stevilo_polj_iste_barve = 1
        barva = BARVA1 if self.na_potezi == IGRALEC_1 else BARVA2
        for polje in za_pregled:
            m, n = polje
            polje_podatki = safe_list_get(self.igralno_polje, m, n)
            if polje_podatki != None:
                if polje_podatki[3] == barva:
                    stevilo_polj_iste_barve += 1
            else:
                break
        if stevilo_polj_iste_barve == 6:
            return True
        else:
            return False

    def narascajoca_crta(self, i, j):
        if i % 2 == 0:  # lihe vrstice
            za_pregled = [(i + 1, j -1), (i + 2, j -1), (i + 3, j - 2), (i + 4, j - 2), (i + 5, j -3)]
        else:  # sode
            za_pregled = [(i + 1, j), (i + 2, j -1), (i + 3, j -1), (i + 4, j - 2), (i + 5, j -2)]
        stevilo_polj_iste_barve = 1
        barva = BARVA1 if self.na_potezi == IGRALEC_1 else BARVA2
        for polje in za_pregled:
            m, n = polje
            polje_podatki = safe_list_get(self.igralno_polje, m, n)
            if polje_podatki != None:
                if polje_podatki[3] == barva:
                    stevilo_polj_iste_barve += 1
            else:
                break
        if stevilo_polj_iste_barve == 6:
            return True
        else:
            return False


