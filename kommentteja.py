input("Tervetuloa pelaamaan! Paina enter jatkaaksesi.")
input("Tehtäväsi on valita kumpi kahdesta lentokentästä sijaitsee korkeammalla merenpinnasta")

name1="murmelli"
name2="orava"

print(f"1. {nimi1}")
        print(f"2. {nimi2}")
        while arvaus != "1" and arvaus != "2":
            arvaus = input("Valitse lentokentistä korkeammalla oleva.")
            if arvaus != "1" and arvaus != "2":
                print("Virheellinen syöte.")
            elif arvaus == oikein and arvaus == "1":
                pisteet = pisteet + 100
                print(f"Oikein! Valitsit {nimi1}, sen korkeus on {korkeus1: .2f}m")
            elif arvaus == oikein and arvaus == "2":
                pisteet = pisteet + 100
                print(f"Oikein! Valitsit {nimi2}, sen korkeus on {korkeus2: .2f}m")
            elif arvaus != oikein and arvaus == "1":
                pisteet = pisteet
                print(f"Väärin. Valitsit {nimi1}, sen korkeus on {korkeus1: .2f}m")
            elif arvaus != oikein and arvaus == "2":
                pisteet = pisteet
                print(f"Väärin. Valitsit {nimi2}, sen korkeus on {korkeus2: .2f}m")
