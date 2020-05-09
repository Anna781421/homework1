import torch
import numpy as np
import matplotlib.pyplot as plt
import math
import argparse


def iterate(text, subs):
    """
    Функция для построения строчки, каждый символ заменяется значением из
    массива, если можно, если нельзя, то просто переносим его
    в новую строчку
    """
    new_text = []
    for symbol in list(text):
        if symbol in subs:
            new_text.append(subs[symbol])
        else:
            new_text.append(symbol)

    return ''.join(new_text)


def buildLSystem():
    """
    Дана стартовая строка и набор правил для построения L-системы
    """
    axiom = 'F-G-G'
    subs = {'F': 'F-G+F+G-F', 'G': 'GG'}
    """
    Достаю входные данные: число итераций для системы
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--num', type=int, default=4)
    args = parser.parse_args()

    n = args.num
    # Строим строчку
    text = axiom
    for _ in range(n):
        text = iterate(text, subs)

    return text


def calculateCUDA(lsystem):
    arr = []  # Массив координат треугольника
    direction = torch.Tensor([[1, 0]]).cuda()  # Начальный вектор направления
    pos = torch.Tensor([[0, 0]]).cuda()  # Текущая позиция

    for symbol in lsystem:
        if symbol == 'F' or symbol == 'G':
            newpos = torch.add(
                input=pos, other=direction,
                alpha=3)  # Прибавляем вектор направления к текущим координатам
            arr.append(pos.cpu().numpy())  # Записываем координаты в массив
            pos = newpos
        elif symbol == '+':
            rot = torch.Tensor([[-0.5, math.sqrt(3) / 2],
                                [-math.sqrt(3) / 2, -0.5]]).cuda()
            direction = direction.mm(rot)
        elif symbol == '-':
            rot = torch.Tensor([[-0.5, -math.sqrt(3) / 2],
                                [math.sqrt(3) / 2, -0.5]]).cuda()
            direction = direction.mm(rot)

    return arr


if __name__ == '__main__':
    """
    Начало программы, строим L-систему и передаем ее в функцию расчета
    """
    # print(buildLSystem())
    cords = calculateCUDA(
        buildLSystem())  # Потом по строчке собираем координаты треугольника

    # Рисуем по массиву координат
    plt.plot(
        list(map(lambda x: x[0][0], cords)) + [0],
        list(map(lambda x: x[0][1], cords)) + [0])

    plt.show()
    