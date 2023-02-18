import streamlit as st
import datetime
#from babel.dates import format_date
import pandas as pd
#import matplotlib.pyplot as plt
import csv

#st.set_page_config(
#    page_title="Kalkulator wynagrodzenia strażaka PSP", # Nazwa strony
#    page_icon="🚒", #https://emojipedia.org/fire-engine/
#)
#st.sidebar.success("Wybierz stronę ponieżej:")

st.markdown("# Symulator wynagrodzenia strażaka PSP")
st.markdown("Aplikacja symulująca wyliczenie uposażenia strażaka, funkcjonariusza Państwowej Straży Pożarnej to narzędzie, które umożliwia użytkownikowi łatwe i szybkie obliczenie wynagrodzenia na podstawie określonych kryteriów, takich jak staż pracy, stopień awansu, rodzaj wykonywanej pracy oraz dodatki i premie. Aplikacja ta może być przydatna dla strażaków oraz ich przełożonych, którzy chcą poznać orientacyjną wysokość wynagrodzenia, jakie może otrzymać pracownik. Dzięki temu narzędziu można w prosty sposób przewidywać wysokość pensji oraz skutki zmiany poszczególnych parametrów, takich jak dodatkowe uprawnienia czy wynagrodzenie za nadgodziny.")

#----------------
#data przyjscia do sluzby
st.markdown("### 1. Podstawowe dane")
data_rozpoczecia_sluzby = st.date_input("Wprowadź datę rozpoczęcia służby:",  min_value=datetime.date(1900, 1, 1), help='Wybierz datę rozpoczęcia słuby wpisując dane rozpoczynając od roku, miesiąca i dni.') #st.date_input("Wprowadź datę rozpoczęcia szłuzby:", min_value=datetime.date(1900, 1, 1))
today = datetime.datetime.now().date()
Data_rozpoczecia_sluzby_today = today - data_rozpoczecia_sluzby #liczba lat w służbie zmienna do wzięcia do obliczeń
locale = "pl_PL"
liczba_lat_w_sluzbie_cyfra = int(Data_rozpoczecia_sluzby_today.days // 365) #liczba lat słuby

#----------------
#wybór dodatku słubowego / funkcyjnego

dodatek = st.selectbox("Wybierz dodatek:", options=["Brak", "Dodatek służbowy", "Dodatek funkcyjny"], index=0, help='Wybierz rodzaj dodatku, który posiadasz.')


if dodatek == "Dodatek służbowy":
    dodatek_sluzbowy = st.number_input("Podaj wartość dodatku służbowego:", value=0.0, format="%.2f", help='Wprowadź wartość dodatku służbowego.')
    dodatek_funkcyjny = 0.0
elif dodatek == "Dodatek funkcyjny":
    dodatek_funkcyjny = st.number_input("Podaj wartość dodatku funkcyjnego:", value=0.0, format="%.2f", help='Wprowadź wartość dodatku funkcyjnego.')
    dodatek_sluzbowy = 0.0
else:
    dodatek_sluzbowy = 0.0
    dodatek_funkcyjny = 0.0
    st.write("Brak dodatku")

#st.write("Dodatek służbowy:", dodatek_sluzbowy)
#st.write("Dodatek funkcyjny:", dodatek_funkcyjny)

#----------------
#dodatek motywacyjny

czy_dodac_dodatek_motywacyjny = st.radio("Czy dodać dodatek motywacyjny?", options=["Tak", "Nie"],index=1, help='Wpisz obecnie otrzymywany dodatej motywacyjny. Dodatek motywacyjny przyznaje się strażakowi w miesięcznej stawce kwotowej w wysokości do 30% uposażenia przewidzianego dla najniższego stanowiska służbowego w Państwowej Straży Pożarnej, które obejmuje stawkę przewidzianą dla najniższej grupy uposażenia zasadniczego i stawkę dodatku za stopień.')

if czy_dodac_dodatek_motywacyjny == "Tak":
    wartosc_dodatku_motywacyjnego = st.number_input("Podaj wartość dodatku motywacyjnego:")
else:
    wartosc_dodatku_motywacyjnego = 0.0

#----------------
#wybor dodatku stołecznego
KwotaBazowa22 = 1614.69    #kwota bazowa 2022
KwotaBazowa23 = 1740.64     #kwota bazowa 2023
czy_dodatek_stoleczny = st.radio("Czy posiadasz prawo do dodatku stołecznego?", options=["TAK", "NIE"],index=1, help='Wpisz czy posiadasz prawo do dodatku stołecznego. Dodatek stołeczny przyznaje się strażakowi w wysokości 31,5% stawki podstawowej, jeżeli strażak zamieszkuje w granicach miasta stołecznego.')
if czy_dodatek_stoleczny == "TAK":
    dodatek_stoleczny_procent = 0.315 # 31,5%
else:
    dodatek_stoleczny_procent = 0.0

#----------
#pierwsza baza danych dot. grupa
grupa_up_tablica = {
    "Nr_grupy": [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20],
    "Kwota_gr_2022": [2550, 2820, 2930, 3030, 3060, 3080, 3110, 3150, 3170, 3260, 3350, 3460, 3550, 3730, 4050, 4540, 5150, 5790, 7910, 9020],
    "Kwota_gr_2023": [2800.00, 3070.00, 3180.00, 3280.00, 3370.00, 3460.00, 3550.00, 3640.00, 3730.00, 3820.00, 3910.00, 4000.00, 4090.00, 4180.00, 4370.00, 4890.00, 5560.00, 6240.00, 8520.00, 9730.00],
    "Kwota_gr_2024": [2810.00, 3080.00, 3180.00, 3280.00, 3380.00, 3480.00, 3580.00, 3680.00, 3780.00, 3880.00, 3980.00, 4080.00, 4180.00, 4280.00, 4560.00, 5100.00, 5750.00, 6420.00, 8700.00, 9900.00],
    "Mnoznik_w_grupie":[1.577, 1.749, 1.813, 1.876, 1.896, 1.906, 1.926, 1.950, 1.961, 2.020, 2.074, 2.144, 2.198, 2.311, 2.509, 2.811, 3.192, 3.587, 4.897, 5.588]
    }
#druga baza danych stopnie_tablica
stopnie_tablica = {
    "stopien":["str.", "st.str.", "sekc.", "st.sekc.", "mł.ogn.", "ogn.", "st.ogn.", "mł.asp.", "asp.", "st.asp.", "asp.sztab.", "mł.kpt.", "kpt.", "st.kpt.", "mł.bryg.", "bryg.", "st.bryg.", "nadbryg.", "gen.brygadier"],
    "stopien_wartosc":[1622, 1632, 1672, 1692, 1712, 1732, 1752, 1807, 1827, 1847, 1867, 1922, 1942, 1962, 1982, 2002, 2022, 2172, 2322]
    }
#Wysługa
wysluga_tablica = {
    "lata":[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35],
    "lata_procent":[0, 0, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.18, 0.19, 0.2, 0.2, 0.22, 0.22, 0.24, 0.24, 0.26, 0.26, 0.28, 0.28, 0.3, 0.3, 0.32, 0.32, 0.32, 0.35]      
    }

#tablica_15_lat
dodatek_15_lat_tablica = {
    "lata15":    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35],
    "dodatek_procent15": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0.05, 0.06, 0.07, 0.08, 0.09, 0.10, 0.11, 0.12, 0.13, 0.14, 0.15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    }
# Tablice przygotowane i sformatowane w kolumnach
df_grupa_uposazenia_tablica = pd.DataFrame(grupa_up_tablica)
df_stopnie_tablica = pd.DataFrame(stopnie_tablica)
df_wysluga_tablica = pd.DataFrame(wysluga_tablica)
df_dodatek_15_lat_tablica = pd.DataFrame(dodatek_15_lat_tablica)

# stwórz rozwijaną listę z numerami grup - obsluga
selected_group = st.selectbox("Grupa uposażenia zasadniczego", df_grupa_uposazenia_tablica["Nr_grupy"],help="Wybierz numer grupy uposażenia zasadniczego na podstawie rozporządzenia MSWiA w sprawie uposażenia strażaków Państwowej Straży Pożarnej")
selected_group2 = st.selectbox("Wybierz obecnie posiadany stopień", df_stopnie_tablica["stopien"], help="Wybierz obecnie posiadany stopień")

# wybierz wiersz dla wybranej grupy i wybierz wartość dla kolumny "Kwota w grupie"
grupa_uposazenia_zasadniczego_2022 = df_grupa_uposazenia_tablica.loc[df_grupa_uposazenia_tablica["Nr_grupy"] == selected_group, "Kwota_gr_2022"].iloc[0]
grupa_uposazenia_zasadniczego_2023 = df_grupa_uposazenia_tablica.loc[df_grupa_uposazenia_tablica["Nr_grupy"] == selected_group, "Kwota_gr_2023"].iloc[0]
grupa_uposazenia_zasadniczego_2024 = df_grupa_uposazenia_tablica.loc[df_grupa_uposazenia_tablica["Nr_grupy"] == selected_group, "Kwota_gr_2024"].iloc[0]
Mnoznik_w_grupie= df_grupa_uposazenia_tablica.loc[df_grupa_uposazenia_tablica["Nr_grupy"] == selected_group, "Mnoznik_w_grupie"].iloc[0]
stopien_wartosc=df_stopnie_tablica.loc[df_stopnie_tablica["stopien"] == selected_group2, "stopien_wartosc"].iloc[0]

procent_lat_wysluga = wysluga_tablica["lata_procent"][liczba_lat_w_sluzbie_cyfra]
procent_lat15_wysluga = dodatek_15_lat_tablica["dodatek_procent15"][liczba_lat_w_sluzbie_cyfra]

#Inne zmienne, pomocnicze
dodatek_stoleczny = KwotaBazowa23 * dodatek_stoleczny_procent

#Dodatek dziadkowy
if liczba_lat_w_sluzbie_cyfra <= 25:
    DDZIADKOWY = 0
elif liczba_lat_w_sluzbie_cyfra >= 26 and liczba_lat_w_sluzbie_cyfra < 28.5:
    DDZIADKOWY = 1500
else:
    DDZIADKOWY = 2500


#zminne podstawowe do obliczenia wynagrodzenia
DSP = dodatek_stoleczny_procent #stały dodatek stłoeczny w wysokości 31,5% z kwoty uposażenia zasadniczego
KDS = dodatek_stoleczny #kwota dodatku stłoecznego
GUZ22 = grupa_uposazenia_zasadniczego_2022 #Grupa uposażenia zasadniczego zł
GUZ23 = grupa_uposazenia_zasadniczego_2023 #Grupa uposażenia zasadniczego zł
GUZ24 = grupa_uposazenia_zasadniczego_2024 #Grupa uposażenia zasadniczego zł
DSPZL = GUZ22 * DSP #dodatek stłoeczny w kwocie
WL = liczba_lat_w_sluzbie_cyfra #Wysługa lat
WUZLAT22 = procent_lat_wysluga * GUZ22 #wysługa lat w kwocie "Wzrost uposażenia zasadniczego z tytułu wysługi lat %"
WUZLAT23 = procent_lat_wysluga * GUZ23 #wysługa lat w kwocie "Wzrost uposażenia zasadniczego z tytułu wysługi lat %"    
WUZLAT24 = procent_lat_wysluga * GUZ24 #wysługa lat w kwocie "Wzrost uposażenia zasadniczego z tytułu wysługi lat %"
ROZNICA24_23 = GUZ24 - GUZ23 #Różnica między kwotą uposażenia zasadniczego w 2024 a 2023 
DS = stopien_wartosc #Dodatek za stopień
DSL = dodatek_sluzbowy #Posiadany dodatek służbowy
DFU = dodatek_funkcyjny #Posiadany dodatek funkcyjny
PDS = dodatek_sluzbowy+dodatek_funkcyjny #Dodatek słubowy razem
DM = wartosc_dodatku_motywacyjnego #dodatek motywacyjny
plus15 = round((GUZ22+WUZLAT22)*procent_lat15_wysluga, 2) #dodatek za 15 lat w służbie w kwocie

#Podwyższenie dodatku służbowego do 8% + od planowanego na 2024 wzrostu w grupie / #Podwyższenie dodatku służbowego do 8% (od 1.03. do 31.12.2023r)
#J10/(J4+J6+J8)

#zmienne pomocnicze: 
#a = sprawdzenie czy dodatek służbowy jest mniejszy od 8% z kwoty uposażenia zasadniczego
#b = kwota podwyższenia dodatku służbowego do 8% z kwoty uposażenia zasadniczego

a=PDS/(GUZ23+(GUZ23*procent_lat_wysluga)+DS) #J10/(J4+J6+J8) arkusza kalkulacyjnego
#st.write("a=", a)
#st.header("____IF____Podwyższenie dodatku służbowego do 8%")
if a >= 0 and a <= 0.08:
    b=((((GUZ23+(GUZ23*procent_lat_wysluga)+DS)*0.08)-PDS)) #J4+J6+J8)*0,08-J10 z arkusza kalkulacyjnego
    #st.write("B sprawdzone dodatek:",b)
else:
    b=0
    #st.write("B=0 nie spełnił warunku",b)
#(J4+J6+J8)*0,08-J10 
#st.write("b=(((",GUZ23,"+(",GUZ23,"*",procent_lat_wysluga,")+",DS,")*",0.08,")-",PDS,")")
#b=(((GUZ23+(GUZ23*procent_lat_wysluga)+DS)*0.08)-PDS) #J12 - "Podwyższenie dodatku służbowego(od 1.03. do 31.12.2023r)"
#st.write("b=", b)
#J12 - "Podwyższenie dodatku służbowego(od 1.03. do 31.12.2023r)"
c=ROZNICA24_23*procent_lat_wysluga+ROZNICA24_23 #J13 - "Podwyższenie dodatku służbowego(od 1.01. do 28.02.2024r)"
#st.write("c=ROZNICA24_23*procent_lat_wysluga+ROZNICA24_23")
#st.write("c=",ROZNICA24_23,"*","(",procent_lat_wysluga,"+",ROZNICA24_23,")=",c)


#uposażenie
uposazenie22 = round(GUZ22+WUZLAT22+DS+PDS+DM+KDS+DDZIADKOWY,2) 

#Wydrukuj wynagrodzenie
st.write("-------------------")
st.markdown("### 2. Symulacja wynagrodzenia")
st.markdown("2.1. Wynagrodzenie przeliczone na zasadach obowiązujących do 28 lutego 2023 roku:")
st.markdown(f"Twoje uposażenie składa się grupy uposazenia zasadniczego: tj: tzw. grupy: :red[{selected_group}] której odpowiada kwota :red[{GUZ22:.2f} zł]. Kolejym składnikiem jest tzw. wzrost uposażenia zasadniczego z tytułu wysługi lat w %. W twoim przypadku liczba przepracowanych lat to :red[{WL}] odpowiadający współczynnik to :red[{procent_lat_wysluga*100} %]. <br>Kolejnym elementem jest posiadany stopień. W twoim wypadku to :red[{selected_group2}] dla którego dodatek równa się :red[{DS:.2f} zł]. <brr> Twój dodatek słuzbowy lub funkcyjny jest w wysokości :red[{PDS:.2f} zł]. Doliczony równiez jest dodatek motywacyjny w wysokości :red[{DM:.2f} zł] oraz dodatek 25+ w wysokości :red[{DDZIADKOWY:.2f} zł].", unsafe_allow_html=True)
st.markdown(f"<b>Twoje wynagrodzenie wynosi: :red[{uposazenie22:.2f} zł brutto].</b>", unsafe_allow_html=True)

#-----------

# Dane do wyświetlenia
dane = [
    ['Grupa w zł:'                  , f"{GUZ22:.2f} zł"                                 , f"{GUZ23:.2f} zł"                                 , f"{GUZ23-GUZ22:.2f} zł"],
    ['% wysługi w zł:'              , f"{WUZLAT22:.2f} zł"                              , f"{WUZLAT23:.2f} zł"                              , f"{WUZLAT23-WUZLAT22:.2f} zł"],
    ['Posiadany stopień:'           , f"{DS:.2f} zł"                                    , f"{DS:.2f} zł"                                    , f"{DS-DS:.2f} zł"],
    ['Dodatek słuzbowy / funkcyjny:', f"{PDS:.2f} zł"                                   , f"{PDS+b+c:.2f} zł"                               , f"{PDS+b+c-PDS:.2f} zł"],
    ['Dodatek motywacyjny:'         , f"{DM:.2f} zł"                                    , f"{DM:.2f} zł"                                    , f"{DM-DM:.2f} zł"],
    ['Dodatek 15+:'                 , f" --- "                                          , f"{plus15:.2f} zł"                                , f"{plus15:.2f} zł"],
    ['Dodatek 25+:'                 , f" {DDZIADKOWY:.2f} "                             , f"{DDZIADKOWY:.2f} zł"                            , f"{DDZIADKOWY-DDZIADKOWY:.2f} zł"],
    ['Dodatek stołeczny'            , f" --- "                                          , f"{KDS:.2f} zł"                                   , f"{KDS:.2f} zł"],
    ['Razem brutto w zł:'           , f"{GUZ22+DS+PDS+DM+DDZIADKOWY+WUZLAT22:.2f} zł"   , f"{GUZ23+DS+PDS+DM+DDZIADKOWY+plus15+WUZLAT23+KDS:.2f} zł"   , f"{(GUZ23+DS+PDS+DM+DDZIADKOWY+plus15+WUZLAT23+KDS)-(GUZ22+DS+PDS+DM+DDZIADKOWY+WUZLAT22):.2f} zł"],
]   

# Utworzenie ramki danych
df = pd.DataFrame(dane, columns=["Nazwa składnika", "2022", "2023", "Różnica"])

# Wyświetlenie ramki danych w aplikacji Streamlit
st.table(df)

# Przygotowanie danych
dane = {
    "2022": GUZ22+DS+PDS+DM+DDZIADKOWY+WUZLAT22,
    "2023": GUZ23+DS+PDS+DM+DDZIADKOWY+plus15+WUZLAT23+KDS
}

# Wyświetlanie wykresu słupkowego
st.bar_chart(dane, width=300, height=400, use_container_width=False,)

#------------------
a1 = today
b1 = f"{GUZ23:.2f} zł"
c1 = f"{WUZLAT23:.2f} zł"
d1 = f"{DS:.2f} zł" 
e1 = f"{PDS+b+c:.2f} zł"
f1 = f"{DM:.2f} zł"
g1 = f"{plus15:.2f} zł"
h1 = f"{DDZIADKOWY:.2f} zł"
i1 = f"{KDS:.2f} zł"
j1 = f"{GUZ23+DS+PDS+DM+DDZIADKOWY+plus15+WUZLAT23+KDS:.2f} zł"


def save_to_csv(a1, b1, c1, d1, e1, f1, g1, h1, i1, j1):
    with open('dane.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([a1, b1, c1, d1, e1, f1, g1, h1, i1, j1])



#st.write("Wartości zmiennych:")
#st.write(f"a = {a1}")
#st.write(f"b = {b1}")
#st.write(f"c = {c1}")
#st.write(f"d = {d1}")
#st.write(f"e = {e1}")
#st.write(f"f = {f1}")
#st.write(f"g = {g1}")
#st.write(f"h = {h1}")
#st.write(f"i = {i1}")
#st.write(f"j = {j1}")

if st.button("Zapisz swoją kalkulację do analizy"):
    save_to_csv(a1, b1, c1, d1, e1, f1, g1, h1, i1, j1)
    st.write("Zapisano dane do pliku dane.csv.")
