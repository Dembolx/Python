##########################################################################
#                                                                        #
#                            Gra 'Wisielec'                              #
#                                                                        #
##########################################################################

# Potrzebne biblioteki

from random import *
from tkinter import *
import os
import sys
import subprocess

# OKNO gry

def inizjalizacjaOknaGry():
    root = Tk()

    root.title("Wisielec")
    root.configure(bg='#FFFFFF')
    root.geometry("1350x550")
    
    return root

# Kolejne poziomy wisielca

def wisielec():
    wisielec = [PhotoImage(file=str(zdjecie) + "_zycie.png") for zdjecie in range(0, 11)] # do zmiennej przypisujemy 10 grafik wisielca
    return wisielec

# Wszystkie ogólne zmienne

ilosc_zyc = 9
koniec = FALSE

# Alfabet

alfabet = ["A","Ą","B","C","Ć","D","E","Ę","F","G","H","I","J","K","L","Ł","M","N","Ń","O","Ó","P","Q","R","S","Ś","T","U","V","W","X","Y","Z","Ż","Ź"] # 0 - 34

# Hasła

hasla = ["Ala ma kota" , "dziewięćsetdziewięćdziesięciodziewięciotysięcznik" , "Konstantynopolitańczykowianeczka" , "Programiści" , "Python" , "Komputer" , "Dobry dzień"] # tablica przechowywująca rózne hasła

# Wybrane hasło

haslo = hasla[randint(0, len(hasla)-1)].upper() # losujemy hasło z tablicy 'hasla'
haslo_dlugosc = len(haslo) # zapisujemy długość hasła

haslo_zaszyfrowane = "" # zaszyfrowane hasło

# Do password2 w wpisujemy hasło tylko za litery podstawiamy '-' a za spacje ' '

for i in range(0, haslo_dlugosc):
    if(haslo[i] == " "):
        haslo_zaszyfrowane = haslo_zaszyfrowane + " "
    else:
        haslo_zaszyfrowane = haslo_zaszyfrowane + "-"
        
haslo_zaszyfrowane_lis = list(haslo_zaszyfrowane)
        
# Dodanie do okna dwóch label-ów zawierających ilośc żyć i etapy odgadywania hasła oraz okna z wisielcem

def Inicjalizacja_paneli(root, wisielec):
    
    # okno z zyciami
    
    zycia_okno = Label(root, width=70 ,borderwidth=7)
    zycia_okno.grid(row=0,column=0,columnspan=8,padx=20,pady=20)
    zycia_okno["text"] = "🧡" * ilosc_zyc

    # Okno z zaszyfrowanym hasłem
    
    haslo_okno = Label(root, width=70 ,borderwidth=7)
    haslo_okno.grid(row=1,column=0,columnspan=8,padx=20,pady=20)
    haslo_okno["text"] = haslo_zaszyfrowane

    # okno z wisielcem
    
    wisielec_okno = Label(root , width=700 , height=550)
    wisielec_okno.grid(row=0, column=8 ,rowspan=14, padx=2, pady=2)
    wisielec_okno["image"] = wisielec[9]
    
    Panele = [zycia_okno , haslo_okno , wisielec_okno]
    
    return Panele

# wyłączenie button-ów i zmiana koloru button-ów

def disableButton(litera, trafiona, przyciski):
    #litera = litera2 - 1
    
    if litera == 100: # jeżeli litera jest równa 100 to do zmiennej 'koniec' przypisujemy wartość 'True'
        global koniec
        koniec = True
            
    else:
        if trafiona == True : 
            przyciski[litera]["state"] = "disabled"
            przyciski[litera].configure(bg='#98FB98') # jeżeli litera znajduje się w haśle to zmieniamy kolor buttona na zielony
        else:
            przyciski[litera]["state"] = "disabled"
            przyciski[litera].configure(bg='#FA8072') # jeżeli litera nie znajduje się w haśle to zmieniamy kolor buttona na czerwony
            
# funkcja sprawdzająca czy dana litera jest w haśle i zmiana ilości żyć lub pola w zamazanym hasłem

def button_click(litera, przyciski,  Panele ,wisielec):
    
    if litera == 35: # jeżeli uzytkownik wcisnął button 'Reset' to resetujemy program
            root.destroy()
            subprocess.call([sys.executable, os.path.realpath(__file__)] + sys.argv[1:])
    
    if(koniec == False):
        
        global password2
        result_password2 = ""
        trafiona = False
        
        # Sprawdzamy czy wybrana litera znajduje się w haśle
        
        for x in range(haslo_dlugosc):
            if(alfabet[litera] == haslo[x]):
                haslo_zaszyfrowane_lis[x] = alfabet[litera] 
                result_password2 = "".join(haslo_zaszyfrowane_lis)
                Panele[1]["text"] = ""
                Panele[1]["text"] = str(result_password2)
                trafiona = True
                
        # Jeżeli liczba jest / nie ma w haśle
        
        if(przyciski[litera]['state'] != DISABLED):      
            if (trafiona == False): # jeżeli nie ma litery w haśle
                global ilosc_zyc
                
                Panele[0]["text"] = ""
                ilosc_zyc -= 1
                Panele[0]["text"] = "🧡" * ilosc_zyc
                Panele[2]["image"] = wisielec[ilosc_zyc]
                
                
            if (haslo == result_password2): # Jeżeli hasło zostało odgadnięte
                litera = 100
                disableButton(litera, trafiona, przyciski)
                Panele[1]["text"] = ""
                Panele[1]["text"] = "Gratuluje wygrales !!!"
                Panele[2]["image"] = wisielec[10]
                
            if (ilosc_zyc == 0): # jeżeli użytkownik stracił wszytskie życia
                litera = 100
                disableButton(litera, trafiona, przyciski)
                Panele[1]["text"] = ""
                Panele[1]["text"] = "Przegrales !!!"
                Panele[0]["text"] = ":("
                
            disableButton(litera, trafiona, przyciski)
        
        
# Tworzenie przycisków 

def inicjalizacjaGuzików(root, Panele, wisielec):
    przyciski = [] # tworzymy tablice do której przypiszemy 35 przycisków
    miejsce = 0

    for x in range(1,6):
        for y in range(1,8):
            przyciski.append(Button(root, text=str(alfabet[miejsce]), width=2 , height=1 ,  padx=40, pady=20))
            przyciski[miejsce].bind('<Button-1>', lambda event , p=miejsce: button_click(p, przyciski, Panele, wisielec))
            przyciski[miejsce].grid(row=2+x, column=y)
            miejsce += 1


    przyciski.append(Button(root,text="Reset" , width=45 , height=1, padx=60, pady=20, command=lambda: button_click(35, przyciski, Panele, wisielec)))
    przyciski[35].grid(row=8 , column=1, columnspan=7)
    
    return przyciski

#-------------------- Main -------------------------

if __name__ == "__main__":
    
    root = inizjalizacjaOknaGry()
    
    wisielec = wisielec()
    
    Panele = Inicjalizacja_paneli(root,wisielec)
    
    przyciski = inicjalizacjaGuzików(root , Panele,wisielec)

root.mainloop()

