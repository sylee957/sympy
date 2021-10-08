from collections import defaultdict
from itertools import chain, compress


def free_symbols_sparse(p):
    exponents = list(map(sum, zip(*p)))
    return {n for n, e in enumerate(exponents) if e}


def _coeffs_sparse(p1, syms):
    N = len(p1.ring.gens)
    nsyms = set(range(N)) - syms
    p2 = defaultdict(dict)
    r = range(N)
    for m1, c1 in p1.items():
        # m21 = tuple(m1[i] if i in syms else 0 for i in range(N))
        # m22 = tuple(m1[i] if i in nsyms else 0 for i in range(N))
        # p2[m21][m22] = c1
        sym_indices = set(compress(r, m1))
        m21 = [0] * N
        m22 = [0] * N
        for i in sym_indices & syms:
            m21[i] = m1[i]
        for i in sym_indices & nsyms:
            m22[i] = m1[i]
        p2[tuple(m21)][tuple(m22)] = c1
    return p2


def coeffs_sparse(p1, syms):
    p2 = _coeffs_sparse(p1, syms)
    return [p1.ring(pi) for pi in p2.values()]


def coeff_sparse(p1, sym, deg):
    p2 = _coeffs_sparse(p1, {sym})
    m = [0] * len(p1.ring.gens)
    m[sym] = deg
    m = tuple(m)
    return p1.ring(p2[m])


def gcd_sparse(p):
    R = p[0].ring
    K = R.domain

    # 1-term gcd?
    if any(len(pi) == 1 for pi in p):
        return gcd_terms(p, R, K)

    # Extract the monomial gcd
    p, d = gcd_monomial(p)

    # Eliminate nonshared symbols
    p, common = gcd_coeffs(p)

    # Use subresultant PRS
    g = p[0]
    for pi in p[1:]:
        g = gcd_prs_sparse(g, pi)

    if d is not None:
        g = g * d

    return g

def gcd_terms(p, R, K):
    #
    # If any of the polynomials only has a single term then the gcd does as
    # well and must divide all terms. We can bypass all of the more
    # complicated algorithms and find the gcd of the monomials and the gcd of
    # the coefficients.
    #
    terms = chain.from_iterable(pi.terms() for pi in p)
    monoms = set()
    coeffs = set()
    for m, c in terms:
        monoms.add(m)
        coeffs.add(c)
    monom_gcd = gcd_monom(monoms)
    coeff_gcd = gcd_ground(coeffs, K)
    term_gcd = R({monom_gcd: coeff_gcd})
    return term_gcd

def gcd_ground(c, K):
    #
    # gcd in the ground domain
    #
    c = list(c)
    gcd = K.gcd
    d = c[0]
    for ci in c[1:]:
        d = gcd(d, ci)
        if d == K.one:
            break
    return d

def gcd_monom(monoms):
    #
    # gcd of a list of monomials
    #
    monom_gcd = tuple(map(min, zip(*monoms)))
    return monom_gcd

def gcd_monomial(p):
    #
    # Extract any common monomial from the polynomials in p
    #
    R = p[0].ring
    monoms = chain(*p)
    monom_gcd = tuple(map(min, zip(*monoms)))
    if monom_gcd == R.zero_monom:
        return p, None
    else:
        d = R({monom_gcd: R.domain.one})
        p = [pi.exquo(d) for pi in p]
        return p, d


def gcd_coeffs(p):
    #
    # Simplify a list of polys whose gcd is wanted. Returns a possibly longer
    # list of simpler polys having the same gcd as the input. This is done by
    # eliminating symbols that can not be part of the gcd because they do not
    # appear in each item of the input. In the output list all items have
    # exactly the same symbols. The set of those symbols is also returned.
    #
    # Given d = gcd(p(x, y), q(y, z)) then d = r(y) does not depend on x or z.
    # Write p(x, y) as a poly in x with coeffs that are polys in y:
    #
    #   p(x, y) = p0(y) + p1(y)*x + p2(y)*x**2 + ...
    #   q(x, y) = q0(y) + q1(y)*z + q2(y)*z**2 + ...
    #
    # Now r(y) = gcd(p0, p1, ..., q0, q1, ...)
    #
    # We can eliminate all symbols that do not appear in all polys until every
    # poly has exactly the same symbols in it.
    #
    # This can very quickly pick out a term with a coefficient of 1 without
    # the need to do any poly arithmetic. If 1 or -1 is encountered the
    # routine returns [1] immediately.
    #
    # In computing gcd of multivariate polynomials this routine is an
    # important optimisation for the common case where the gcd is just 1. Even
    # if the gcd is not 1 we can still reduce the number of symbols
    # drastically in some cases before proceeding to e.g. subresultant PRS
    # where performance depends strongly on the number of symbols.
    #
    # Example:
    #
    #   >>> x = symbols('x:10')
    #   >>> K = QQ[x]
    #   >>> p1 = K.from_sympy(sum(x[:8]))
    #   >>> p2 = K.from_sympy(sum(x[2:]))
    #   >>> p1
    #   x0 + x1 + x2 + x3 + x4 + x5 + x6 + x7
    #   >>> p2
    #   x2 + x3 + x4 + x5 + x6 + x7 + x8 + x9
    #   >>> gcd_coeffs([p1, p2])
    #   ([1], set())
    #
    all_coeffs = p

    while True:
        # Quick exits are most efficient if we start from the simplest polys
        p = sorted(set(all_coeffs), key=len)

        # Find the intersection of symbols for each poly:
        common = free_symbols_sparse(p[0])
        allsame = True
        for pi in p[1:]:

            # Quick exit
            if not common:
                R = p[0].ring
                K = R.domain
                gcd = gcd_terms(p, R, K)
                return [gcd], None

            syms = free_symbols_sparse(pi)
            if allsame and syms != common:
                allsame = False
            common &= syms

        # The loop is complete if they all have the same symbols.
        if allsame:
            return p, common

        # Extract coefficients as polys containing only the common symbols.
        all_coeffs = []
        for i, pi in enumerate(p):
            coeffs_i = coeffs_sparse(pi, free_symbols_sparse(pi) - common)
            all_coeffs.extend(coeffs_i)

            # Quick exit:
            if any(len(c) == 1 for c in coeffs_i):
                R = p[0].ring
                K = R.domain
                gcd = gcd_terms(all_coeffs + p[i+1:], R, K)
                return [gcd], None


def prem_sparse(f, g, x):
    df = f.degree(x)
    dg = g.degree(x)

    if dg < 0:
        raise ZeroDivisionError

    r, dr = f, df

    if df < dg:
        return r

    N = df - dg + 1

    lc_g = coeff_sparse(g, x, dg)

    xp = f.ring.gens[x]

    while True:
        lc_r = coeff_sparse(r, x, dr)
        j, N = dr - dg, N - 1

        R = r * lc_g
        G = g * lc_r * xp**j
        r = R - G

        _dr, dr = dr, r.degree(x)

        if dr < dg:
            break
        elif not (dr < _dr):
            raise ValueError

    c = lc_g ** N

    return r * c


def subresultants_sparse(f, g, x):
    n = f.degree(x)
    m = g.degree(x)

    if n < m:
        f, g = g, f
        n, m = m, n

    if f == 0:
        return 0, 0

    if g == 0:
        return f, 1

    R = [f, g]
    d = n - m

    b = (-1) ** (d + 1)

    h = prem_sparse(f, g, x)
    h = h * b

    lc = coeff_sparse(g, x, m)
    c = lc ** d

    S = [1, c]
    c = -c

    while h:
        k = h.degree(x)
        R.append(h)

        f, g, m, d = g, h, k, m-k

        b = -lc * c**d

        h = prem_sparse(f, g, x)
        h = h.exquo(b)

        lc = coeff_sparse(g, x, k)

        if d > 1:
            p = (-lc) ** d
            q = c ** (d-1)
            c = p.exquo(q)
        else:
            c = -lc

        S.append(-c)

    return R


def primitive_sparse(p, x):
    coeffs = coeffs_sparse(p, {x})
    content = gcd_sparse(coeffs)
    primitive = p.exquo(content)
    return content, primitive


def main_variable_sparse(p):
    syms = free_symbols_sparse(p)
    if not syms:
        return None
    return min(syms)


def gcd_prs_sparse(p1, p2):
    x = main_variable_sparse(p1)
    if x is None:
        return p1.ring.one

    c1, pp1 = primitive_sparse(p1, x)
    c2, pp2 = primitive_sparse(p2, x)

    h = subresultants_sparse(pp1, pp2, x)[-1]
    c = gcd_sparse([c1, c2])

    K = p1.ring.to_domain()
    if K.is_negative(coeff_sparse(h, x, h.degree(x))):
        h = -h

    _, h = primitive_sparse(h, x)
    h = h * c

    return h
