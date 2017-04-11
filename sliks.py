import tkinter
import math
import copy
import logging
import os

import logika_igre
import clovek
import racunalnik
import minimax

# visina trikotnikov v sestkotniku
VISINA_TRIKOTNIKA = 3 ** (0.5) * (0.5) * logika_igre.STRANICA_SESTKOTNIKA
STRANICA_SESTKOTNIKA = logika_igre.STRANICA_SESTKOTNIKA
VELIKOST_MATRIKE = logika_igre.VELIKOST_MATRIKE

IGRALEC_1 = logika_igre.IGRALEC_1
IGRALEC_2 = logika_igre.IGRALEC_2
PRAZNO = logika_igre.PRAZNO

# neumno, ampak bolj razumljivo v večini primerov
BARVA_1 = IGRALEC_1
BARVA_2 = IGRALEC_2

NI_KONEC = logika_igre.NI_KONEC
NEODLOCENO = logika_igre.NEODLOCENO

class Gui():

    def __init__(self, master):

        # ZAČNEMO NOVO IGRO
        self.igra = None
        self.igralec_1 = None # Objekt, ki igra IGRALEC_1 (nastavimo ob začetku igre)
        self.igralec_2 = None # Objekt, ki igra IGRALEC_2 (nastavimo ob začetku igre)


        # PLOSCA
        self.plosca = tkinter.Canvas(master, width=VISINA_TRIKOTNIKA * 2 * VELIKOST_MATRIKE + STRANICA_SESTKOTNIKA + 1
                                     , height=1.5 * STRANICA_SESTKOTNIKA * VELIKOST_MATRIKE + 0.5 * STRANICA_SESTKOTNIKA + 1)
        self.plosca.pack()

        self.plosca.bind("<Button-1>", self.plosca_klik)

        # Ključi so id, vrednosti koordinate.
        self.id_koord = {}
        # Obratno.
        self.koord_id = {}

        # GLAVNI MENU
        glavni_menu = tkinter.Menu(master)
        master.config(menu=glavni_menu)

        #TODO
        # izbira clovek, racunalnik

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
        #self.napolni_igralno_polje()
        #print(self.igra.igralno_polje)


###########################################################################
#               NEVARNO OBMOCJE                                           #
###########################################################################

        # Prični igro v načinu človek proti računalniku
        #self.zacni_igro(clovek.Clovek(self), racunalnik.Racunalnik(self, minimax.Minimax(minimax.globina)))
        self.zacni_igro(clovek.Clovek(self), clovek.Clovek(self))

    def zacni_igro(self, igralec_1, igralec_2):
        """Nastavi stanje igre na zacetek igre.
           Za igralca uporabi dana igralca."""
        # Ustavimo vsa vlakna, ki trenutno razmišljajo
        self.prekini_igralce()
        self.nova_igra()
        # Shranimo igralce
        self.igralec_1 = igralec_1
        self.igralec_2 = igralec_2
        # prvi na potezi je igralec 2, saj je prvo polje že pobarvano
        # z barvo igralca 1
        self.igralec_2.igraj()

    def prekini_igralce(self):
        """Sporoči igralcem, da morajo nehati razmišljati."""
        logging.debug ("prekinjam igralce")
        if self.igralec_1: self.igralec_1.racunalnik.prekini()
        if self.igralec_2: self.igralec_2.racunalnik.prekini()


###########################################################################

    def nova_igra(self):
        '''počisti ploščo in nariše novo mrežo'''
        self.igra = logika_igre.Igra()
        self.plosca.delete('all')
        self.napolni_igralno_polje()
        self.igra.na_potezi = logika_igre.IGRALEC_2

    def narisi_sestkotnik(self, x, y):
        a = STRANICA_SESTKOTNIKA
        v = VISINA_TRIKOTNIKA
        t = [x, y + a * 0.5,
             x + v, y,
             x + 2 * v,y + (0.5) * a,
             x + 2 * v, y + 1.5 * a,
             x + v, y + 2 * a,
             x, y + 1.5 * a]
        id = self.plosca.create_polygon(*t, fill=PRAZNO, outline='black')
        return id

    def napolni_igralno_polje(self):
        '''nariše igralno polje sestavljeno iz šestkotnikov'''
        a = STRANICA_SESTKOTNIKA
        v = VISINA_TRIKOTNIKA
        for i in range(VELIKOST_MATRIKE): # vrstica
            # preverimo sodost/lihost in tako določimo zamik prvega šestkotnika
            if i % 2 == 0: # lihe vrstice (ker začnemo šteti z 0)
                zacetni_x = 2
                for j in range(VELIKOST_MATRIKE): # stolpec
                    x = zacetni_x + j * 2 * v
                    y = i * 1.5 * a + 2
                    id = self.narisi_sestkotnik(x, y)
                    self.id_koord[id] = (i, j)
                    self.koord_id[(i,j)] = id
            else: # sode vrstice
                zacetni_x = v + 2
                for j in range(VELIKOST_MATRIKE): # stolpec
                    x = zacetni_x + j * 2 * v
                    y = i * 1.5 * a + 2
                    id = self.narisi_sestkotnik(x, y)
                    self.id_koord[id] = (i, j)
                    self.koord_id[(i, j)] = id

        # pobarvamo prvo polje
        i = VELIKOST_MATRIKE // 2
        j = i
        sredina = self.koord_id[(i,j)]
        self.plosca.itemconfig(sredina, fill=BARVA_1)
        self.igra.zabelezi_spremembo_barve(i, j, BARVA_1)

    def narisi_zmagovalni_vzorec(self, zmagovalna_polja):
        '''poudari zmagovalni vzorec'''
        for (i, j) in zmagovalna_polja:
            id = self.koord_id[(i, j)]
            self.plosca.itemconfig(id, width=3)

    def velikost_igralnega_polja(self, matrika):
        '''spremeni velikost igralnega polja'''
        #TODO
        #okno se mora ponovno naložiti
        #VELIKOST_MATRIKE = matrika
        #self.nova_igra()
        pass

    def plosca_klik(self, event):
        '''določi koordinate klika in pokliče potezo'''
        m = event.x
        n = event.y
        id = self.plosca.find_closest(m, n)[0]
        (i, j) = self.id_koord[id]
        self.povleci_potezo(i, j)

    def povleci_potezo(self, i, j):
        # preverimo veljavnost poteze, če je veljavna, v logika_igre spremenimo barvo,
        # potem še sliks pobarva ustrezno polje
        veljavnost = self.igra.veljavnost_poteze(i, j)
        if veljavnost == True:

            # izvedemo potezo v logiki igre
            self.igra.izvedi_potezo(i, j)

            # pobarvamo polje
            id = self.koord_id[(i, j)]
            barva = self.igra.na_potezi
            self.plosca.itemconfig(id, fill=barva)

            # preverimo, ali je igre morda ze konec
            konec_igre = self.igra.je_morda_konec(barva)
            if type(konec_igre) == list:
                self.narisi_zmagovalni_vzorec(konec_igre[1])
                self.igra.na_potezi = None
                logging.debug("konec igre")
                #TODO izpiši, da je igre konec
            else:
                # zamenjamo trenutnega igralca
                self.igra.na_potezi = logika_igre.nasprotnik(barva)
        else:
            pass


if __name__ == "__main__":
    root = tkinter.Tk()
    root.title("SIX")

    logging.basicConfig(level=logging.DEBUG)
    aplikacija = Gui(root)
    root.iconbitmap(os.path.join('ikona','matica.ico'))
    root.mainloop()
