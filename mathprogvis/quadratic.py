import numpy as np

def hull(x, y, xlb, xub, n=20):
    '''compute convex hull for y == x**2

    Arguments:
     - x, y: varnames
     - xlb, xub: domain of x
     - n: number of tangent cuts to add
     - negate: if True, model -y == x**2

    Returns:
     - list of dicts for inequalities in form a*x + b >= 0
    '''
    b = ''
    ineqs = []

    # secant: y <= (xub**2 - xlb**)/(xub - xlb)*(x - xlb) + xlb**2
    #         y <= (xub + xlb)*x - xub*xlb
    ineqs += [{x:xub + xlb, y:-1, b:-xub*xlb}]

    # tangents at p: y >= 2*p*(x - p) + p**2
    #                y >= 2*p*x - p**2
    ineqs += [{x:-2*p, y:1, b:p**2} for p in np.linspace(xlb, xub, n)]

    return ineqs
