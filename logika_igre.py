def safe_list_get(matrika, i, j):
  '''preveri, če je polje (i,j) v matriki (seznamu)'''
  try:
    return matrika[i][j]
  except IndexError:
    return None

class Igra():
    #TODO

    def __init__(self):
    
        # VELIKOST IGRALNEGA POLJA
        self.STRANICA_SESTKOTNIKA = 20
        self.VELIKOST_MATRIKE = 20

        # SEZNAM ŠESTKOTNIKOV
        self.igralno_polje = [[0 for i in range(self.VELIKOST_MATRIKE)] for j in range(self.VELIKOST_MATRIKE)]
   
    def veljavne_poteze(self):
        '''vrne seznam veljavnih potez'''
        poteze = []
        for vrstica in self.igralno_polje:
            for polje in vrstica:
                id, i, j = polje[0], polje[1], polje[2]
                if self.igralno_polje.itemcget(id, "fill") != '':
                  #AttributeError: 'list' object has no attribute 'itemcget'
                  #itemcget deluje na platnu hm hm....
                  #najbrz bi bilo lazje barvo vkljuciti med podatke sestkotnika
                    continue
                elif self.igralno_polje.itemcget(id, "fill") == '':
                    if stevilo_sosedov(i, j) == 0:
                        continue
                    else:
                        poteze.append(id)
                        # shranimo samo id, saj se sicer preverjanje elementov v
                        # povleci_potezo oteži
                        # ali sploh potrebujeva i, j v veljavnih potezah?
        return poteze

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




