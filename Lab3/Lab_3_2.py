import math
import random
from scipy import stats

x = 38
a = 37
b = 1
M = 1000
lam = 0.1


if __name__ == '__main__':
    n = 100
    xi = [[random.random() for j in range(12)] for i in range(n)]  # Равномерно распределенная СВ от 0 до 1
    zi = [(sum(i) - 6) * 0.25 + 3 for i in xi]  # Центральная предельная теорема

    print(zi)

    m_o = sum(zi) / n
    d_o = sum([(i - m_o) ** 2 for i in zi]) / n

    print('Матожидание:', m_o)
    print('Дисперсия:', d_o)
    print('Средне крадратическое отклонение', math.sqrt(d_o))
    print('Погрешность матожидания:', math.fabs(m_o - 3) / 3)
    print('Погрешность отклонения:', math.fabs(math.sqrt(d_o) - 0.25) / 0.25)

    # ----------------------

    h = (max(zi) - min(zi)) / (1 + 3.3221 * math.log(n, 10))  # Считаем шаг

    intervals = [min(zi), min(zi) + h]  # Получаем интервалы

    while max(zi) >= intervals[-1]:
        intervals.append(intervals[-1] + h)

    ni = [0 for i in range(len(intervals) - 1)]  # Получаем частоты
    for i in zi:
        for j in range(1, len(intervals)):
            if i < intervals[j]:
                ni[j - 1] += 1
                break

    fi = lambda x: 1 / math.sqrt(2 * math.pi) * math.exp(- (x ** 2) / 2)  # Считаем FI
    # Теоретические частоты
    ni_ = [n * h / math.sqrt(d_o) * fi(((intervals[i - 1] + intervals[i]) / 2 - m_o) / math.sqrt(d_o)) for i in
           range(1, len(intervals))]

    o_ni = ni.copy()
    o_ni_ = ni_.copy()
    for i in range(2, len(o_ni)):
        if o_ni[i] < 5:
            for j in range(i + 1, len(o_ni)):
                o_ni[i] += o_ni[j]
                o_ni_[i] += o_ni_[j]
            del o_ni[i + 1: len(o_ni)]
            del o_ni_[i + 1: len(o_ni_)]
            break

    o_ni[1] += o_ni[0]
    o_ni_[1] += o_ni_[0]
    o_ni[-2] += o_ni[-1]
    o_ni_[-2] += o_ni_[-1]
    del o_ni[0]
    del o_ni_[0]
    del o_ni[-1]
    del o_ni_[-1]

    print('\nИнтервалы:', intervals)
    print('Шаг:', h)
    print('\nКоличество интервалов:', len(ni))
    print('Частоты:', ni)
    print('Теоритические частоты:', ni_)
    print('\nКоличество объединенных интервалов:', len(o_ni))
    print('Объединенные частоты:', o_ni)
    print('Объединенные теоритические частоты:', o_ni_)

    X2 = sum([((ni[i] - ni_[i]) ** 2) / ni_[i] for i in range(len(ni))])  # Критерий Пирсона

    print('\nX^2:', X2, "< 7.8")

    n_ni = [sum(ni[0: i]) for i in range(1, len(ni) + 1)]

    m_o = sum([ni[i - 1] * (intervals[i - 1] + intervals[i]) / 2 for i in range(1, len(intervals))]) / n
    d_o = sum([ni[i - 1] * (((intervals[i - 1] + intervals[i]) / 2) - m_o) ** 2 for i in range(1, len(intervals))]) / n

    print('\nМатожидание через интервалы:', m_o)
    print('Дисперсия через интервалы:', d_o)

    lap = lambda g: stats.norm.cdf(g) - 0.5  # Функция Лапласа
    print(lap(6))
    max = 0
    print('\nСередины', '\t\t\tЧастоты', '\tНакопленные', '\tFn(x)', '\tF(x)', '\t\t\t\t|Fn(x) - F(x)|')
    for i in range(len(ni)):
        print((intervals[i] + intervals[i + 1]) / 2, end='\t')  # Середины
        print(ni[i], end='\t\t\t')  # Частоты
        print(n_ni[i], end='\t\t\t\t')  # Накопленные частоты
        print(n_ni[i] / n, end='\t')  # Fn(n(накоп) / n(100))
        if n_ni[i] / n == 1:
            print(end='\t')
        fx = 0.5 + lap((((intervals[i] + intervals[i + 1]) / 2) - m_o) / math.sqrt(d_o))
        print(round(fx, 16), end='\t')  # Функция Лапласа
        fx = math.fabs(n_ni[i] / n - fx)
        print(fx)  # '|Fn(x) - F(x)|'
        if fx > max:
            max = fx

    print('\nМаксимальное расхождение:', max)
    print('Лямбда:', max * math.sqrt(n), '<' if max * math.sqrt(n) < 1.36 else '>', '1.36')
