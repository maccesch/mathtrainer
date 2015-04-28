from time import mktime
from flask import Flask, render_template
from datetime import date
from sympy import S, floor, sqrt, factor, Add, Eq, symbols, latex, simplify, exp, log
import locale
from numpy.random import seed, random_integers as randint

locale.setlocale(locale.LC_ALL, 'de_DE')
app = Flask(__name__)


def desolve_equation(lhs, rhs, operation_count):
    for i in range(operation_count):
        number = S(randint(1, 10) * (randint(0, 1) * 2 - 1))
        op = randint(0, 10)
        if op <= 6:
            rhs = Add(rhs, number, evaluate=(randint(0, 1) == 1))
            lhs = Add(lhs, number, evaluate=(randint(0, 1) == 1))
        elif op <= 8:
            rhs *= number
            lhs *= number
        else:
            rhs /= number
            lhs /= number

    return lhs, rhs


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
    equations.append(generate_quadratic_equation())
    #equations.append(generate_exponential_equation())
    equations.append(generate_equation())

    return equations


@app.route('/')
def get_exercises_for_today():
    equations = get_equations_for_date(date.today())

    return render_template('exercises.html', equations=equations, date=date.today().strftime('%A, %d.%m.%Y'))


if __name__ == '__main__':
    app.run()