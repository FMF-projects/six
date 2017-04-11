import logika_igre

import logging

globina = 4

IGRALEC_1 = logika_igre.IGRALEC_1
IGRALEC_2 = logika_igre.IGRALEC_2
NEODLOCENO = logika_igre.NEODLOCENO
NI_KONEC = logika_igre.NI_KONEC

BARVA1 = logika_igre.BARVA1
BARVA2 = logika_igre.BARVA2

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
        '''Vrne število pobarvanih polj v izbranem vzorcu, izbrane barve. Ce v vzorcu nastopa
        sestkotnik nasprotnikove barve, vrne 0.'''
        stevilo_polj = 1
        for polje in vzorec:
            i, j = polje
            polje_podatki = self.logika_igre.safe_list_get(self.igra.igralno_polje, i, j)
            if polje_podatki != None:
                if polje_podatki[3] == barva:
                    stevilo_polj += 1
                else:
                    return 0
        return stevilo_polj

    # Vrednosti igre
    ZMAGA = 100000
    NESKONCNO = ZMAGA + 1

    def vrednost_pozicije(self):
        '''Smo v trenutnem stanju, torej sestkotniki so obarvani, kot pac so.
        Gremo po vseh poljih in za vsako polje pogledamo, koliko lahko doprinese
        k vrednosti trenutne pozicije za dolocenega igralca. Ce v nekem vzorcu nastopa
        vsaj eno polje nasprotnikove barve, to polje ne doprinese nicesar, sicer pa doloceno vrednost.'''
        vrednosti = {
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
        for vrstica in self.igra.igralno_polje:
            for polje in vrstica:
                x1, x2 = 0, 0
                i, j, barva = polje[1], polje[2], polje[3]
                if barva == BARVA1:
                    for vzorec in self.igra.zmagovalni_vzorci(i, j):
                        x1 += self.stevilo_polj_v_vzorcu(vzorec, barva)
                elif barva == BARVA2:
                    for vzorec in self.igra.zmagovalni_vzorci(i, j):
                        x2 += self.stevilo_polj_v_vzorcu(vzorec, barva)
                if (x1, x2) in vrednosti:
                    vr_pozicije += vrednosti[(x1,x2)]
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
        if not self.prekinitev:
            # Potezo izvedemo v primeru, da nismo bili prekinjeni
            self.poteza = poteza

    def minimax(self, globina, maksimiziramo):
        """Glavna metoda minimax."""
        if self.prekinitev:
            # Sporočili so nam, da moramo prekiniti
            logging.debug ("Minimax prekinja, globina = {0}".format(globina))
            return (None, 0)
        (zmagovalec, lst) = self.igra.stanje_igre()
        if zmagovalec in (IGRALEC_1, IGRALEC_2, NEODLOCENO):
            logging.debug("minimax: končna pozicija {0}, {1}".format(zmagovalec, lst))
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
                    for p in self.igra.veljavne_poteze(): # ta funkcija ne obstaja, imava le funkcijo veljavnost poteze
                        self.igra.povleci_potezo(p)
                        vrednost = self.minimax(globina-1, not maksimiziramo)[1]
                        self.igra.razveljavi()
                        if vrednost > vrednost_najboljse:
                            vrednost_najboljse = vrednost
                            najboljsa_poteza = p
                else:
                    # Minimiziramo
                    najboljsa_poteza = None
                    vrednost_najboljse = Minimax.NESKONCNO
                    for p in self.igra.veljavne_poteze():
                        self.igra.povleci_potezo(p)
                        vrednost = self.minimax(globina-1, not maksimiziramo)[1]
                        self.igra.razveljavi()
                        if vrednost < vrednost_najboljse:
                            vrednost_najboljse = vrednost
                            najboljsa_poteza = p

                assert (najboljsa_poteza is not None), "minimax: izračunana poteza je None"
                return (najboljsa_poteza, vrednost_najboljse)
        else:
            assert False, "minimax: nedefinirano stanje igre"
