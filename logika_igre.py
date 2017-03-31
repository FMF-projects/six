def safe_list_get(matrika, i, j):
  '''preveri, če je polje (i,j) v matriki (seznamu)'''
  try:
    return matrika[i-1][j-1] #indeksi se zacnejo z 1
  except IndexError:
    return None

# VELIKOST IGRALNEGA POLJA
STRANICA_SESTKOTNIKA = 20
VELIKOST_MATRIKE = 20
    
class Igra():

    def __init__(self):

        # SEZNAM ŠESTKOTNIKOV
        self.igralno_polje = [[0 for i in range(VELIKOST_MATRIKE)] for j in range(VELIKOST_MATRIKE)]
        #print(self.igralno_polje)
   
    def veljavnost_poteze(self, id):
        '''vrne seznam veljavnih potez'''
        poteze = []
        for vrstica in self.igralno_polje:
            for polje in vrstica:
              if polje[0] == id:
                i, j, barva = polje[1], polje[2], polje[3]
                if barva != '':
                    continue
                elif barva == '':
                    if self.stevilo_sosedov(i, j) == 0:
                        continue
                    else:
                        poteze.append(id)
        return poteze

    def stevilo_sosedov(self, i, j):
        st_sosedov = 0
        # koordinate sosedov se razlikujejo ce se nahajamo v sodi ali v lihi vrstici
        if i % 2 == 1: #lihe
          okolica = [(i-1, j-1), (i, j-1), (i+1, j-1), (i+1, j), (i, j+1), (i-1, j)]
        else: #sode
          okolica = [(i-1, j), (i, j-1), (i+1, j), (i+1, j+1), (i, j+1), (i-1, j+1)]
        for sosed in okolica:
            x, y = sosed
            sosed_podatki = safe_list_get(self.igralno_polje, x, y)
            if sosed_podatki != None:
                if sosed_podatki[3] != '':
                    st_sosedov += 1
        return st_sosedov
      




