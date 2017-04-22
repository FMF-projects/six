import logika_igre

import logging

globina = 3

IGRALEC_1 = logika_igre.IGRALEC_1
IGRALEC_2 = logika_igre.IGRALEC_2
NEODLOCENO = logika_igre.NEODLOCENO
NI_KONEC = logika_igre.NI_KONEC

VELIKOST_MATRIKE = logika_igre.VELIKOST_MATRIKE

class Minimax():

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
        return stevilo_polj

    # Vrednosti igre
    ZMAGA = 100000
    NESKONCNO = 100 * ZMAGA

    def vrednost_pozicije(self):
        '''Smo v trenutnem stanju, torej sestkotniki so obarvani, kot pac so.
        Gremo po vseh poljih in za vsako polje pogledamo, koliko lahko doprinese
        k vrednosti trenutne pozicije za dolocenega igralca. Ce v nekem vzorcu nastopa
        vsaj eno polje nasprotnikove barve, to polje ne doprinese nicesar, sicer pa doloceno vrednost.'''
        vrednosti = {
            (6,0): Minimax.ZMAGA,
            (0,6): -Minimax.ZMAGA,
            (5,0) : Minimax.ZMAGA//10,
            (0,5) : -Minimax.ZMAGA//10,
            (4,0) : Minimax.ZMAGA//100,
            (0,4) : -Minimax.ZMAGA//100,
            (3,0) : Minimax.ZMAGA//1000,
            (0,3) : -Minimax.ZMAGA//1000,
            (2,0) : Minimax.ZMAGA//10000,
            (0,2) : -Minimax.ZMAGA//10000,
            (1,0) : Minimax.ZMAGA//100000,
            (0,1) : -Minimax.ZMAGA//100000
            }
        vr_pozicije = 0

        for i in range(VELIKOST_MATRIKE):
            for j in range(VELIKOST_MATRIKE):
                for vzorec in self.igra.zmagovalni_vzorci(i, j):
                    x1 = self.stevilo_polj_v_vzorcu(vzorec, self.igra.na_potezi)
                    x2 = self.stevilo_polj_v_vzorcu(vzorec, logika_igre.nasprotnik(self.igra.na_potezi))
                    # print('st polj v vzorcu:', self.stevilo_polj_v_vzorcu(vzorec, self.igra.na_potezi))
                    if (x1, x2) in vrednosti:
                        vr_pozicije += vrednosti[(x1,x2)]
                        #print('vr pozicije, (x1,x2)',vr_pozicije, (x1,x2))
        return vr_pozicije

    def izracunaj_potezo(self, igra):
        logging.debug ("minimax: racunamo potezo")
        self.igra = igra
        self.prekinitev = False # Glavno vlakno bo to nastavilo na True, če moramo nehati
        self.jaz = self.igra.na_potezi
        self.poteza = None # Sem napišemo potezo, ko jo najdemo
        # Poženemo minimax
        (poteza, vrednost) = self.minimax(self.globina, True)
        self.jaz = None
        self.igra = None
        logging.debug("minimax: poteza {0}, vrednost {1}, prekinitev {2}".format(poteza, vrednost, self.prekinitev))
        if self.prekinitev == False:
            # Potezo izvedemo v primeru, da nismo bili prekinjeni
            self.poteza = poteza

    def minimax(self, globina, maksimiziramo):
        #logging.debug("Minimax globina = {0}".format(globina))
        """Glavna metoda minimax."""
        # vrne par (poteza, vrednost), pri čemer je poteza
        # sestavljena iz koordinat polja (i,j)

        if self.prekinitev == True:
            # Sporočili so nam, da moramo prekiniti
            logging.debug ("Minimax prekinja, globina = {0}".format(globina))
            return (None, 0)

        (zmagovalec, zmagovalna_polja) = self.igra.stanje_igre()
        #print(zmagovalec, zmagovalna_polja)

        if zmagovalec in (IGRALEC_1, IGRALEC_2, NEODLOCENO):
            logging.debug("minimax: končna pozicija {0}, {1}".format(zmagovalec, zmagovalna_polja))
            # Igre je konec, vrnemo njeno vrednost
            if zmagovalec == self.jaz:
                return (None, Minimax.ZMAGA)
            elif zmagovalec == logika_igre.nasprotnik(self.jaz):
                return (None, -Minimax.ZMAGA)
            else:
                return (None, 0)

        elif zmagovalec == NI_KONEC:
            # Igre ni konec
            if globina == 0:
                return (None, self.vrednost_pozicije())
            else:
                # Naredimo eno stopnjo minimax
                if maksimiziramo:
                    # Maksimiziramo
                    najboljsa_poteza = None
                    vrednost_najboljse = -Minimax.NESKONCNO
                    vrednosti = []
                    for (i, j) in self.igra.veljavne_poteze():
                        #print(self.igra.veljavne_poteze())
                        #logging.debug("Minimax vrednost_najboljse = {0}".format(vrednost_najboljse))
                        self.igra.izvedi_potezo(i, j)
                        vrednost = self.minimax(globina-1, not maksimiziramo)[1]
                        vrednosti.append(vrednost)
                        logging.debug("Minimax vrednost = {0}, polje {1}".format(vrednost, (i,j)))
                        self.igra.razveljavi()
                        if vrednost > vrednost_najboljse:
                            vrednost_najboljse = vrednost
                            najboljsa_poteza = (i, j)
                        #print('najboljsa poteza:', najboljsa_poteza)

                            #logging.debug("Minimax najboljsa_poteza = {0}".format(najboljsa_poteza))
                else:
                    # Minimiziramo
                    najboljsa_poteza = None
                    vrednost_najboljse = Minimax.NESKONCNO
                    vrednosti = []
                    for (i, j) in self.igra.veljavne_poteze():
                        #logging.debug("Minimax vrednost_najboljse = {0}".format(vrednost_najboljse))
                        self.igra.izvedi_potezo(i, j)
                        vrednost = self.minimax(globina-1, not maksimiziramo)[1]
                        vrednosti.append(vrednost)
                        logging.debug("Minimax vrednost = {0}, polje {1}".format(vrednost, (i, j)))
                        self.igra.razveljavi()
                        if vrednost < vrednost_najboljse:
                            vrednost_najboljse = vrednost
                            najboljsa_poteza = (i, j)
                            #logging.debug("Minimax najboljsa_poteza = {0}".format(najboljsa_poteza))
                        #print('najboljsa poteza:', najboljsa_poteza)

                assert (najboljsa_poteza is not None), "minimax: izračunana poteza je None \n" + str(vrednosti)
                return (najboljsa_poteza, vrednost_najboljse)

        else:
            assert False, "minimax: nedefinirano stanje igre"
