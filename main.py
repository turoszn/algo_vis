import random
import matplotlib.pyplot as plt
import matplotlib.animation as animate


# Funkcja wyboru algorytmu
def choice():
    try:
        global x
        x = int(input("Wybierz algorytm:\n 1.Sortowanie Bąbelkowe \n 2.Sortowanie przez wstawianie"
                      " \n 3.Sortowanie Szybkie \n 4.Sortowanie przez wybieranie"
                      " \n 5.Sortowanie przez scalanie \n 6.Sortowanie stogowe \n "))
    except ValueError:
        print("Podano nieprawidłową wartość, spróbuj jeszcze raz.")
        choice()
    return x


# Wybór algorytmu
al = choice()
while al not in range(1, 7):
    print("Podano nieprawidłową wartość, lub nieistniejącą opcję. Spróbuj jeszcze raz.")
    al = choice()


# Wprowadzenie liczby elementów tablicy
def element():
    try:
        global x
        x = int(input("Wprowadź liczbę elementów wieksza niz 10:"))

    except ValueError:
        print("Podano nieprawidłową wartość, spróbuj jeszcze raz.")
        element()
    return x


# tworzenie tablicy elementów
n = element()
while n < 10:
    print("Zbyt mala ilosc elementow. Przynajmniej 10 elementów jest wymagane.")
    n = element()

array = [i + 1 for i in range(n)]
random.shuffle(array)


# Funkcja do menu wyboru. t - title a - algo, nazwy skrócone żeby nie pomieszać zmiennych później
def menu(wybrany):
    if wybrany == 1:
        t = "Sortowanie Bąbelkowe"
        a = bubble(array)
    elif wybrany == 2:
        t = "Sortowanie przez wstawianie"
        a = insert(array)
    elif wybrany == 3:
        t = "Sortowanie Szybkie"
        a = quick(array, 0, n - 1)
    elif wybrany == 4:
        t = "Sortowanie przez wybieranie"
        a = select(array)
    elif wybrany == 5:
        t = "Sortowanie przez scalanie"
        a = merge_sort(array, 0, n - 1)
    elif wybrany == 6:
        t = "Sortowanie stogowe"
        a = heap(array)
    return t, a


# mieszanie
def swap(tab, i, j):
    a = tab[j]
    tab[j] = tab[i]
    tab[i] = a


# Sortowanie babelkowe
def bubble(arr):
    if len(arr) == 1:
        return
    for i in range(len(arr) - 1):
        for j in range(len(arr) - 1 - i):
            if arr[j] > arr[j + 1]:
                swap(arr, j, j + 1)
            yield arr


# Sortowanie przez wstawianie
def insert(arr):
    if len(arr) == 1:
        return
    for i in range(1, len(arr)):
        j = i
        while j > 0 and arr[j - 1] > arr[j]:
            swap(arr, j, j - 1)
            j -= 1
            yield arr


# Sortowanie szybkie
def quick(arr, p, q):
    if p >= q:
        return
    elem = arr[q]
    index = p
    for i in range(p, q):
        if arr[i] < elem:
            swap(arr, i, index)
            index += 1
        yield arr
    swap(arr, q, index)
    yield arr

    yield from quick(arr, p, index - 1)
    yield from quick(arr, index + 1, q)


def select(arr):
    for i in range(len(arr) - 1):
        minimal = i
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[minimal]:
                minimal = j
            yield arr
        if minimal != i:
            swap(arr, i, minimal)
            yield arr


def merge_sort(arr, l, r):  # l = left r = right
    if r <= l:
        return
    elif l < r:
        mid = (l + r) // 2
        yield from merge_sort(arr, l, mid)
        yield from merge_sort(arr, mid + 1, r)
        yield from merge(arr, l, mid, r)
        yield arr


def merge(arr, lb, mid, ub):
    new = []
    i = lb
    j = mid + 1
    while i <= mid and j <= ub:
        if arr[i] < arr[j]:
            new.append(arr[i])
            i += 1
        else:
            new.append(arr[j])
            j += 1
    if i > mid:
        while j <= ub:
            new.append(arr[j])
            j += 1
    else:
        while i <= mid:
            new.append(arr[i])
            i += 1
    for i, val in enumerate(new):
        arr[lb + i] = val
        yield arr


def heapify(arr, n, i):
    largest = i
    l = i * 2 + 1
    r = i * 2 + 2
    while l < n and arr[l] > arr[largest]:
        largest = l
    while r < n and arr[r] > arr[largest]:
        largest = r
    if largest != i:
        swap(arr, i, largest)
        yield arr
        yield from heapify(arr, n, largest)


def heap(arr):
    n = len(arr)
    for i in range(n, -1, -1):
        yield from heapify(arr, n, i)
    for i in range(n - 1, 0, -1):
        swap(arr, 0, i)
        yield arr
        yield from heapify(arr, i, 0)


res = menu(al)

title = res[0]
algo = res[1]

# Initialize fig
fig, ax = plt.subplots(figsize=(15,7))
ax.set_title(title)

bar_rec = ax.bar(range(len(array)), array, align='edge')

ax.set_xlim(0, n)
ax.set_ylim(0, int(n * 1.1))

text = ax.text(0.02, 0.95, "", transform=ax.transAxes)

epochs = [0]


def update_plot(array, rec, epochs):
    for rec, val in zip(rec, array):
        rec.set_height(val)
    epochs[0] += 1


anima = animate.FuncAnimation(fig, func=update_plot, fargs=(bar_rec, epochs), frames=algo, interval=1, repeat=False)
plt.show()
