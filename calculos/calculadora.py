import emoji
from calculos.calculotrz import transluz
from calculos.calculohpl import motohelp
from calculos.calculohr import hrtransporte
from calculos.calculoribcar import ribeirao
from calculos.calculonr import nrexpress



def calculos ():
    transluz()
    print ('Calculo da Transluz Feito !', emoji.emojize(":thumbs_up:"))
    motohelp()
    print ('Calculo da Moto Help Feito !',emoji.emojize(":thumbs_up:"))
    hrtransporte()
    print ('Calculo da HR Transportr Feito !',emoji.emojize(":thumbs_up:"))
    ribeirao()
    print ('Calculo da Ribeirão Feito !',emoji.emojize(":thumbs_up:"))
    nrexpress()
    print ('Calculo da NR Express Feito !',emoji.emojize(":thumbs_up:"))
    
if __name__ == "__main__":
    calculos()