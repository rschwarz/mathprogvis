import numpy as np

def ineqs(x, y, z, xl, xu, yl, yu):
    '''sparse inequalities for z = x*y

    Arguments:
     - x, y, z: strings for variables names
     - xl, xu: bounds for x
     - yl, yu: bounds for y

    Returns:
     - list of inequalities in sparse dict form (ax + b >= 0)

    '''
    # The four inequalities read:
    # z >= x*yl + xl*y - xl*yl
    # z >= x*yu + xu*y - xu*yu
    # z <= x*yu + xl*y - xl*yu
    # z <= x*yl + xu*y - xu*yl
    b = ''
    res = [
        {x:-yl, y:-xl, z: 1, b: xl*yl},
        {x:-yu, y:-xu, z: 1, b: xu*yu},
        {x: yu, y: xl, z:-1, b:-xl*yu},
        {x: yl, y: xu, z:-1, b:-xu*yl},
    ]

    return res


def sparse_ineqs(x, y, z, variables, lower, upper):
    '''sparse inequalities for z = x*y, all given as sparse affine expressions

    Arguments:
     - x, y, z: sparse affine expressions
     - variables: list of varnames
     - lower: lower bounds for variables
     - upper: lower bounds for variables

    Returns:
     - list of inequalities in sparse dict form (ax + b >= 0)
    '''
    assert len(variables) == len(lower)
    assert len(variables) == len(upper)

    _x, _y, _z, b = 'x', 'y', 'z', ''

    lb, ub = dict(zip(variables, lower)), dict(zip(variables, upper))
    lb[b], ub[b] = 1, 1    # constant term

    xl, xu, yl, yu = 0.0, 0.0, 0.0, 0.0
    for var, coef in x.items():
        if coef > 0:
            xl += coef * lb[var]
            xu += coef * ub[var]
        else:
            xl += coef * ub[var]
            xu += coef * lb[var]
    for var, coef in y.items():
        if coef > 0:
            yl += coef * lb[var]
            yu += coef * ub[var]
        else:
            yl += coef * ub[var]
            yu += coef * lb[var]

    res = []
    for i in ineqs(_x, _y, _z, xl, xu, yl, yu):
        row = {b:i[b]}
        for _v, expr in zip([_x, _y, _z], [x, y, z]):
            for var, coef in expr.items():
                row[var] = row.get(var, 0.0) + i[_v] * coef

        for k in [k for k in row if row[k] == 0.0]:
            del row[k]

        if row:
            res.append(row)

    return res
