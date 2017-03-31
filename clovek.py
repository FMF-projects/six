class Clovek():

    def __init__(self, gui):
        self.gui = gui
    
    def klik(self, poteza):
        '''povlečemo potezo, če je ta veljavna'''
        self.gui.povleci_potezo(poteza)