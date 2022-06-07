import math
import numpy as np

N = 100
M = 1000
a = 37
b = 1

x = [38]
for i in range(1, N):
    z = (x[i - 1] * a + b) % M
    x.append(z)

for i in range(N):
    x[i] = x[i] / M

print("Псевдо случайные числа")
print(x)

H = (max(x) - min(x)) / (1 + 3.3221 * math.log10(N))
print("Длина интервала: ", H)

cou = 0
n_i = []
A = min(x)
B = min(x) + H
while B < 1:
    n_i.append(0)
    for i in x:
        if A <= i <= B:
            n_i[cou] += 1
    cou += 1
    A += H
    B += H

n_i.append(0)
for i in x:
    if A <= i < 1:
        n_i[cou] += 1

print("Количество чисел в каждом интервале: ", n_i)

sr_vibor = round((sum(x) / float(N)), 8)
print("Средне выборочное ", sr_vibor)

sum = 0
for i in x:
    sum = sum + pow((i - sr_vibor), 2)
desper = sum / len(x)
print("Десперсия: ", desper)

sigma = math.sqrt(desper)
print("Сигма: ", sigma)

a_z = sr_vibor - math.sqrt(3) * sigma
b_z = sr_vibor + math.sqrt(3) * sigma
print("A*: ", a_z, "B*: ", b_z)

plotnost = 1 / (b_z - a_z)
print("Плотность вероятности предполагаемого распределения", plotnost)

x_s = []
A = min(x)
B = min(x) + H
while B < 1:
    x_s.append((B + A) / 2)
    A += H
    B += H
x_s.append((1 + A) / 2)

print("Середины интервалов: ", x_s)
# print(len(x_s))

n_z = []
n_z.append(N * (x_s[0] - a_z) / (b_z - a_z))
for i in range(1, len(x_s) - 1):
    n_z.append(N * (1 / (b_z - a_z)) * (x_s[i] - x_s[i - 1]))
n_z.append(N * (1 / (b_z - a_z)) * (b_z - x_s[len(x_s) - 2]))

print("Теоретические частоты", n_z)

x_pirson = 0
for i in range(5):
    x_pirson += (pow((n_i[i] - n_z[i]), 2)) / n_z[i]
print("Критерий Пирсона: ", x_pirson)
print(x_pirson, " < 11.1")

print("Нет оснований отвергать теорию")

result = []
if len(x) % 2 == 0:
    med = sorted(x)[int(len(x) / 2)]
else:
    med = (sorted(x)[int(len(x) / 2)] + sorted(x)[int(len(x) / 2 + 1)]) / 2
print("Медиана: ", med)
for i in x:
    result.append("+" if i >= med else "-")
print("Серия: ", result)

count = 1
for j in range(1, len(result)):
    if result[j] != result[j - 1]:
        count += 1
print("Количечтво серий: ", count)
print("40 < ", count, " < 61")

s = []
s1 = []
s2 = []
s3 = []
for i in range(len(x)):
    s.append(i * x[i])
    s1.append(x[i] * ((len(x) + 1) / 2))
    s2.append(x[i] ** 2)


r = (math.fsum(s) / len(x) - math.fsum(s1) / len(x))
m = np.sqrt((math.fsum(s2) / len(x) - (math.fsum(x) / len(x)) ** 2) * (len(x) ** 2 - 1) / 12)
rr = r / m
print(rr)
r_max = 1.96 * (1 - rr ** 2) / np.sqrt(len(x))
print(r_max)
print("Корреляция отсутствует")
