
from tkinter import *

#root = Tk()
#root.title("new App")
#root.geometry("640x640+0+0")
#heading = Label(root, text="Zadajte retazec", font=("arial",40,"bold"), fg="steelblue").pack()
#label1 = Label(root, text="Zadajte vase meno:", font=("arial",20,"bold"), fg="black").place(x=10,y=200)
#string = input()
#entry_box = Entry(root, textvariable=string, width=25, bg="lightgreen").place(x=300, y=200)
#work = Button(root,text="Work",width=30,height=5,bg="lightblue",command=vysledok).place(x=205, y=300)
#root.mainloop()


#vypisanie vysledneho hashu
print('Zadajte nejaky retazec')
#zadanie stringu
string = input()
def vysledok():
   print("MD5 hash      : " + hex(bytereverse(output_int)))


#Kod
################################
#inicializacia kontextu
A = 0x67452301
B = 0xEFCDAB89
C = 0x98BADCFE
D = 0x10325476


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
# zoberieme 3 32bitove slova a vratime jedno 32 bitove

def F(X, Y, Z):
    return ((X&Y) | ((~X) & Z))

def G(X, Y, Z):
    return ((X&Z) | (Y & (~Z)))

def H(X, Y, Z):
    return (X^Y^Z)

def I(X, Y, Z):
    return ( Y^(X|(~Z)) )

# Spravu spracuvavame po blokoch o velksoti 512 bitov, 512 bitov vyjadrime ako sestnast 32 bitovych slov a ulozime do postupnosti X[0,1...15]

# pretocime bajty s tym ze najmenej vyznamny bit bude prvy(low order poradie)
def loworder(x,s):
    return ( (x<<s) | x>>(32-s))


def bytereverse(num32):
    rev_byte = 0;
    for i in range(0, 16):
        rev_byte = rev_byte << 8
        low_order_byte = num32 & 0xFF
        rev_byte = rev_byte | low_order_byte

        num32 = num32 >> 8
    return rev_byte

# sinusova tabulka
sinusova_tabulkaT=[0xD76AA478, 0xE8C7B756, 0x242070DB, 0xC1BDCEEE, 0xF57C0FAF,
        0x4787C62A, 0xA8304613, 0xFD469501, 0x698098D8, 0x8B44F7AF,
        0xFFFF5BB1, 0x895CD7BE, 0x6B901122, 0xFD987193, 0xA679438E,
        0x49B40821, 0xF61E2562, 0xC040B340, 0x265E5A51, 0xE9B6C7AA,
        0xD62F105D, 0x02441453, 0xD8A1E681, 0xE7D3FBC8, 0x21E1CDE6,
        0xC33707D6, 0xF4D50D87, 0x455A14ED, 0xA9E3E905, 0xFCEFA3F8,
        0x676F02D9, 0x8D2A4C8A, 0xFFFA3942, 0x8771F681, 0x6d9d6122,
        0xFDE5380C, 0xA4BEEA44, 0x4BDECFA9, 0xF6BB4B60, 0xBEBFBC70,
        0x289B7EC6, 0xEAA127FA, 0xD4EF3085, 0x04881D05, 0xD9D4D039,
        0xE6DB99E5, 0x1FA27CF8, 0xC4AC5665, 0xF4292244, 0x432AFF97,
        0xAB9423A7, 0xFC93A039, 0x655B59C3, 0x8F0CCC92, 0xFFEFF47D,
        0x85845DD1, 0x6FA87E4F, 0xFE2CE6E0, 0xA3014314, 0x4E0811A1,
        0xF7537E82, 0xBD3AF235, 0x2AD7D2BB, 0xEB86D391]

# posuvacia tabulka
Posuv1=[7,12,17,22]*4
Posuv2=[5, 9,14,20]*4
Posuv3=[4,11,16,23]*4
Posuv4=[6,10,15,21]*4

# K tabulka obsahujuca 64 elementov
K_tabulka1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
K_tabulka2 = [1, 6, 11, 0, 5, 10, 15, 4, 9, 14, 3, 8, 13, 2, 7, 12]
K_tabulka3 = [5, 8, 11, 14, 1, 4, 7, 10, 13, 0, 3, 6, 9, 12, 15, 2]
K_tabulka4 = [0, 7, 14, 5, 12, 3, 10, 1, 8, 15, 6, 13, 4, 11, 2, 9]

# Funkcia pre jednotlive kola
def kolo1(a, b, c, d, X, k, sine_i, s):
    Xk = int.from_bytes(X[4*k:4*k+4],byteorder='little')
    FN = F(b,c,d)
    a = (a + FN + Xk + sine_i) & 0xFFFFFFFF
    a = ((loworder(a , s)& 0xFFFFFFFF) + b) & 0xFFFFFFFF
    vysledok_kola(1,k,s,sine_i,FN)
    return a

def kolo2(a, b, c, d, X, k, sine_i, s):
    Xk = int.from_bytes(X[4*k:4*k+4],byteorder='little')
    FN = G(b,c,d)
    a = (a + FN + Xk + sine_i) & 0xFFFFFFFF
    a = ((loworder(a , s)& 0xFFFFFFFF) + b) & 0xFFFFFFFF
    vysledok_kola(2,k,s,sine_i,FN)
    return a

def kolo3(a, b, c, d, X, k, sine_i, s):
    Xk = int.from_bytes(X[4*k:4*k+4],byteorder='little')
    FN = H(b,c,d)
    a = (a + FN + Xk + sine_i) & 0xFFFFFFFF
    a = ((loworder(a , s)& 0xFFFFFFFF) + b) & 0xFFFFFFFF
    vysledok_kola(3,k,s,sine_i,FN)
    return a

def kolo4(a, b, c, d, X, k, sine_i, s):
    Xk = int.from_bytes(X[4*k:4*k+4],byteorder='little')
    FN = I(b,c,d)
    a = (a + FN + Xk + sine_i) & 0xFFFFFFFF
    a = ((loworder(a , s)& 0xFFFFFFFF) + b) & 0xFFFFFFFF
    vysledok_kola(4,k,s,sine_i,FN)
    return a

def vysledok_kola(R,k,s,sine_i,FN):
    return None

# funkcia kde prechadzame cez rozne 512 bitove bloky nasej spravy, dokopy 64 kol
for i in range(0, len(vysledny_string), 64):
    X = vysledny_string[i:i + 64]
    AA = A
    BB = B
    CC = C
    DD = D


    A = kolo1(A, B, C, D, X, K_tabulka1[0], sinusova_tabulkaT[0], Posuv1[0])
    D = kolo1(D, A, B, C, X, K_tabulka1[1], sinusova_tabulkaT[1], Posuv1[1])
    C = kolo1(C, D, A, B, X, K_tabulka1[2], sinusova_tabulkaT[2], Posuv1[2])
    B = kolo1(B, C, D, A, X, K_tabulka1[3], sinusova_tabulkaT[3], Posuv1[3])

    A = kolo1(A, B, C, D, X, K_tabulka1[4], sinusova_tabulkaT[4], Posuv1[4])
    D = kolo1(D, A, B, C, X, K_tabulka1[5], sinusova_tabulkaT[5], Posuv1[5])
    C = kolo1(C, D, A, B, X, K_tabulka1[6], sinusova_tabulkaT[6], Posuv1[6])
    B = kolo1(B, C, D, A, X, K_tabulka1[7], sinusova_tabulkaT[7], Posuv1[7])

    A = kolo1(A, B, C, D, X, K_tabulka1[8], sinusova_tabulkaT[8], Posuv1[8])
    D = kolo1(D, A, B, C, X, K_tabulka1[9], sinusova_tabulkaT[9], Posuv1[9])
    C = kolo1(C, D, A, B, X, K_tabulka1[10], sinusova_tabulkaT[10], Posuv1[10])
    B = kolo1(B, C, D, A, X, K_tabulka1[11], sinusova_tabulkaT[11], Posuv1[11])

    A = kolo1(A, B, C, D, X, K_tabulka1[12], sinusova_tabulkaT[12], Posuv1[12])
    D = kolo1(D, A, B, C, X, K_tabulka1[13], sinusova_tabulkaT[13], Posuv1[13])
    C = kolo1(C, D, A, B, X, K_tabulka1[14], sinusova_tabulkaT[14], Posuv1[14])
    B = kolo1(B, C, D, A, X, K_tabulka1[15], sinusova_tabulkaT[15], Posuv1[15])

    #2kolo
    A = kolo2(A, B, C, D, X, K_tabulka2[0], sinusova_tabulkaT[16], Posuv2[0])
    D = kolo2(D, A, B, C, X, K_tabulka2[1], sinusova_tabulkaT[17], Posuv2[1])
    C = kolo2(C, D, A, B, X, K_tabulka2[2], sinusova_tabulkaT[18], Posuv2[2])
    B = kolo2(B, C, D, A, X, K_tabulka2[3], sinusova_tabulkaT[19], Posuv2[3])

    A = kolo2(A, B, C, D, X, K_tabulka2[4], sinusova_tabulkaT[20], Posuv2[4])
    D = kolo2(D, A, B, C, X, K_tabulka2[5], sinusova_tabulkaT[21], Posuv2[5])
    C = kolo2(C, D, A, B, X, K_tabulka2[6], sinusova_tabulkaT[22], Posuv2[6])
    B = kolo2(B, C, D, A, X, K_tabulka2[7], sinusova_tabulkaT[23], Posuv2[7])

    A = kolo2(A, B, C, D, X, K_tabulka2[8], sinusova_tabulkaT[24], Posuv2[8])
    D = kolo2(D, A, B, C, X, K_tabulka2[9], sinusova_tabulkaT[25], Posuv2[9])
    C = kolo2(C, D, A, B, X, K_tabulka2[10], sinusova_tabulkaT[26], Posuv2[10])
    B = kolo2(B, C, D, A, X, K_tabulka2[11], sinusova_tabulkaT[27], Posuv2[11])

    A = kolo2(A, B, C, D, X, K_tabulka2[12], sinusova_tabulkaT[28], Posuv2[12])
    D = kolo2(D, A, B, C, X, K_tabulka2[13], sinusova_tabulkaT[29], Posuv2[13])
    C = kolo2(C, D, A, B, X, K_tabulka2[14], sinusova_tabulkaT[30], Posuv2[14])
    B = kolo2(B, C, D, A, X, K_tabulka2[15], sinusova_tabulkaT[31], Posuv2[15])

    #3kolo
    A = kolo3(A, B, C, D, X, K_tabulka3[0], sinusova_tabulkaT[32], Posuv3[0])
    D = kolo3(D, A, B, C, X, K_tabulka3[1], sinusova_tabulkaT[33], Posuv3[1])
    C = kolo3(C, D, A, B, X, K_tabulka3[2], sinusova_tabulkaT[34], Posuv3[2])
    B = kolo3(B, C, D, A, X, K_tabulka3[3], sinusova_tabulkaT[35], Posuv3[3])

    A = kolo3(A, B, C, D, X, K_tabulka3[4], sinusova_tabulkaT[36], Posuv3[4])
    D = kolo3(D, A, B, C, X, K_tabulka3[5], sinusova_tabulkaT[37], Posuv3[5])
    C = kolo3(C, D, A, B, X, K_tabulka3[6], sinusova_tabulkaT[38], Posuv3[6])
    B = kolo3(B, C, D, A, X, K_tabulka3[7], sinusova_tabulkaT[39], Posuv3[7])

    A = kolo3(A, B, C, D, X, K_tabulka3[8], sinusova_tabulkaT[40], Posuv3[8])
    D = kolo3(D, A, B, C, X, K_tabulka3[9], sinusova_tabulkaT[41], Posuv3[9])
    C = kolo3(C, D, A, B, X, K_tabulka3[10], sinusova_tabulkaT[42], Posuv3[10])
    B = kolo3(B, C, D, A, X, K_tabulka3[11], sinusova_tabulkaT[43], Posuv3[11])

    A = kolo3(A, B, C, D, X, K_tabulka3[12], sinusova_tabulkaT[44], Posuv3[12])
    D = kolo3(D, A, B, C, X, K_tabulka3[13], sinusova_tabulkaT[45], Posuv3[13])
    C = kolo3(C, D, A, B, X, K_tabulka3[14], sinusova_tabulkaT[46], Posuv3[14])
    B = kolo3(B, C, D, A, X, K_tabulka3[15], sinusova_tabulkaT[47], Posuv3[15])

    #4kolo
    A = kolo4(A, B, C, D, X, K_tabulka4[0], sinusova_tabulkaT[48], Posuv4[0])
    D = kolo4(D, A, B, C, X, K_tabulka4[1], sinusova_tabulkaT[49], Posuv4[1])
    C = kolo4(C, D, A, B, X, K_tabulka4[2], sinusova_tabulkaT[50], Posuv4[2])
    B = kolo4(B, C, D, A, X, K_tabulka4[3], sinusova_tabulkaT[51], Posuv4[3])

    A = kolo4(A, B, C, D, X, K_tabulka4[4], sinusova_tabulkaT[52], Posuv4[4])
    D = kolo4(D, A, B, C, X, K_tabulka4[5], sinusova_tabulkaT[53], Posuv4[5])
    C = kolo4(C, D, A, B, X, K_tabulka4[6], sinusova_tabulkaT[54], Posuv4[6])
    B = kolo4(B, C, D, A, X, K_tabulka4[7], sinusova_tabulkaT[55], Posuv4[7])

    A = kolo4(A, B, C, D, X, K_tabulka4[8], sinusova_tabulkaT[56], Posuv4[8])
    D = kolo4(D, A, B, C, X, K_tabulka4[9], sinusova_tabulkaT[57], Posuv4[9])
    C = kolo4(C, D, A, B, X, K_tabulka4[10], sinusova_tabulkaT[58], Posuv4[10])
    B = kolo4(B, C, D, A, X, K_tabulka4[11], sinusova_tabulkaT[59], Posuv4[11])

    A = kolo4(A, B, C, D, X, K_tabulka4[12], sinusova_tabulkaT[60], Posuv4[12])
    D = kolo4(D, A, B, C, X, K_tabulka4[13], sinusova_tabulkaT[61], Posuv4[13])
    C = kolo4(C, D, A, B, X, K_tabulka4[14], sinusova_tabulkaT[62], Posuv4[14])
    B = kolo4(B, C, D, A, X, K_tabulka4[15], sinusova_tabulkaT[63], Posuv4[15])

    # updratujeme MD buffer po spracovani kazdeho 512 bloku
    A = (A + AA) & 0xFFFFFFFF
    B = (B + BB) & 0xFFFFFFFF
    C = (C + CC) & 0xFFFFFFFF
    D = (D + DD) & 0xFFFFFFFF

    output_int = D << 96 | C << 64 | B << 32 | A


    #funckia s vysledkom
    vysledok()