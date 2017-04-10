import tkinter
import math
import copy
import logging

import logika_igre
import clovek
import racunalnik
import minimax

# visina trikotnikov v sestkotniku
VISINA_TRIKOTNIKA = 3 ** (0.5) * (0.5) * logika_igre.STRANICA_SESTKOTNIKA
STRANICA_SESTKOTNIKA = logika_igre.STRANICA_SESTKOTNIKA
VELIKOST_MATRIKE = logika_igre.VELIKOST_MATRIKE

BARVA1 = logika_igre.BARVA1
BARVA2 = logika_igre.BARVA2
BARVA3 = logika_igre.BARVA3

class Gui():

    def __init__(self, master):
    
        # ZAČNEMO NOVO IGRO
        self.igra = None
        self.igralec_1 = None # Objekt, ki igra BARVA1 (nastavimo ob začetku igre)
        self.igralec_2 = None # Objekt, ki igra BARVA2 (nastavimo ob začetku igre)

        
        # PLOSCA
        self.plosca = tkinter.Canvas(master, width=VISINA_TRIKOTNIKA * 2 * VELIKOST_MATRIKE + STRANICA_SESTKOTNIKA + 1
                                     , height=1.5 * STRANICA_SESTKOTNIKA * VELIKOST_MATRIKE + 0.5 * STRANICA_SESTKOTNIKA + 1)
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
        #self.narisi_mrezo()
        #print(self.igra.igralno_polje)


###########################################################################
#               NEVARNO OBMOCJE                                           #
###########################################################################

        # Prični igro v načinu človek proti računalniku
        self.zacni_igro(clovek.Clovek(self), racunalnik.Racunalnik(self, minimax.Minimax(minimax.globina)))


    def zacni_igro(self, igralec_1, igralec_2):
        """Nastavi stanje igre na zacetek igre.
           Za igralca uporabi dana igralca."""
        # Ustavimo vsa vlakna, ki trenutno razmišljajo
        self.prekini_igralce()
        self.nova_igra()
        # Shranimo igralce
        self.igralec_1 = igralec_1
        self.igralec_2 = igralec_2
        # Križec je prvi na potezi
        #self.napis.set("Na potezi je X.")
        self.igralec_2.igraj()

    # def koncaj_igro(self, zmagovalec, trojka):
    #     """Nastavi stanje igre na konec igre."""
    #     if zmagovalec == IGRALEC_X:
    #         self.napis.set("Zmagal je X.")
    #         self.narisi_zmagovalno_trojico(zmagovalec, trojka)
    #     elif zmagovalec == IGRALEC_O:
    #         self.napis.set("Zmagal je O.")
    #         self.narisi_zmagovalno_trojico(zmagovalec, trojka)
    #     else:
    #         self.napis.set("Neodločeno.")

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
        self.narisi_mrezo()
        self.igra.na_potezi = logika_igre.IGRALEC_2


    def narisi_sestkotnik(self, x, y):
        a = STRANICA_SESTKOTNIKA
        v = VISINA_TRIKOTNIKA
        t1 = (x, y + a * 0.5)
        t2 = (x + v, y)
        t3 = (x + 2 * v,y + (0.5) * a)
        t4 = (x + 2 * v, y + 1.5 * a)
        t5 = (x + v, y + 2 * a)
        t6 = (x, y + 1.5 * a)
        id = self.plosca.create_polygon(*t1, *t2, *t3, *t4, *t5, *t6, fill='', outline='black')
        return id

    def narisi_mrezo(self):
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
                    self.igra.igralno_polje[i][j] = [self.narisi_sestkotnik(x, y), i, j, '']
            else: # sode vrstice
                zacetni_x = v + 2
                for j in range(VELIKOST_MATRIKE): # stolpec
                    x = zacetni_x + j * 2 * v
                    y = i * 1.5 * a + 2
                    self.igra.igralno_polje[i][j] = [self.narisi_sestkotnik(x, y), i, j, '']

        # pobarvamo prvo polje
        sredina = self.igra.igralno_polje[VELIKOST_MATRIKE // 2][VELIKOST_MATRIKE // 2]
        self.plosca.itemconfig(sredina[0], fill=BARVA1)
        sredina[3]=BARVA1
        
        
    def narisi_zmagovalni_vzorec(self, zmagovalna_polja):
        '''poudari zmagovalni vzorec'''
        for id in zmagovalna_polja:
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
        self.povleci_potezo(m, n)
     
    def povleci_potezo(self, m, n):
        # pogledamo trenutnega igralca in izberemo ustrezno barvo
        igralec = self.igra.na_potezi

        if igralec == None:
            return None
            
        if igralec == logika_igre.IGRALEC_1:
            barva = BARVA1
        else:
            barva = BARVA2
        
        # najdemo polje, ki je najblizje kliku miske
        id_sestkotnika = self.plosca.find_closest(m, n)[0]
        
        # preverimo veljavnost poteze in jo izvedemo
        if self.igra.veljavnost_poteze(id_sestkotnika) == True:
        
            # shranimo igralno polje preden izvedemo potezo
            kopija = copy.deepcopy(self.igra.igralno_polje)
            self.igra.zgodovina.append((kopija, igralec))
            #print(self.igra.zgodovina, '================================')
            
            self.plosca.itemconfig(id_sestkotnika, fill=barva)
            
            # zabeležimo spremembo barve
            for vrstica in self.igra.igralno_polje:
                for polje in vrstica:
                    if polje[0] == id_sestkotnika:
                        polje[3] = barva

            # preverimo, ali je igre morda ze konec
            konec_igre = self.igra.je_morda_konec(barva)
            if konec_igre != logika_igre.NI_KONEC and konec_igre != logika_igre.NEODLOCENO:
                self.narisi_zmagovalni_vzorec(konec_igre[0])
                self.igra.na_potezi = None
            else:
                # zamenjamo trenutnega igralca
                self.igra.na_potezi = logika_igre.nasprotnik(igralec)

    
if __name__ == "__main__":
    root = tkinter.Tk()
    root.title("SIX")

    aplikacija = Gui(root)
    root.iconbitmap(r'..\six\ikona\matica.ico')
    root.mainloop()
