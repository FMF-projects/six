def safe_list_get(matrika, i, j):
  try:
    return matrika[i][j]
  except IndexError:
    return None

class Igra():
    #TODO
    STRANICA_SESTKOTNIKA = 20
    VELIKOST_MATRIKE = 20

    def __init__(self):

        # SEZNAM ŠESTKOTNIKOV
        self.igralno_polje = [[0 for i in range(Igra.VELIKOST_MATRIKE)] for j in range(Igra.VELIKOST_MATRIKE)]

    def veljavne_poteze(self):
        '''vrne seznam veljavnih potez'''
        poteze = []
        for vrstica in self.igralno_polje:
            for polje in vrstica:
                id, i, j = polje[0], polje[1], polje[2]
                if self.igralno_polje.itemcget(id, "fill") != '':
                    continue
                elif self.igralno_polje.itemcget(id, "fill") == '':
                    if stevilo_sosedov(i, j) == 0:
                        continue
                    else:
                        poteze.append(polje)


    def stevilo_sosedov(self, i, j):
        st_sosedov = 0
        okolica = [(i, j-1), (i+1, j-1), (i-1, j), (i+1, j), (i, j+1), (i+1, j+1)]
        for sosed in okolica:
            x, y = sosed
            sosed_podatki = safe_list_get(self.igralno_polje, x, y)
            if sosed_podatki != None:
                if self.igralno_polje.itemcget(sosed_podatki[0], "fill") != '':
                    st_sosedov += 1
        return st_sosedov




