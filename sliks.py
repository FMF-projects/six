import tkinter
import math
import logging
import os

import logika_igre
import clovek
import racunalnik
import alfabeta

###########################################################################
#               KONSTANTE                                                 #
###########################################################################

STRANICA_SESTKOTNIKA = 20
# visina trikotnikov v sestkotniku
VISINA_TRIKOTNIKA = 3 ** (0.5) * (0.5) * STRANICA_SESTKOTNIKA


PRAZNO = logika_igre.PRAZNO

NI_KONEC = logika_igre.NI_KONEC
NEODLOCENO = logika_igre.NEODLOCENO

kombinacije_barv = [('red','blue'), ('red', 'green'), ('blue','green')]

###########################################################################
#               GUI                                                       #
###########################################################################

class Gui():

    def __init__(self, master):

        # PLOSCA
        self.plosca = tkinter.Canvas(master, width=self.velikost_igralnega_polja()[0]
                                     , height=self.velikost_igralnega_polja()[1])
        self.plosca.grid(row=1, column=0)

        self.plosca.bind("<Button-1>", self.plosca_klik)

        # POLJE ZA SPOROCILA
        self.napis = tkinter.StringVar(master, value='')
        tkinter.Label(master, textvariable=self.napis).grid(row=0, column=0)
        
        # SHRANJEVANJE PODATKOV O POLJIH
        # Ključi so id, vrednosti koordinate.
        self.id_koord = {}
        # Obratno.
        self.koord_id = {}
        
        # ZAČNEMO NOVO IGRO
        self.igra = None
        self.igralec_1 = None # Objekt, ki igra IGRALEC_1 (nastavimo ob začetku igre)
        self.igralec_2 = None # Objekt, ki igra IGRALEC_2 (nastavimo ob začetku igre)

        self.zacni_igro(clovek.Clovek(self), clovek.Clovek(self))
        
        # Če uporabnik zapre okno naj se poklice self.zapri_okno
        master.protocol("WM_DELETE_WINDOW", lambda: self.zapri_okno(master))

        # GLAVNI MENU
        glavni_menu = tkinter.Menu(master)
        master.config(menu=glavni_menu)

        # PODMENUJI
        igra_menu = tkinter.Menu(glavni_menu, tearoff=0)
        glavni_menu.add_cascade(label="Igra", menu=igra_menu)

        velikost_menu = tkinter.Menu(glavni_menu, tearoff=0)
        glavni_menu.add_cascade(label="Velikost polja", menu=velikost_menu)
        
        barva_menu = tkinter.Menu(glavni_menu, tearoff=0)
        glavni_menu.add_cascade(label="Barva", menu=barva_menu)

        # IZBIRE V PODMENUJIH
        igra_menu.add_command(label="Nova igra", command=lambda: self.zacni_igro(self.igralec_1, self.igralec_2))
        igra_menu.add_command(label="Človek - Človek", command=lambda: self.nacin_igre(0))
        igra_menu.add_command(label="Človek - Računalnik", command=lambda: self.nacin_igre(1))
        igra_menu.add_command(label="Računalnik - Človek", command=lambda: self.nacin_igre(2))
        igra_menu.add_command(label="Računalnik - Računalnik", command=lambda: self.nacin_igre(3))
        
        velikost_menu.add_command(label="10x10", command=lambda: self.spremeni_velikost_igralnega_polja(10))
        velikost_menu.add_command(label="15x15", command=lambda: self.spremeni_velikost_igralnega_polja(15))
        velikost_menu.add_command(label="20x20", command=lambda: self.spremeni_velikost_igralnega_polja(20))

        barva_menu.add_command(label="rdeča-modra", command=lambda: self.barva_igralnih_polj(0))
        barva_menu.add_command(label="rdeča-zelena", command=lambda: self.barva_igralnih_polj(1))
        barva_menu.add_command(label="modra-zelena", command=lambda: self.barva_igralnih_polj(2))


    ##################################
    #             IGRA               #
    ##################################
    
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

    def nova_igra(self):
        '''počisti ploščo in nariše novo mrežo'''
        self.igra = logika_igre.Igra()
        self.napis.set('Na potezi je {0}.'.format(self.izpis_igralca(logika_igre.drugi)))
        self.plosca.delete('all')
        self.napolni_igralno_polje()
        self.igra.na_potezi = logika_igre.drugi

    def prekini_igralce(self):
        """Sporoči igralcem, da morajo nehati razmišljati."""
        logging.debug ("prekinjam igralce")
        if self.igralec_1: self.igralec_1.prekini()
        if self.igralec_2: self.igralec_2.prekini()

    def povleci_potezo(self, i, j):
        '''logiki igre naroci naj povlece potezo, 
        potem pa se ona ukvarja z veljavnostjo''' 
        barva = self.igra.na_potezi
        
        # izvedemo potezo v logiki igre
        poteza = self.igra.izvedi_potezo(i, j)

        # poteza ni bila veljavna, ne naredimo nič
        if poteza == None:
            pass
        # poteza je bila veljavna
        else:
            # pobarvamo polje
            id = self.koord_id[(i, j)]
            self.plosca.itemconfig(id, fill=barva)

            # nadaljujemo igro
            (zmagovalec, zmagovalna_polja) = poteza
            if zmagovalec == NI_KONEC:
                # poklicemo naslednjega igralca
                if self.igra.na_potezi == logika_igre.prvi:
                    self.igralec_1.igraj()
                    self.napis.set('Na potezi je {0}.'.format(self.izpis_igralca(logika_igre.prvi)))
                else:
                    self.igralec_2.igraj()
                    self.napis.set('Na potezi je {0}.'.format(self.izpis_igralca(logika_igre.drugi)))

            else:
                self.konec_igre(zmagovalec, zmagovalna_polja)
                self.prekini_igralce()
                self.igra.na_potezi = None            
        
    ###########################################
    #          OSTALE FUNKCIJE                #
    ###########################################

    def plosca_klik(self, event):
        '''določi koordinate klika in pokliče ustreznega igralca'''
        m = event.x
        n = event.y
        id = self.plosca.find_closest(m, n)[0]
        (i, j) = self.id_koord[id]
        if self.igra.na_potezi == logika_igre.prvi:
            self.igralec_1.klik(i, j)
        elif self.igra.na_potezi == logika_igre.drugi:
            self.igralec_2.klik(i, j)
        else:
            pass

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
        velikost = logika_igre.velikost_matrike
        for i in range(velikost): # vrstica
            # preverimo sodost/lihost in tako določimo zamik prvega šestkotnika
            if i % 2 == 0: # lihe vrstice (ker začnemo šteti z 0)
                zacetni_x = 2
                for j in range(velikost): # stolpec
                    x = zacetni_x + j * 2 * v
                    y = i * 1.5 * a + 2
                    id = self.narisi_sestkotnik(x, y)
                    self.id_koord[id] = (i, j)
                    self.koord_id[(i,j)] = id
            else: # sode vrstice
                zacetni_x = v + 2
                for j in range(velikost): # stolpec
                    x = zacetni_x + j * 2 * v
                    y = i * 1.5 * a + 2
                    id = self.narisi_sestkotnik(x, y)
                    self.id_koord[id] = (i, j)
                    self.koord_id[(i, j)] = id
        # pobarvamo prvo polje
        self.pobarvaj_prvo_polje()

    def pobarvaj_prvo_polje(self):
        '''pobarva prvo polje z barvo igralca 1 in spremembo zabeleži v logiko igre'''
        i = logika_igre.velikost_matrike // 2
        j = i
        barva = logika_igre.prvi
        sredina = self.koord_id[(i,j)]
        self.plosca.itemconfig(sredina, fill=barva)
        self.igra.zabelezi_spremembo_barve(i, j, barva)

    def velikost_igralnega_polja(self):
        '''izracuna velikost igralnega polja'''
        velikost_matrike = logika_igre.velikost_matrike
        sirina = VISINA_TRIKOTNIKA * 2 * velikost_matrike + STRANICA_SESTKOTNIKA + 1
        visina = 1.5 * STRANICA_SESTKOTNIKA * velikost_matrike + 0.5 * STRANICA_SESTKOTNIKA + 1
        return (sirina, visina)

    def spremeni_velikost_igralnega_polja(self, velikost):
        '''spremeni velikost igralnega polja'''
        self.prekini_igralce()
        logika_igre.velikost_matrike = velikost
        (sirina, visina) = self.velikost_igralnega_polja()
        self.plosca.config(width=sirina, height=visina)
        self.zacni_igro(self.igralec_1, self.igralec_2)
        
    def barva_igralnih_polj(self, kombinacija):
        '''spremeni barvo igralnih polj'''
        self.prekini_igralce()
        logika_igre.prvi = kombinacije_barv[kombinacija][0]
        logika_igre.drugi = kombinacije_barv[kombinacija][1]
        self.zacni_igro(self.igralec_1, self.igralec_2)

    def nacin_igre(self, nacin):
        '''nastavi igralce'''
        nacini_igre = [(clovek.Clovek(self), clovek.Clovek(self)),
                (clovek.Clovek(self), racunalnik.Racunalnik(self, alfabeta.Alfabeta(alfabeta.globina))),
                (racunalnik.Racunalnik(self, alfabeta.Alfabeta(alfabeta.globina)), clovek.Clovek(self)),
                (racunalnik.Racunalnik(self, alfabeta.Alfabeta(alfabeta.globina)), racunalnik.Racunalnik(self, alfabeta.Alfabeta(alfabeta.globina)))]
                
        (igralec_1, igralec_2) = nacini_igre[nacin]
        self.zacni_igro(igralec_1, igralec_2)

    def izpis_igralca(self, igralec):
        '''pravilno sklanja ime igralca, za izpis uporabniku'''
        if igralec == 'red':
            return 'rdeči'
        elif igralec == 'blue':
            return 'modri'
        elif igralec == 'green':
            return 'zeleni'

    def konec_igre(self, zmagovalec, zmagovalna_polja):
        '''uvede ustrezne spremembe v oknu'''
        # igre je konec, imamo zmagovalca
        if zmagovalec in [logika_igre.prvi, logika_igre.drugi]:
            self.napis.set('Zmagal je {0}.'.format(self.izpis_igralca(zmagovalec)))
            for (i, j) in zmagovalna_polja:
                id = self.koord_id[(i, j)]
                self.plosca.itemconfig(id, width=3)

        # igre je konec, rezultat je izenacen
        else:
            self.napis.set('Igra je neodločena.')
            
    def zapri_okno(self, master):
        '''Ta metoda se pokliče, ko uporabnik zapre aplikacijo.'''
        self.prekini_igralce()
        # Dejansko zapremo okno.
        master.destroy()
            
            


if __name__.endswith('__main__'):
    root = tkinter.Tk()
    root.title("SIX")
    root.resizable(width=False, height=False)
    #logging.basicConfig(level=logging.DEBUG)
    aplikacija = Gui(root)
    root.iconbitmap(os.path.join('ikona','matica.ico'))
    root.mainloop()
