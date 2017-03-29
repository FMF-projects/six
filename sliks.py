import tkinter
import math

import logika_igre

class Gui():

    def __init__(self, master):
    
        # ZAČNEMO NOVO IGRO
        self.igra = logika_igre.Igra()
        
        self.STRANICA_SESTKOTNIKA = self.igra.STRANICA_SESTKOTNIKA
        self.VELIKOST_MATRIKE = self.igra.VELIKOST_MATRIKE
        # visina trikotnikov v sestkotniku
        self.VISINA_TRIKOTNIKA = 3 ** (0.5) * (0.5) * self.STRANICA_SESTKOTNIKA

        
        # PLOSCA
        self.plosca = tkinter.Canvas(master, width=self.VISINA_TRIKOTNIKA * 2 * self.VELIKOST_MATRIKE + 1
                                     , height=1.5 * self.STRANICA_SESTKOTNIKA * self.VELIKOST_MATRIKE + 0.5 * self.STRANICA_SESTKOTNIKA + 1)
        self.plosca.pack()

        self.plosca.bind("<Button-1>", self.plosca_klik)

        # GLAVNI MENU
        glavni_menu = tkinter.Menu(master)
        master.config(menu=glavni_menu)

        # PODMENUJI
        igra_menu = tkinter.Menu(glavni_menu, tearoff=0)
        glavni_menu.add_cascade(label="Igra", menu=igra_menu)

        velikost_menu = tkinter.Menu(glavni_menu, tearoff=0)
        glavni_menu.add_cascade(label="Velikost polja", menu=velikost_menu)


        # IZBIRE V PODMENUJIH
        igra_menu.add_command(label="Nova igra", command=self.nova_igra)
        velikost_menu.add_command(label="10x10", command=self.velikost_igralnega_polja(10))
        velikost_menu.add_command(label="15x15", command=self.velikost_igralnega_polja(15))
        velikost_menu.add_command(label="20x20", command=self.velikost_igralnega_polja(20))

        # UKAZI OB ZAGONU
        self.narisi_mrezo()
        #print(self.igra.igralno_polje)


    def narisi_sestkotnik(self, x, y):
        a = self.STRANICA_SESTKOTNIKA
        v = self.VISINA_TRIKOTNIKA
        t1 = (x, y + a * 0.5)
        t2 = (x + v, y)
        t3 = (x + 2 * v,y + (0.5) * a)
        t4 = (x + 2 * v, y + 1.5 * a)
        t5 = (x + v, y + 2 * a)
        t6 = (x, y + 1.5 * a)
        id = self.plosca.create_polygon(*t1, *t2, *t3, *t4, *t5, *t6, outline='black')
        return id

    def narisi_mrezo(self):
        '''nariše igralno polje sestavljeno iz šestkotnikov'''
        a = self.STRANICA_SESTKOTNIKA
        v = self.VISINA_TRIKOTNIKA
        for i in range(1, self.VELIKOST_MATRIKE + 1): # vrstica
            
            #preverimo sodost/lihost in tako določimo zamik prvega šestkotnika
            if i % 2 == 1:
                zacetni_x = 2
                for j in range(1, self.VELIKOST_MATRIKE + 1): #stolpec
                    x = zacetni_x + (j - 1) * 2 * v
                    y = (i - 1) * 1.5 * a + 2
                    self.igra.igralno_polje[i - 1][j - 1] = [self.narisi_sestkotnik(x, y), i, j]
            else:
                zacetni_x = v + 2
                for j in range(1, self.VELIKOST_MATRIKE): #stolpec
                    x = zacetni_x + (j - 1) * 2 * v
                    y = (i - 1) * 1.5 * a + 2
                    self.igra.igralno_polje[i - 1][j - 1] = [self.narisi_sestkotnik(x, y), i, j]   
    
    def nova_igra(self):
        '''počisti ploščo in nariše novo mrežo'''
        self.plosca.delete('all')
        self.narisi_mrezo()
        
    def velikost_igralnega_polja(self, matrika):
        '''spremeni velikost igralnega polja'''
        #TODO
        #okno se mora ponovno naložiti
        self.igra.VELIKOST_MATRIKE = matrika
        self.nova_igra()

    def plosca_klik(self, event):
        '''določi koordinate klika in pokliče potezo'''
        m = event.x
        n = event.y
        self.povleci_potezo(m, n)

    def povleci_potezo(self, m, n):
        #zaenkrat samo barvanje ustreznega polja
        #TODO
        id_sestkotnika = self.plosca.find_closest(m, n)[0]
        if id_sestkotnika in self.igra.veljavne_poteze():
            self.plosca.itemconfig(id_sestkotnika, fill='green')
        else:
            nothing
        #dodati je potrebno še izjemo za prvo polje

    


if __name__ == "__main__":
    root = tkinter.Tk()
    root.title("SIX")

    aplikacija = Gui(root)

    root.mainloop()
