gates = 1
letras = ["0", "e", "f", "g", "h", "i", "j"]
print(letras[1])

numbers = [101, 102, 103, 104, 105, 106]

is_number = [(float(x) - 100) for x in numbers]

peso_arduino = 106

if (peso_arduino in numbers):
    print("otra vez")
else:
    print("pase joven")