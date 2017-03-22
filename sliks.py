import tkinter
import math

class Gui():
    STRANICA_SESTKOTNIKA = 25
    VELIKOST_MATRIKE = 14

    def __init__(self, master):

        # PLOSCA
        self.plosca = tkinter.Canvas(master, width=3 ** (0.5) * (Gui.STRANICA_SESTKOTNIKA + 0.5) * Gui.VELIKOST_MATRIKE + 2, height=1.5 * Gui.STRANICA_SESTKOTNIKA * Gui.VELIKOST_MATRIKE + 0.5 * Gui.STRANICA_SESTKOTNIKA + 1)
        self.plosca.pack()

        self.igralno_polje = [[0 for i in range(Gui.VELIKOST_MATRIKE)] for j in range(Gui.VELIKOST_MATRIKE)]

        self.narisi_mrezo()
        print(self.igralno_polje)
        

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




if __name__ == "__main__":
    root = tkinter.Tk()
    root.title("SIX")

    aplikacija = Gui(root)

    root.mainloop()
