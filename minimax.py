import logika_igre

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
        '''vrne število pobarvanih polj v izbranem vzorcu, izbrane barve'''
        stevilo_polj = 1
        for polje in vzorec:
            i, j = polje
            polje_podatki = self.logika_igre.safe_list_get(self.igra.igralno_polje, i, j)
            if polje_podatki != None:
                if polje_podatki[3] == barva:
                    stevilo_polj += 1
        return stevilo_polj
    
    # Vrednosti igre
    ZMAGA = 100000
    
    def vrednost_pozicije(self):
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
                        x1 += stevilo_polj_v_vzorcu(vzorec, barva)
                elif barva == BARVA2:
                    for vzorec in self.igra.zmagovalni_vzorci(i, j):
                        x2 += stevilo_polj_v_vzorcu(vzorec, barva)
                if (x1, x2) in vrednosti:
                    vr_pozicije += vrednosti[(x1,x2)]
    
    # def izracunaj_potezo(self, igra):
        # self.igra = igra
        
    
        
    