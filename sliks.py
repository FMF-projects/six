import tkinter
import math

class Gui():
    STRANICA_SESTKOTNIKA = 23
    VELIKOST_MATRIKE = 13

    def __init__(self, master):

        # PLOSCA
        self.plosca = tkinter.Canvas(master, width=3 ** (0.5) * (Gui.STRANICA_SESTKOTNIKA) * Gui.VELIKOST_MATRIKE + 1
                                     , height=1.5 * Gui.STRANICA_SESTKOTNIKA * Gui.VELIKOST_MATRIKE + 0.5 * Gui.STRANICA_SESTKOTNIKA + 1)

        self.plosca.pack()

        self.igralno_polje = [[0 for i in range(Gui.VELIKOST_MATRIKE)] for j in range(Gui.VELIKOST_MATRIKE)]

        self.plosca.bind("<Button-1>", self.plosca_klik)

        # GLAVNI MENU
        glavni_menu = tkinter.Menu(master)
        master.config(menu=glavni_menu)

        # PODMENUJI
        igra_menu = tkinter.Menu(glavni_menu, tearoff=0)
        glavni_menu.add_cascade(label="Igra", menu=igra_menu)

        nastavitve_menu = tkinter.Menu(glavni_menu, tearoff=0)
        glavni_menu.add_cascade(label="Nastavitve", menu=nastavitve_menu)

        # IZBIRE V PODMENUJIH
        igra_menu.add_command(label="Nova igra", command=self.nova_igra)


        self.narisi_mrezo()
        #print(self.igralno_polje)


    def nova_igra(self):
        self.plosca.delete('all')
        self.narisi_mrezo()

    def narisi_sestkotnik(self, x, y):
        a = Gui.STRANICA_SESTKOTNIKA
        # visina trikotnikov v sestkotniku
        v = 3 ** (0.5) * (0.5) * a
        t1 = (x, y + a * 0.5)
        t2 = (x + v, y)
        t3 = (x + 2 * v,y + (0.5) * a)
        t4 = (x + 2 * v, y + 1.5 * a)
        t5 = (x + v, y + 2 * a)
        t6 = (x, y + 1.5 * a)
        id = self.plosca.create_polygon(*t1, *t2, *t3, *t4, *t5, *t6, fill='', outline='black')
        return id

    def narisi_mrezo(self):
        a = Gui.STRANICA_SESTKOTNIKA
        v = 3 ** (0.5) * (0.5) * a
        for i in range(1, Gui.VELIKOST_MATRIKE + 1): # vrstica
            if i % 2 == 1:
                zacetni_x = 2
            else:
                zacetni_x = v + 2

            for j in range(1, Gui.VELIKOST_MATRIKE + 1): #stolpec
                x = zacetni_x + (j - 1) * 2 * v
                y = (i - 1) * 1.5 * a + 2
                self.igralno_polje[i - 1][j - 1] = self.narisi_sestkotnik(x, y)

    def plosca_klik(self, event):
        m = event.x
        n = event.y
        self.povleci_potezo(m, n)

    def povleci_potezo(self, m, n):
        #zaenkrat samo barvanje ustreznega polja
        #TODO
        id_sestkotnika = self.plosca.find_closest(m, n)[0]
        self.plosca.itemconfig(id_sestkotnika, fill='red')








if __name__ == "__main__":
    root = tkinter.Tk()
    root.title("SIX")

    aplikacija = Gui(root)

    root.mainloop()
