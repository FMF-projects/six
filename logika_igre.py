def safe_list_get(matrika, i, j):
  '''preveri, če je polje (i,j) v matriki (seznamu)'''
  try:
    return matrika[i][j]
  except IndexError:
    return None

IGRALEC_1 = '1'
IGRALEC_2 = '2'

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
VELIKOST_MATRIKE = 5
    
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
      




