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
from sympy.geometry.synthetic.constructions import SyntheticGeometrySymmetry as Symmetry
from sympy.geometry.synthetic.constructions import SyntheticGeometryInversion as Inversion
from sympy.geometry.synthetic.predicates import SyntheticGeometryCollinear as Collinear
from sympy.geometry.synthetic.predicates import SyntheticGeometryEqpoints as Eqpoints
from sympy.geometry.synthetic.predicates import SyntheticGeometryPerpendicular as Perpendicular
from sympy.geometry.synthetic.auxiliary import SyntheticGeometryAuxiliaryRatio as AuxiliaryRatio
from sympy.geometry.synthetic.auxiliary import SyntheticGeometryAuxiliaryPoint as AuxiliaryPoint
from sympy.geometry.synthetic.quantities import SyntheticGeometryPythagorasDifference as Pythagoras
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedArea as Area
from sympy.geometry.synthetic.quantities import SyntheticGeometrySignedRatio as Ratio
from sympy.geometry.synthetic.ecs import PlaneECS1 as ECS1
from sympy.geometry.synthetic.ecs import PlaneECS5 as ECS5
from sympy.geometry.synthetic.ecs import PlaneECS6 as ECS6
from sympy.geometry.synthetic.ecs import PlaneECS7 as ECS7
from sympy.geometry.synthetic.ecs import PlaneECS8 as ECS8
from sympy.core.numbers import Rational, Integer


class _PlaneECSConverter:
    def __init__(self, prover):
        self.constructions = []
        self.prover = prover

    def prove(self, predicate):
        return self.prover(tuple(self.constructions), predicate)

    def append_PLine(self, W, U, V):
        N = AuxiliaryPoint(W, U, V)
        self.append_PRatio(N, W, U, V, Integer(1))
        return Line(W, N)

    def append_TLine(self, W, U, V):
        if self.prove(Collinear(W, U, V)) == True:
            if self.prove(Eqpoints(W, U)) == True:
                N = AuxiliaryPoint(W, V)
                self.constructions.append(TRatio(N, W, V, Integer(1)))
                return Line(N, W)

            N = AuxiliaryPoint(W, U)
            self.constructions.append(TRatio(N, W, U, Integer(1)))
            return Line(N, W)

        N = AuxiliaryPoint(W, U, V)
        self.constructions.append(Foot(N, W, U, V))
        return Line(N, W)

    def append_BLine(self, U, V):
        M = AuxiliaryPoint(U, V)
        self.append_Midpoint(M, U, V)
        N = AuxiliaryPoint(M, U)
        self.append_TRatio(N, M, U, Integer(1))
        return Line(N, M)

    def append_ALine(self, P, Q, W, U, V):
        if self.prove(Perpendicular(U, W, W, V)) == True:
            return TLine(P, P, Q)

        R = AuxiliaryPoint(Q, P)
        self.append_TRatio(R, Q, P, 4*Area(U, W, V)/Pythagoras(U, W, V))
        return Line(P, R)

    def append_LRatio(self, Y, U, V, r):
        return self.append_PRatio(Y, U, U, V, r)

    def append_PRatio(self, Y, W, U, V, r):
        self.constructions.append(PRatio(Y, W, U, V, r))

    def append_TRatio(self, Y, U, V, r):
        self.constructions.append(TRatio(Y, U, V, r))

    def append_Foot(self, Y, P, U, V):
        self.constructions.append(Foot(Y, P, U, V))

    def append_Midpoint(self, Y, U, V):
        return self.append_LRatio(Y, U, V, Rational(1, 2))

    def append_On_Line(self, Y, U, V):
        return self.append_LRatio(Y, U, V, AuxiliaryRatio(U, Y, U, V))

    def append_On_PLine(self, Y, W, U, V):
        return self.append_PRatio(Y, W, U, V, AuxiliaryRatio(W, Y, U, V))

    def append_ARatio(self, Y, O, U, V, r_o, r_u, r_v):
        self.constructions.append(ARatio(Y, O, U, V, r_o, r_u, r_v))

    def append_On(self, Y, L):
        if isinstance(L, Line):
            U, V = L.args
            return self.append_On_Line(Y, U, V)

        if isinstance(L, PLine):
            W, U, V = L.args
            return self.append_On_PLine(Y, W, U, V)

        if isinstance(L, TLine):
            W, U, V = L.args
            L = self.append_TLine(W, U, V)
            return self.append_On(Y, L)

        if isinstance(L, BLine):
            U, V = L.args
            L = self.append_BLine(U, V)
            return self.append_On(Y, L)

        if isinstance(L, Circle):
            O, P = L.args
            Q = AuxiliaryPoint(P)
            return self.append_Intersection(Y, Line(P, Q), Circle(O, P))

        raise NotImplementedError(f"Unknown On: {Y}, {L}")

    def append_Intersection_Line_Line(self, Y, U, V, P, Q):
        self.constructions.append(ECS1(Y, U, V, P, Q))

    def append_Intersection_Line_PLine(self, Y, U, V, R, P, Q):
        self.constructions.append(ECS5(Y, U, V, R, P, Q))

    def append_Intersection_Line_TLine(self, Y, U, V, R, P, Q):
        self.constructions.append(ECS6(Y, U, V, R, P, Q))

    def append_Intersection_Line_BLine(self, Y, U, V, P, Q):
        self.constructions.append(ECS7(Y, U, V, P, Q))

    def append_Intersection_Line_Circle(self, Y, U, V, O, P):
        self.constructions.append(ECS8(Y, U, V, O))

    def append_Intersection(self, Y, L1, L2):
        if isinstance(L1, Line) and isinstance(L2, Line):
            U, V = L1.args
            P, Q = L2.args
            return self.append_Intersection_Line_Line(Y, U, V, P, Q)

        if isinstance(L1, Line) and isinstance(L2, PLine):
            U, V = L1.args
            R, P, Q = L2.args
            return self.append_Intersection_Line_PLine(Y, U, V, R, P, Q)

        if isinstance(L1, PLine) and isinstance(L2, Line):
            U, V = L2.args
            R, P, Q = L1.args
            return self.append_Intersection_Line_PLine(Y, U, V, R, P, Q)

        if isinstance(L1, Line) and isinstance(L2, TLine):
            U, V = L1.args
            R, P, Q = L2.args
            return self.append_Intersection_Line_TLine(Y, U, V, R, P, Q)

        if isinstance(L1, TLine) and isinstance(L2, Line):
            U, V = L2.args
            R, P, Q = L1.args
            return self.append_Intersection_Line_TLine(Y, U, V, R, P, Q)

        if isinstance(L1, Line) and isinstance(L2, BLine):
            U, V = L1.args
            P, Q = L2.args
            return self.append_Intersection_Line_BLine(Y, U, V, P, Q)

        if isinstance(L1, BLine) and isinstance(L2, Line):
            U, V = L2.args
            P, Q = L1.args
            return self.append_Intersection_Line_BLine(Y, U, V, P, Q)

        if isinstance(L1, Line) and isinstance(L2, Circle):
            U, V = L1.args
            O, P = L2.args
            if P == U:
                return self.append_Intersection_Line_Circle(Y, U, V, O, P)
            if P == V:
                return self.append_Intersection_Line_Circle(Y, V, U, O, P)

        if isinstance(L1, Circle) and isinstance(L2, Circle):
            O1, P1 = L1.args
            O2, P2 = L2.args
            if P1 == P2:
                P = P1
                N = AuxiliaryPoint(P, O1, O2)
                self.append_Foot(N, P, O1, O2)
                return self.append_PRatio(Y, N, N, P, -Integer(1))

        if isinstance(L1, Circle):
            return self.append_Intersection(Y, L2, L1)

        if isinstance(L1, PLine):
            W, U, V = L1.args
            L1 = self.append_PLine(W, U, V)
            return self.append_Intersection(Y, L1, L2)

        if isinstance(L1, TLine):
            W, U, V = L1.args
            L1 = self.append_TLine(W, U, V)
            return self.append_Intersection(Y, L1, L2)

        if isinstance(L1, BLine):
            U, V = L1.args
            L1 = self.append_BLine(U, V)
            return self.append_Intersection(Y, L1, L2)

        if not isinstance(L1, ALine) and isinstance(L2, ALine):
            P, Q, W, U, V = L2.args
            L2 = self.append_ALine(P, Q, W, U, V)
            return self.append_Intersection(Y, L1, L2)

        if isinstance(L1, ALine):
            P, Q, W, U, V = L1.args
            L1 = self.append_ALine(P, Q, W, U, V)
            return self.append_Intersection(Y, L1, L2)

        raise NotImplementedError(f"Unknown Intersection: {Y}, {L1}, {L2}")

    def append(self, C):
        if isinstance(C, On):
            Y, L = C.args
            return self.append_On(Y, L)

        if isinstance(C, Intersection):
            Y, L1, L2 = C.args
            return self.append_Intersection(Y, L1, L2)

        if isinstance(C, Midpoint):
            Y, U, V = C.args
            return self.append_LRatio(Y, U, V, Rational(1, 2))

        if isinstance(C, Symmetry):
            Y, U, V = C.args
            return self.append_LRatio(Y, U, V, -Integer(1))

        if isinstance(C, Foot):
            Y, P, U, V = C.args
            return self.append_Foot(Y, P, U, V)

        if isinstance(C, PRatio):
            Y, W, U, V, r = C.args
            return self.append_PRatio(Y, W, U, V, r)

        if isinstance(C, LRatio):
            Y, U, V, r = C.args
            return self.append_LRatio(Y, U, V, r)

        if isinstance(C, MRatio):
            Y, U, V, r = C.args
            return self.append_LRatio(Y, U, V, r / (r + 1))

        if isinstance(C, TRatio):
            Y, U, V, r = C.args
            return self.append_TRatio(Y, U, V, r)

        if isinstance(C, Inversion):
            P, Q, O, A = C.args
            if self.prove(Collinear(Q, O, A)) == True:
                return self.append_LRatio(P, O, A, Ratio(O, A, O, Q))
            return self.append_LRatio(P, O, Q, Pythagoras(O, A, O) / Pythagoras(O, Q, O))

        if isinstance(C, ARatio):
            Y, O, U, V, r_o, r_u, r_v = C.args
            return self.append_ARatio(Y, O, U, V, r_o, r_u, r_v)

        if isinstance(C, Centroid):
            Y, A, B, C = C.args
            r_A = Rational(1, 3)
            r_B = Rational(1, 3)
            r_C = Rational(1, 3)
            return self.append_ARatio(Y, A, B, C, r_A, r_B, r_C)

        if isinstance(C, Orthocenter):
            Y, A, B, C = C.args
            r_A = Pythagoras(A, B, C)*Pythagoras(A, C, B) / (16*Area(A, B, C)**2)
            r_B = Pythagoras(B, A, C)*Pythagoras(B, C, A) / (16*Area(A, B, C)**2)
            r_C = Pythagoras(C, A, B)*Pythagoras(C, B, A) / (16*Area(A, B, C)**2)
            return self.append_ARatio(Y, A, B, C, r_A, r_B, r_C)

        if isinstance(C, Circumcenter):
            Y, A, B, C = C.args
            r_A = Pythagoras(B, C, B)*Pythagoras(B, A, C) / (32*Area(A, B, C)**2)
            r_B = Pythagoras(A, C, A)*Pythagoras(A, B, C) / (32*Area(A, B, C)**2)
            r_C = Pythagoras(A, B, A)*Pythagoras(A, C, B) / (32*Area(A, B, C)**2)
            return self.append_ARatio(Y, A, B, C, r_A, r_B, r_C)

        if isinstance(C, Incenter):
            C, I, A, B = C.args
            r_I = -2*Pythagoras(I, A, B)*Pythagoras(I, B, A) / (Pythagoras(A, I, B)*Pythagoras(A, B, A))
            r_A = Pythagoras(I, A, B)*Pythagoras(I, B, I) / (Pythagoras(A, I, B)*Pythagoras(A, B, A))
            r_B = Pythagoras(I, B, A)*Pythagoras(I, A, I) / (Pythagoras(A, I, B)*Pythagoras(A, B, A))
            return self.append_ARatio(C, I, A, B, r_I, r_A, r_B)

        raise NotImplementedError(f"Unknown construction: {C}")
