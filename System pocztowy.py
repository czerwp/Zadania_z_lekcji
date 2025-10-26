weight_count = 0
packages_list=[]
package=[]
product_count = int(input("Ile produktów chcesz wysłać?"))

for product in range (product_count):
    weight = float(input("Jaka jest waga produktu?"))
    if weight < 1 or weight > 10:
        print("Waga spoza zakresu (1-10kg).")
        break
    if weight_count + weight <=20:
        package.append(weight)
        weight_count += weight
    else:
        packages_list.append(package)
        package= [weight]
        weight_count= weight
if package:
    packages_list.append(package)

total_packages=len(packages_list)
total_weight=sum(sum(x) for x in packages_list)
empty=total_packages*20 - total_weight
empty_package=[20 - sum(x) for x in packages_list]
max_empty = max(empty_package)
max_empty_index=empty_package.index(max_empty)+1


print(f'Liczba wysłanych paczek: {total_packages} {packages_list}, Waga wysłanych produktów: {total_weight}, Suma pustych kilogramów: {empty}, Najwięcej pustych kg ma paczka: {max_empty_index}, kg: {max_empty}')
