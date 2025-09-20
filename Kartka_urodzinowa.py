import datetime
print("Imię odbiorcy")
Name=input()
print("Rok urodzenia")
Year=int(input())
x = datetime.datetime.now()
z=x.year
y=z-Year
print("Spersonalizowana wiadomość")
Message=input()
print("Imię nadawcy")
Sender=input()
d=format(Name)+","+" "+"Wszystkiego najlepszego z okazji"+" "+format(y)+" "+"urodzin!"+"\n"+format(Message)+"\n"+format(Sender)
print(d)