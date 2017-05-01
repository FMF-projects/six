import logika_igre

import logging
import random

globina = 4

IGRALEC_1 = logika_igre.IGRALEC_1
IGRALEC_2 = logika_igre.IGRALEC_2
NEODLOCENO = logika_igre.NEODLOCENO
NI_KONEC = logika_igre.NI_KONEC

# Vrednosti igre
ZMAGA = 10**9
NESKONCNO = 100 * ZMAGA

VELIKOST_MATRIKE = logika_igre.VELIKOST_MATRIKE

class Alfabeta():

    def __init__(self, globina):
        self.globina = globina  # do katere globine iščemo?
        self.prekinitev = False # ali moramo končati?
        self.igra = None # objekt, ki opisuje igro (ga dobimo kasneje)
        self.jaz = None  # katerega igralca igramo (podatek dobimo kasneje)
        self.poteza = None # sem napišemo potezo, ko jo najdemo

    def prekini(self):
        """Metoda, ki jo pokliče GUI, če je treba nehati razmišljati, ker
           je uporabnik zaprl okno ali izbral novo igro."""
        self.prekinitev = True

    def stevilo_polj_v_vzorcu(self, vzorec, barva):
        '''Vrne število polj izbrane barve v izbranem vzorcu'''
        stevilo_polj = 0
        for (i, j) in vzorec:
            if self.igra.igralno_polje[i][j] == barva:
                stevilo_polj += 1
            elif self.igra.igralno_polje[i][j] == logika_igre.nasprotnik(barva):
                return 0
        return stevilo_polj

    def vrednost_pozicije(self):
        '''Smo v trenutnem stanju, torej sestkotniki so obarvani, kot pac so.
        Gremo po vseh poljih in za vsako polje pogledamo, koliko lahko doprinese
        k vrednosti trenutne pozicije za dolocenega igralca. Ce v nekem vzorcu nastopa
        vsaj eno polje nasprotnikove barve, to polje ne doprinese nicesar, sicer pa doloceno vrednost.'''
        vrednosti = {
            (6,0) : ZMAGA,
            (0,6) : -ZMAGA,
            (5,0) : ZMAGA//2,
            (0,5) : -ZMAGA//2,
            (4,0) : ZMAGA//10,
            (0,4) : -ZMAGA//10,
            (3,0) : ZMAGA//50000,
            (0,3) : -ZMAGA//50000,
            (2,0) : ZMAGA//5000000,
            (0,2) : -ZMAGA//5000000,
            (1,0) : 1,
            (0,1) : -1,
            (0,0) : 0
            }
        vr_pozicije = 0

        for i in range(VELIKOST_MATRIKE):
            for j in range(VELIKOST_MATRIKE):
                for vzorec in self.igra.zmagovalni_vzorci(i, j):
                    x1 = self.stevilo_polj_v_vzorcu(vzorec, self.igra.na_potezi)
                    x2 = self.stevilo_polj_v_vzorcu(vzorec, logika_igre.nasprotnik(self.igra.na_potezi))
                    vr_pozicije += vrednosti[(x1,x2)]
                    #if x1+x2 > 4: print('(x1,x2):', (x1,x2),'vr pozicije, (x1,x2)',vr_pozicije, (x1,x2))
        return vr_pozicije

    def izracunaj_potezo(self, igra):
        logging.debug ("alfabeta: racunamo potezo")
        self.igra = igra
        self.prekinitev = False # Glavno vlakno bo to nastavilo na True, če moramo nehati
        self.jaz = self.igra.na_potezi
        self.poteza = None # Sem napišemo potezo, ko jo najdemo
        # Poženemo minimax
        (poteza, vrednost) = self.alfabeta(self.globina, True)
        self.jaz = None
        self.igra = None
        logging.debug("alfabeta: poteza {0}, vrednost {1}, prekinitev {2}".format(poteza, vrednost, self.prekinitev))
        if self.prekinitev == False:
            # Potezo izvedemo v primeru, da nismo bili prekinjeni
            self.poteza = poteza

    def alfabeta(self, globina, maksimiziramo, alfa=-NESKONCNO, beta=NESKONCNO):

        if self.prekinitev == True:
            # Sporočili so nam, da moramo prekiniti
            return (None, 0)

        (zmagovalec, zmagovalna_polja) = self.igra.stanje_igre()

        if zmagovalec in (IGRALEC_1, IGRALEC_2, NEODLOCENO):
            # Igre je konec, vrnemo njeno vrednost
            if zmagovalec == self.jaz:
                return (None, ZMAGA)
            elif zmagovalec == logika_igre.nasprotnik(self.jaz):
                return (None, -ZMAGA)
            else:
                return (None, 0)

        elif zmagovalec == NI_KONEC:
            # Igre ni konec
            if globina == 0:
                return (None, self.vrednost_pozicije())
            if maksimiziramo:
                vrednost = -NESKONCNO
                poteza = None
                for (i,j) in self.igra.veljavne_poteze():
                    self.igra.izvedi_potezo(i, j)
                    pomozna_vr = self.alfabeta(globina-1, not maksimiziramo, alfa, beta)[1]
                    self.igra.razveljavi()

                    if pomozna_vr > vrednost:
                        vrednost = pomozna_vr
                        poteza = (i, j)

                    alfa = max(alfa, vrednost)
                    if beta < alfa:
                        break
                assert (poteza is not None), "minimax: izračunana poteza je None"
                return (poteza, vrednost)
            else:
                vrednost = NESKONCNO
                for (i,j) in self.igra.veljavne_poteze():
                    self.igra.izvedi_potezo(i, j)
                    pomozna_vr = self.alfabeta(globina-1, not maksimiziramo, alfa, beta)[1]
                    self.igra.razveljavi()

                    if pomozna_vr < vrednost:
                        vrednost = pomozna_vr
                        poteza = (i, j)

                    beta = max(beta, vrednost)
                    if beta < alfa:
                        break
                assert (poteza is not None), "minimax: izračunana poteza je None"
                return (poteza, vrednost)

        else:
            assert False, "minimax: nedefinirano stanje igre"

