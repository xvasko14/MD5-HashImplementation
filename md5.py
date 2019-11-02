import math

# OTAZKA PRE UZIVATELA
#print('Zadajte slovo alebo retazec')
# zadanie hashu
#message = input()
#print(message)

#Kod
################################
#inicializacia kontextu
A = 0x67452301
B = 0xEFCDAB89
C = 0x98BADCFE
D = 0x10325476

string = "a"

#################################
#pridanie zarovanavacich bitov
#dlzka musi byt po priadni zarovnavacich bitov o 64 bit mensia ako naosobok 512 (512*2 = 1024 -64 = 960 atd...)
dlzka_stringu = len(string)
dlzka_stringu_bit = dlzka_stringu * 8


# zakodujeme do bytov
string_byte = string.encode('utf-8')

# vypocitame zarovnavacie bity ( plati + pocet zarovnaacich bitov ) Mod 512 =448
zarovavaci_bit = 56-dlzka_stringu%64
zarovavaci_bit = 64 if (zarovavaci_bit == 0) else zarovavaci_bit


# vysledny string po pridani
zarovnavaci_string = string_byte + b'\x80' + b'\x00' * (zarovavaci_bit-1)

##################################
# Pridanie Dlzky
# vyplnenie zvysnich 64 bitov vo forme 32 bitoych slov s low-order poradim bajtov
# ak nestaci  64 bitov na vstupnu spravu teda je vacsia ako 2^64, pouzivame dolnych 64 bitov na vyjadrenie a teda dlzka je presne nasobok 512

vysledny_string = zarovnavaci_string+(dlzka_stringu_bit%2**64).to_bytes(8,byteorder='little')

########################
# zoberie e 3 32bitove slova a vratime jedno 32 bitove

def F(X, Y, Z):
    return ((X&Y) | ((~X) & Z))

def G(X, Y, Z):
    return ((X&Z) | (Y & (~Z)))

def H(X, Y, Z):
    return (X^Y^Z)

def I(X, Y, Z):
    return ( Y^(X|(~Z)) )
