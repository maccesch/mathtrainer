# coding=utf-8
from time import mktime
from flask import Flask, render_template
from datetime import date
from sympy import S, floor, sqrt, factor, Add, Eq, symbols, latex, simplify, exp, log, root
import locale
from numpy.random import seed, random_integers as randint, choice
from sympy.core.mul import Mul
from sympy.core.numbers import Rational

locale.setlocale(locale.LC_ALL, 'de_DE')
app = Flask(__name__)


def desolve_equation(lhs, rhs, operation_count, eq_symbols=range(1, 11)):
    for i in range(operation_count):
        number = S(choice(eq_symbols) * (randint(0, 1) * 2 - 1))
        op = randint(0, 10)
        if op <= 6:
            rhs = Add(rhs, number, evaluate=(randint(0, 1) == 1))
            lhs = Add(lhs, number, evaluate=(randint(0, 1) == 1))
        elif op <= 8:
            rhs = Mul(rhs, number, evaluate=(randint(0, 1) == 1))
            lhs = Mul(lhs, number, evaluate=(randint(0, 1) == 1))
        else:
            rhs = Mul(rhs, number**(-1), evaluate=(randint(0, 1) == 1))
            lhs = Mul(lhs, number**(-1), evaluate=(randint(0, 1) == 1))

    return lhs, rhs


def generate_hard_equation():
    x, a, b, c = symbols('x a b c')

    eq_symbols = [a, b, c] + range(-20, 0) + range(1, 21)

    solution = S(choice(eq_symbols))

    if (solution in (a, b, c) or solution > 0) and randint(0, 1):
        solution = sqrt(solution)
    if randint(0, 1):
        solution /= choice(eq_symbols)


    lhs = solution
    rhs = x

    lhs, rhs = desolve_equation(lhs, rhs, 10, eq_symbols)

    return latex(Eq(rhs, lhs)), [latex(solution)]


def generate_equation():
    solution = S(randint(-20, 20)) / S(randint(1, 10))

    lhs = solution
    rhs = symbols('x')

    lhs, rhs = desolve_equation(lhs, rhs, 7)

    return latex(Eq(rhs, lhs)), [latex(solution)]


def generate_quadratic_equation():
    p = S(randint(-10, 10))
    p2 = p / 2

    q = randint(-10, min(10, floor(p2 ** 2)))

    x1 = simplify(-p2 + sqrt(p2 ** 2 - q))
    x2 = simplify(-p2 - sqrt(p2 ** 2 - q))

    x = symbols('x')
    xx = x ** 2 + p * x

    if randint(0, 1):
        xx = factor(xx)
    rhs = xx + q
    lhs = S(0)

    lhs, rhs = desolve_equation(lhs, rhs, 5)

    solutions = [latex(x1)]
    if x1 != x2:
        solutions.append(latex(x2))

    return latex(Eq(rhs, lhs)), solutions


def generate_exponential_equation():

    solution_op = randint(0, 2)
    if solution_op == 0:
        solution = S(randint(-20, 20)) + sqrt(S(randint(0, 10))) * (randint(0, 1) * 2 - 1)
    elif solution_op == 1:
        solution = log(S(randint(1, 20)))
    else:
        solution = exp(S(randint(-10, 10)))

    x = symbols('x')

    lhs = x
    rhs = solution

    lhs, rhs = desolve_equation(lhs, rhs, 2)

    use_base = 0

    if solution_op == 0:
        use_base = randint(0, 1)
        op = randint(0, 1)
    elif solution_op == 1:
        op = 0
    else:
        op = 1

    if op and rhs > 0:
        lhs = log(lhs)
        rhs = log(rhs)
    else:
        if use_base:
            base = S(randint(2, 10))
            lhs = base ** lhs
            rhs = base ** rhs
        else:
            lhs = exp(lhs)
            rhs = exp(rhs)

    lhs, rhs = desolve_equation(lhs, rhs, 3)

    return latex(Eq(lhs, rhs)), (latex(simplify(solution)), )


def get_equations_for_date(thedate):

    seed(int(mktime(date.today().timetuple())))

    equations = []

    eq, sol = generate_quadratic_equation()
    equations.append((u'Aufgabe 1', ur'Bestimme die Lösungsmenge von \(x\).', eq, sol))

    # equations.append(generate_exponential_equation())

    eq, sol = generate_equation()
    equations.append((u'Aufgabe 2', ur'Löse nach \(x\) auf.', eq, sol))

    eq, sol = generate_hard_equation()
    equations.append((u'Bonushammeraufgabe', ur'Löse nach \(x\) auf. Eventuell vorkommende Symbole \(a\), \(b\) und \(c\) sind unbekannte Konstanten.', eq, sol))

    return equations


@app.route('/')
def get_exercises_for_today():
    equations = get_equations_for_date(date.today())

    return render_template('exercises.html', equations=equations, date=date.today().strftime('%A, %d.%m.%Y'))


if __name__ == '__main__':
    # app.debug = True
    app.run()