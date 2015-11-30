
def disj(ineqss, variables, indicator='delta'):
    '''Balas' extended formulation for union of convex sets.

    Assumes, that the origin is part of all disjunctive sets.

    Arguments:
      - ineqss: list of lists of dicts, representing sparse inequalities
                (format: ax + b >= 0)
      - variables: list of varnames
      - indicator: prefix of indicator variables

    Returns:
      - list of dicts for ineqs
      - list of indicator varnames
      - list of other added varnames
    '''
    n = len(ineqss)
    idx = list(range(n))

    ineqs = []
    inds = ['%s#%d' % (indicator, i) for i in idx]
    copies = {(v,i):'%s#%d' % (v,i) for v in variables for i in idx}

    b = ''

    # sum_i indicator_i == 1, indicator_i >= 0
    ineqs += [dict(zip(inds + [b], [ 1]*n + [-1])),
              dict(zip(inds + [b], [-1]*n + [ 1]))]
    ineqs += [{inds[i]:1} for i in idx]

    # variables as convex combination of copies
    # v == sum_i v_i
    for v in variables:
        ineqs += [dict(zip([copies[v,i] for i in idx] + [v], [ 1]*n + [-1])),
                  dict(zip([copies[v,i] for i in idx] + [v], [-1]*n + [ 1]))]

    # disjunctive models with copies of variables
    # a*x_i + b*indicator_i >= 0
    for i in idx:
        for ineq in ineqss[i]:
            row = {}
            for var in variables:
                row[copies[var,i]] = ineq.get(var, 0.0)
            row[inds[i]] = ineq.get(b, 0.0)
            for k in [k for k in row if row[k] == 0.0]:
                del row[k]
            ineqs.append(row)

    return ineqs, inds, sorted(copies.values())
