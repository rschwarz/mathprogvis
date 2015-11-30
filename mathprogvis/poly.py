import cdd
from matplotlib import pyplot as plt
from matplotlib.collections import PolyCollection
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np
from scipy.spatial import ConvexHull

NT = 'float'

# from http://stackoverflow.com/a/8567929
def unique_rows(a):
    a = np.ascontiguousarray(a)
    unique_a = np.unique(a.view([('', a.dtype)]*a.shape[1]))
    return unique_a.view(a.dtype).reshape((unique_a.shape[0], a.shape[1]))


def split_gens(gens):
    'split generators into vertices and rays'
    g = np.array(gens)
    if g.size == 0:
        return g, g
    return g[g[:,0]==1, 1:], g[g[:,0]==0, 1:]


def verts2ineqs(verts):
    'computes (dense) inequalities from vertices'
    v = np.array(verts)
    # prepend 1 to denote vertices
    v = np.hstack((np.ones((v.shape[0], 1)), v))
    V = cdd.Matrix(v, number_type=NT)
    V.rep_type = cdd.RepType.GENERATOR
    H = cdd.Polyhedron(V).get_inequalities()
    return np.array(H)


def ineqs2verts(ineqs):
    'computes (dense) inequalities from vertices'
    h = np.array(ineqs)
    H = cdd.Matrix(h, number_type=NT)
    H.rep_type = cdd.RepType.INEQUALITY
    V = cdd.Polyhedron(H).get_generators()
    v, r = split_gens(V)
    assert r.size == 0, 'generating rays found: %s' % V
    return v


def sparse2ineqs(sparse, variables):
    '''computes (dense) inequalities from dict-based inequalities

    Arguments:
     - ineqs: list of dicts that map varnames to coefficient.
              the format is "ax + b >= 0", the empty string maps to "b"
     - variables: list of varnames for column order

    Returns:
     - array of coefficients [b, a]
    '''
    nrows, ncols = len(sparse), len(variables) + 1
    j = {var:idx + 1 for (idx,var) in enumerate(variables)}
    j[''] = 0

    h = np.zeros((nrows, ncols))
    for i,row in enumerate(sparse):
        for var,coef in row.items():
            h[i, j[var]] = coef
    return h


def sparse2verts(sparse, variables):
    '''computes vertices from dict-based inequalities

    Arguments:
     - ineqs: list of dicts that map varnames to coefficient.
              the format is "ax + b >= 0", the empty string maps to "b"
     - variables: list of varnames for column order

    Returns:
     - vertices
    '''
    h = sparse2ineqs(sparse, variables)
    return ineqs2verts(h)


def proj_verts2verts(verts, keep_indices):
    'project vertices to subspace'
    v = np.array(verts)
    pv = v[:, keep_indices]
    return unique_rows(pv)


def proj_ineqs2verts(ineqs, keep_indices):
    'project ineqs to subspace, return vertices'
    return proj_verts2verts(ineqs2verts(ineqs), keep_indices)


def proj_sparse2verts(sparse, variables, keep):
    'project sparse ineqs to subspace, return vertices'
    ineqs = sparse2ineqs(sparse, variables)
    indices = [variables.index(k) for k in keep]
    return proj_ineqs2verts(ineqs, indices)


def plot2d(*args):
    'plot collections'
    fig, ax = plt.subplots()
    for s in args:
        ax.add_collection(s)
    ax.autoscale_view(tight=True)
    return fig, ax


def plot3d(*args):
    'plot collections'
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    for s in args:
        ax.add_collection3d(s)
    ax.autoscale_view(tight=True)
    return fig, ax


def polygon2D(verts, alpha=0.2, **kwargs):
    'builds 2D polygon collection from vertices'
    hull = ConvexHull(verts)
    fullface = np.array([[hull.points[v] for v in hull.vertices]])
    return PolyCollection(fullface, alpha=alpha, **kwargs)


def polygon3D(verts, alpha=0.2, **kwargs):
    'builds 3D polygon collection from vertices'
    hull = ConvexHull(verts)
    facets = np.array([hull.points[s] for s in hull.simplices])
    return Poly3DCollection(facets, alpha=alpha, **kwargs)
