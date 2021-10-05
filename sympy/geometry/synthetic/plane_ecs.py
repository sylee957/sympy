from sympy.geometry.synthetic.constructions import SyntheticGeometryOn as On
from sympy.geometry.synthetic.constructions import SyntheticGeometryLine as Line
from sympy.geometry.synthetic.constructions import SyntheticGeometryPLine as PLine
from sympy.geometry.synthetic.constructions import SyntheticGeometryTLine as TLine
from sympy.geometry.synthetic.constructions import SyntheticGeometryBLine as BLine
from sympy.geometry.synthetic.constructions import SyntheticGeometryALine as ALine
from sympy.geometry.synthetic.constructions import SyntheticGeometryCircle as Circle
from sympy.geometry.synthetic.constructions import SyntheticGeometryLRatio as LRatio
from sympy.geometry.synthetic.constructions import SyntheticGeometryMRatio as MRatio
from sympy.geometry.synthetic.constructions import SyntheticGeometryPRatio as PRatio
from sympy.geometry.synthetic.constructions import SyntheticGeometryTRatio as TRatio
from sympy.geometry.synthetic.constructions import SyntheticGeometryARatio as ARatio
from sympy.geometry.synthetic.constructions import SyntheticGeometryCentroid as Centroid
from sympy.geometry.synthetic.constructions import SyntheticGeometryOrthocenter as Orthocenter
from sympy.geometry.synthetic.constructions import SyntheticGeometryCircumcenter as Circumcenter
from sympy.geometry.synthetic.constructions import SyntheticGeometryIncenter as Incenter
from sympy.geometry.synthetic.constructions import SyntheticGeometryIntersection as Intersection
from sympy.geometry.synthetic.constructions import SyntheticGeometryFoot as Foot
from sympy.geometry.synthetic.constructions import SyntheticGeometryMidpoint as Midpoint
from sympy.geometry.synthetic.constructions import SyntheticGeometryInversion as Inversion
from sympy.geometry.synthetic.predicates import SyntheticGeometryCollinear as Collinear
from sympy.geometry.synthetic.predicates import SyntheticGeometryEqpoints as Eqpoints
from sympy.geometry.synthetic.predicates import SyntheticGeometryPerpendicular as Perpendicular
from sympy.geometry.synthetic.auxiliary import SyntheticGeometryAuxiliaryRatio as AuxiliaryRatio
from sympy.geometry.synthetic.auxiliary import SyntheticGeometryAuxiliaryPoint as AuxiliaryPoint
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedRatio as Ratio
from sympy.geometry.synthetic.quantities import SyntheticGeometryPythagorasDifference as Pythagoras
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedArea as Area
from sympy.geometry.synthetic.ecs import PlaneECS1 as ECS1
from sympy.geometry.synthetic.ecs import PlaneECS5 as ECS5
from sympy.geometry.synthetic.ecs import PlaneECS6 as ECS6
from sympy.geometry.synthetic.ecs import PlaneECS7 as ECS7
from sympy.geometry.synthetic.ecs import PlaneECS8 as ECS8
from sympy.core.numbers import Rational, Integer


def _inter_line_line(C):
    Y, L1, L2 = C.args
    if isinstance(L1, Line) and isinstance(L2, Line):
        U, V = L1.args
        P, Q = L2.args
        return ECS1(Y, U, V, P, Q)


def _tline_to_line(constructions, prove, W, U, V):
    if prove(tuple(constructions), Collinear(W, U, V)) == True:
        if prove(tuple(constructions), Eqpoints(W, U)):
            N = AuxiliaryPoint(W, V)
            return N, TRatio(N, W, V, Integer(1))
        else:
            N = AuxiliaryPoint(W, U)
            return N, TRatio(N, W, U, Integer(1))
    else:
        N = AuxiliaryPoint(W, U, V)
        return N, Foot(N, W, U, V)


def _convert_inter_line_line(C):
    if isinstance(C, Intersection):
        Y, L1, L2 = C.args
        if isinstance(L1, Line) and isinstance(L2, Line):
            U, V = L1.args
            P, Q = L2.args
            return ECS1(Y, U, V, P, Q)


def _convert_tratio(C):
    Y, U, V, r = C.args
    return [TRatio(Y, U, V, r)]


def _convert_aline(constructions, prove, C):
    P, Q, W, U, V = C.args
    if prove(constructions, Perpendicular(U, W, W, V)):
        return [], TLine(P, P, Q)
    else:
        R = AuxiliaryPoint(Q, P)
        aux = TRatio(R, Q, P, 4*Area(U, W, V)/Pythagoras(U, W, V))
        return _convert_tratio(aux), Line(P, R)


def _constructions_to_ecs(constructions, prove):
    constructions = list(constructions)
    new = []
    for C in constructions:
        if isinstance(C, On):
            Y, L = C.args
            if isinstance(L, Line):
                U, V = L.args
                new.append(PRatio(Y, U, U, V, AuxiliaryRatio(U, Y, U, V)))
                continue

            if isinstance(L, PLine):
                W, U, V = L.args
                new.append(PRatio(Y, W, U, V, AuxiliaryRatio(W, Y, U, V)))
                continue

            if isinstance(L, TLine):
                W, U, V = L.args
                N, aux = _tline_to_line(new, prove, W, U, V)
                new.append(aux)
                new.append(PRatio(Y, N, N, W, AuxiliaryRatio(N, Y, N, W)))
                continue

            if isinstance(L, BLine):
                U, V = L.args
                N = AuxiliaryPoint(U, V)
                M = AuxiliaryPoint(N, U, V)
                new.append(PRatio(N, U, U, V, Rational(1, 2)))
                new.append(TRatio(M, N, U, Integer(1)))
                new.append(PRatio(Y, M, M, N, AuxiliaryRatio(M, Y, M, N)))
                continue

        if isinstance(C, Intersection):
            Y, L1, L2 = C.args
            if isinstance(L1, Line) and isinstance(L2, Line):
                new.append(_convert_inter_line_line(C))
                continue

            if isinstance(L1, Line) and isinstance(L2, PLine):
                U, V = L1.args
                R, P, Q = L2.args
                new.append(ECS5(Y, U, V, R, P, Q))
                continue

            if isinstance(L1, PLine) and isinstance(L2, Line):
                U, V = L2.args
                R, P, Q = L1.args
                new.append(ECS5(Y, U, V, R, P, Q))
                continue

            if isinstance(L1, Line) and isinstance(L2, TLine):
                U, V = L1.args
                R, P, Q = L2.args
                new.append(ECS6(Y, U, V, R, P, Q))
                continue

            if isinstance(L1, TLine) and isinstance(L2, Line):
                U, V = L2.args
                R, P, Q = L1.args
                new.append(ECS6(Y, U, V, R, P, Q))
                continue

            if isinstance(L1, Line) and isinstance(L2, BLine):
                U, V = L1.args
                P, Q = L2.args
                new.append(ECS7(Y, U, V, P, Q))
                continue

            if isinstance(L1, BLine) and isinstance(L2, Line):
                U, V = L2.args
                P, Q = L1.args
                new.append(ECS7(Y, U, V, P, Q))
                continue

            if isinstance(L1, BLine) and isinstance(L2, BLine):
                U, V = L1.args
                P, Q = L2.args
                N = AuxiliaryPoint(U, V)
                M = AuxiliaryPoint(N, U, V)
                new.append(PRatio(N, U, U, V, Rational(1, 2)))
                new.append(TRatio(M, N, U, Integer(1)))
                new.append(ECS7(Y, N, M, P, Q))
                continue

            if isinstance(L1, Line) and isinstance(L2, Circle):
                U, V = L1.args
                O, P = L2.args
                if P == V:
                    U, V = V, U
                if P == U:
                    new.append(ECS8(Y, U, V, O))
                    continue

            if isinstance(L1, PLine) and isinstance(L2, PLine):
                W, U, V = L1.args
                R, P, Q = L2.args
                N = AuxiliaryPoint(W, U, V)
                new.append(PRatio(N, W, U, V, Integer(1)))
                new.append(ECS5(Y, W, N, R, P, Q))
                continue

            if isinstance(L1, TLine) and isinstance(L2, TLine):
                W, U, V = L1.args
                R, P, Q = L2.args
                N, aux = _tline_to_line(new, prove, W, U, V)
                new.append(aux)
                new.append(ECS6(Y, N, W, R, P, Q))
                continue

            if isinstance(L1, ALine) and isinstance(L2, ALine):
                aux1, L1 = _convert_aline(new, prove, L1)
                aux2, L2 = _convert_aline(new, prove, L2)
                new.extend(aux1)
                new.extend(aux2)
                aux3 = _convert_inter_line_line(Intersection(Y, L1, L2))
                new.append(aux3)
                continue

        if isinstance(C, Midpoint):
            Y, U, V = C.args
            new.append(PRatio(Y, U, U, V, Rational(1, 2)))
            continue

        if isinstance(C, Foot):
            Y, P, U, V = C.args
            new.append(Foot(Y, P, U, V))
            continue

        if isinstance(C, PRatio):
            Y, W, U, V, r = C.args
            new.append(PRatio(Y, W, U, V, r))
            continue

        if isinstance(C, LRatio):
            Y, U, V, r = C.args
            new.append(PRatio(Y, U, U, V, r))
            continue

        if isinstance(C, MRatio):
            Y, U, V, r = C.args
            new.append(PRatio(Y, U, U, V, r / (r + 1)))
            continue

        if isinstance(C, TRatio):
            Y, U, V, r = C.args
            new.append(TRatio(Y, U, V, r))
            continue

        if isinstance(C, Inversion):
            P, Q, O, A = C.args
            if prove(tuple(new), Collinear(Q, O, A)):
                new.append(PRatio(P, O, O, A, Ratio(O, A, O, Q)))
                continue
            else:
                new.append(PRatio(P, O, O, Q, Pythagoras(O, A, O) / Pythagoras(O, Q, O)))
                continue

        if isinstance(C, ARatio):
            new.append(C)
            continue
        if isinstance(C, Centroid):
            Y, A, B, C = C.args
            r_A = Rational(1, 3)
            r_B = Rational(1, 3)
            r_C = Rational(1, 3)
            new.append(ARatio(Y, A, B, C, r_A, r_B, r_C))
            continue
        if isinstance(C, Orthocenter):
            Y, A, B, C = C.args
            r_A = Pythagoras(A, B, C)*Pythagoras(A, C, B) / (16*Area(A, B, C)**2)
            r_B = Pythagoras(B, A, C)*Pythagoras(B, C, A) / (16*Area(A, B, C)**2)
            r_C = Pythagoras(C, A, B)*Pythagoras(C, B, A) / (16*Area(A, B, C)**2)
            new.append(ARatio(Y, A, B, C, r_A, r_B, r_C))
            continue
        if isinstance(C, Circumcenter):
            Y, A, B, C = C.args
            r_A = Pythagoras(B, C, B)*Pythagoras(B, A, C) / (32*Area(A, B, C)**2)
            r_B = Pythagoras(A, C, A)*Pythagoras(A, B, C) / (32*Area(A, B, C)**2)
            r_C = Pythagoras(A, B, A)*Pythagoras(A, C, B) / (32*Area(A, B, C)**2)
            new.append(ARatio(Y, A, B, C, r_A, r_B, r_C))
            continue
        if isinstance(C, Incenter):
            C, I, A, B = C.args
            r_I = -2*Pythagoras(I, A, B)*Pythagoras(I, B, A) / (Pythagoras(A, I, B)*Pythagoras(A, B, A))
            r_A = Pythagoras(I, A, B)*Pythagoras(I, B, I) / (Pythagoras(A, I, B)*Pythagoras(A, B, A))
            r_B = Pythagoras(I, B, A)*Pythagoras(I, A, I) / (Pythagoras(A, I, B)*Pythagoras(A, B, A))
            new.append(ARatio(C, I, A, B, r_I, r_A, r_B))
            continue

        raise NotImplementedError(f"Unknown construction: {C}")

    return tuple(new)
