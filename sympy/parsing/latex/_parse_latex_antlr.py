# Ported from latex2sympy by @augustt198
# https://github.com/augustt198/latex2sympy
# See license in LICENSE.txt

import sympy
from sympy.external import import_module
from sympy.printing.str import StrPrinter

from .errors import LaTeXParsingError


LaTeXParser = LaTeXLexer = MathErrorListener = None

try:
    LaTeXParser = import_module('sympy.parsing.latex._antlr.latexparser',
                                import_kwargs={'fromlist': ['LaTeXParser']}).LaTeXParser
    LaTeXLexer = import_module('sympy.parsing.latex._antlr.latexlexer',
                               import_kwargs={'fromlist': ['LaTeXLexer']}).LaTeXLexer
except Exception:
    pass

ErrorListener = import_module('antlr4.error.ErrorListener',
                              warn_not_installed=True,
                              import_kwargs={'fromlist': ['ErrorListener']}
                              )



if ErrorListener:
    class MathErrorListener(ErrorListener.ErrorListener):  # type: ignore
        def __init__(self, src):
            super(ErrorListener.ErrorListener, self).__init__()
            self.src = src

        def syntaxError(self, recog, symbol, line, col, msg, e):
            fmt = "%s\n%s\n%s"
            marker = "~" * col + "^"

            if msg.startswith("missing"):
                err = fmt % (msg, self.src, marker)
            elif msg.startswith("no viable"):
                err = fmt % ("I expected something else here", self.src, marker)
            elif msg.startswith("mismatched"):
                names = LaTeXParser.literalNames
                expected = [
                    names[i] for i in e.getExpectedTokens() if i < len(names)
                ]
                if len(expected) < 10:
                    expected = " ".join(expected)
                    err = (fmt % ("I expected one of these: " + expected, self.src,
                                  marker))
                else:
                    err = (fmt % ("I expected something else here", self.src,
                                  marker))
            else:
                err = fmt % ("I don't understand this", self.src, marker)
            raise LaTeXParsingError(err)


def parse_latex(sympy):
    antlr4 = import_module('antlr4', warn_not_installed=True)

    if None in [antlr4, MathErrorListener]:
        raise ImportError("LaTeX parsing requires the antlr4 python package,"
                          " provided by pip (antlr4-python2-runtime or"
                          " antlr4-python3-runtime) or"
                          " conda (antlr-python-runtime)")

    matherror = MathErrorListener(sympy)

    stream = antlr4.InputStream(sympy)
    lex = LaTeXLexer(stream)
    lex.removeErrorListeners()
    lex.addErrorListener(matherror)

    tokens = antlr4.CommonTokenStream(lex)
    parser = LaTeXParser(tokens)

    # remove default console error listener
    parser.removeErrorListeners()
    parser.addErrorListener(matherror)

    expr = parser.math().expr()
    return convert_expr(expr)


def convert_relation(rel):
    if rel.expr():
        return convert_expr(rel.expr())

    lh = convert_relation(rel.relation(0))
    rh = convert_relation(rel.relation(1))
    if rel.LT():
        return sympy.StrictLessThan(lh, rh)
    elif rel.LTE():
        return sympy.LessThan(lh, rh)
    elif rel.GT():
        return sympy.StrictGreaterThan(lh, rh)
    elif rel.GTE():
        return sympy.GreaterThan(lh, rh)
    elif rel.EQUAL():
        return sympy.Eq(lh, rh)


def convert_expr(expr):
    if isinstance(expr, LaTeXParser.FactorialContext):
        return convert_factorial(expr)
    if isinstance(expr, LaTeXParser.PowContext):
        return convert_pow(expr)
    if isinstance(expr, LaTeXParser.MulContext):
        return convert_mul(expr)
    if isinstance(expr, LaTeXParser.DivContext):
        return convert_div(expr)

    if isinstance(expr, LaTeXParser.AddContext):
        return convert_add(expr)
    if isinstance(expr, LaTeXParser.SubContext):
        return convert_sub(expr)

    if isinstance(expr, LaTeXParser.EqualsContext):
        return convert_eq(expr)
    if isinstance(expr, LaTeXParser.LessEqualContext):
        return convert_le(expr)
    if isinstance(expr, LaTeXParser.LessThanContext):
        return convert_lt(expr)
    if isinstance(expr, LaTeXParser.GreaterEqualContext):
        return convert_ge(expr)
    if isinstance(expr, LaTeXParser.GreaterThanContext):
        return convert_gt(expr)

    if isinstance(expr, LaTeXParser.SpecialsContext):
        return convert_special(expr.special())
    if isinstance(expr, LaTeXParser.ImplicitMulContext):
        return convert_mul(expr)


def convert_factorial(expr):
    expr = convert_expr(expr.expr())
    return sympy.factorial(expr, evaluate=False)


def convert_pow(expr):
    base, exp = expr.base, expr.exp
    base, exp = convert_expr(base), convert_expr(exp)
    return sympy.Pow(base, exp, evaluate=False)


def convert_mul(expr):
    lhs, rhs = expr.lhs, expr.rhs
    lhs, rhs = convert_expr(lhs), convert_expr(rhs)
    return sympy.Mul(lhs, rhs, evaluate=False)


def convert_div(expr):
    lhs, rhs = expr.lhs, expr.rhs
    lhs, rhs = convert_expr(lhs), convert_expr(rhs)
    rhs = sympy.Pow(rhs, -1, evaluate=False)
    return sympy.Mul(lhs, rhs, evaluate=False)


def convert_add(expr):
    lhs, rhs = expr.lhs, expr.rhs
    lhs, rhs = convert_expr(lhs), convert_expr(rhs)
    return sympy.Add(lhs, rhs, evaluate=False)


def convert_sub(expr):
    lhs, rhs = expr.lhs, expr.rhs
    lhs, rhs = convert_expr(lhs), convert_expr(rhs)
    rhs = sympy.Mul(-1, rhs, evaluate=False)
    return sympy.Add(lhs, rhs, evaluate=False)


def convert_rel(expr, rel_op):
    lhs, rhs = expr.lhs, expr.rhs
    lhs, rhs = convert_expr(lhs), convert_expr(rhs)
    return rel_op(lhs, rhs, evaluate=False)


convert_eq = lambda expr: convert_rel(expr, sympy.Eq)
convert_le = lambda expr: convert_rel(expr, sympy.Le)
convert_lt = lambda expr: convert_rel(expr, sympy.Lt)
convert_ge = lambda expr: convert_rel(expr, sympy.Ge)
convert_gt = lambda expr: convert_rel(expr, sympy.Gt)


def convert_special(special):
    if special.unary_add():
        return convert_unary_add(special.unary_add())
    if special.unary_sub():
        return convert_unary_sub(special.unary_sub())
    if special.paren():
        return convert_paren(special.paren())
    if special.atom():
        return convert_atom(special.atom())
    if special.log():
        return convert_log(special.log())
    if special.sqrt():
        return convert_sqrt(special.sqrt())
    if special.amsmath_func():
        return convert_amsmath_func(special.amsmath_func())
    if special.user_func():
        return convert_user_func(special.user_func())
    if special.frac():
        return convert_frac(special.frac())
    if special.limit():
        return convert_limit(special.limit())
    if special.derivative():
        return convert_derivative(special.derivative())
    if special.absolute():
        return convert_abs(special.absolute())
    if special.integral():
        return convert_integral(special.integral())

def convert_unary_add(unary):
    return convert_expr(unary.expr())


def convert_unary_sub(unary):
    return sympy.Mul(-1, convert_expr(unary.expr()), evaluate=False)


def convert_paren(paren):
    return convert_expr(paren.expr())


def convert_abs(expr):
    expr = convert_expr(expr.expr())
    return sympy.Abs(expr, evaluate=False)


def convert_sqrt(sqrt):
    root = sympy.S.One * 2
    if sqrt.root:
        root = sqrt.root
        root = convert_expr(root)
    base = sqrt.base
    base = convert_expr(base)
    return sympy.Pow(base, sympy.S.One/root, evaluate=False)


def convert_log(log):
    base = sympy.Integer(10)
    if log.base:
        base = convert_subexpr(log.base)
    exp = None
    if log.exp:
        exp = convert_supexpr(log.exp)

    if log.func_arg_noparens():
        arg = convert_special(log.func_arg_noparens().special())
    elif log.func_arg_parens():
        arg = convert_expr(log.func_arg_parens().expr())

    result = sympy.log(arg, base, evaluate=False)
    if exp is not None:
        return sympy.Pow(result, exp, evaluate=False)
    return result


def convert_amsmath_func(func):
    exp = None
    if func.exp:
        exp = convert_supexpr(func.exp)

    if func.func_arg_noparens():
        arg = convert_special(func.func_arg_noparens().special())
    elif func.func_arg_parens():
        arg = convert_expr(func.func_arg_parens().expr())

    sympy_func = convert_func_normal(func.func_normal())
    result = sympy_func(arg)
    if exp is not None:
        return sympy.Pow(result, exp, evaluate=False)
    return result


def convert_func_normal(func_normal):
    if func_normal.FUNC_EXP():
        return sympy.exp
    if func_normal.FUNC_LN():
        return sympy.log

    if func_normal.FUNC_SIN():
        return sympy.sin
    if func_normal.FUNC_COS():
        return sympy.cos
    if func_normal.FUNC_TAN():
        return sympy.tan

    if func_normal.FUNC_CSC():
        return sympy.csc
    if func_normal.FUNC_SEC():
        return sympy.sec
    if func_normal.FUNC_COT():
        return sympy.cot

    if func_normal.FUNC_ARCSIN():
        return sympy.asin
    if func_normal.FUNC_ARCCOS():
        return sympy.acos
    if func_normal.FUNC_ARCTAN():
        return sympy.atan

    if func_normal.FUNC_ARCCSC():
        return sympy.acsc
    if func_normal.FUNC_ARCSEC():
        return sympy.asec
    if func_normal.FUNC_ARCCOT():
        return sympy.acot

    if func_normal.FUNC_SINH():
        return sympy.sinh
    if func_normal.FUNC_COSH():
        return sympy.cosh
    if func_normal.FUNC_TANH():
        return sympy.tanh

    if func_normal.FUNC_ARSINH():
        return sympy.asinh
    if func_normal.FUNC_ARCOSH():
        return sympy.acosh
    if func_normal.FUNC_ARTANH():
        return sympy.atanh


def convert_subsupexpr(expr):
    if expr.expr():
        return convert_expr(expr.expr())
    elif expr.atom():
        return convert_atom(expr.atom())

convert_subexpr = convert_subsupexpr
convert_supexpr = convert_subsupexpr


def convert_user_func(func):
    name = func.user_func_name()
    args = func.user_func_args()
    func = sympy.Function(name.getText())
    args = (convert_expr(x) for x in args.expr())
    return func(*args, evaluate=False)


def convert_frac(frac):
    upper, lower = frac.upper, frac.lower
    if upper.getText() == '1':
        lower = convert_expr(lower)
        return sympy.Pow(lower, -1, evaluate=False)
    upper, lower = convert_expr(upper), convert_expr(lower)
    lower = sympy.Pow(lower, -1, evaluate=False)
    return sympy.Mul(upper, lower, evaluate=False)


def convert_limit(limit):
    content = convert_expr(limit.expr())
    limit_sub = limit.limit_sub()
    var = convert_expr(limit_sub.var)
    approaching = convert_expr(limit_sub.approaching)

    direction = '+-'
    if limit_sub.limit_left():
        direction = '+'
    elif limit_sub.limit_right():
        direction = '-'

    return sympy.Limit(content, var, approaching, direction)


def convert_derivative(diff):
    if diff.derivative_type_1():
        diff = diff.derivative_type_1()
    elif diff.derivative_type_2():
        diff = diff.derivative_type_2()
    upper, lower = diff.upper, diff.lower
    upper, lower = convert_expr(upper), convert_expr(lower)
    return sympy.Derivative(upper, lower)


def convert_integral(integral):
    if integral.integral_indefinite():
        integral = integral.integral_indefinite()
        expr, wrt = convert_integrand(integral.integrand())
        return sympy.Integral(expr, wrt)
    elif integral.integral_definite():
        integral = integral.integral_definite()
        expr, wrt = convert_integrand(integral.integrand())
        start, stop = integral.subexpr(), integral.supexpr()
        start = convert_subexpr(start)
        stop = convert_supexpr(stop)
        return sympy.Integral(expr, (wrt, start, stop))


def convert_integrand(integrand):
    if integrand.differential():
        return convert_differential(integrand.differential())
    elif integrand.differential_frac():
        differential_frac = integrand.differential_frac()
        expr, wrt = convert_differential(differential_frac.differential())
        lower = differential_frac.differential_denom
        lower = convert_expr(lower)
        if expr is sympy.S.One:
            expr = sympy.Pow(lower, -1, evaluate=False)
        else:
            lower = sympy.Pow(lower, -1, evaluate=False)
            expr = sympy.Mul(expr, lower, evaluate=False)
        return expr, wrt


def convert_differential(differential):
    expr = sympy.S.One
    if differential.differential_numer:
        expr = convert_expr(differential.differential_numer)

    wrt = differential.wrt
    wrt = convert_expr(wrt)
    return expr, wrt


def convert_postfix_list(arr, i=0):
    if i >= len(arr):
        raise LaTeXParsingError("Index out of bounds")

    res = convert_postfix(arr[i])
    if isinstance(res, sympy.Expr):
        if i == len(arr) - 1:
            return res  # nothing to multiply by
        else:
            if i > 0:
                left = convert_postfix(arr[i - 1])
                right = convert_postfix(arr[i + 1])
                if isinstance(left, sympy.Expr) and isinstance(
                        right, sympy.Expr):
                    left_syms = convert_postfix(arr[i - 1]).atoms(sympy.Symbol)
                    right_syms = convert_postfix(arr[i + 1]).atoms(
                        sympy.Symbol)
                    # if the left and right sides contain no variables and the
                    # symbol in between is 'x', treat as multiplication.
                    if len(left_syms) == 0 and len(right_syms) == 0 and str(
                            res) == "x":
                        return convert_postfix_list(arr, i + 1)
            # multiply by next
            return sympy.Mul(
                res, convert_postfix_list(arr, i + 1), evaluate=False)
    else:  # must be derivative
        wrt = res[0]
        if i == len(arr) - 1:
            raise LaTeXParsingError("Expected expression for derivative")
        else:
            expr = convert_postfix_list(arr, i + 1)
            return sympy.Derivative(expr, wrt)


def do_subs(expr, at):
    if at.expr():
        at_expr = convert_expr(at.expr())
        syms = at_expr.atoms(sympy.Symbol)
        if len(syms) == 0:
            return expr
        elif len(syms) > 0:
            sym = next(iter(syms))
            return expr.subs(sym, at_expr)
    elif at.equality():
        lh = convert_expr(at.equality().expr(0))
        rh = convert_expr(at.equality().expr(1))
        return expr.subs(lh, rh)


def convert_postfix(postfix):
    if hasattr(postfix, 'exp'):
        exp_nested = postfix.exp()
    else:
        exp_nested = postfix.exp_nofunc()

    exp = convert_exp(exp_nested)
    for op in postfix.postfix_op():
        if op.BANG():
            if isinstance(exp, list):
                raise LaTeXParsingError("Cannot apply postfix to derivative")
            exp = sympy.factorial(exp, evaluate=False)
        elif op.eval_at():
            ev = op.eval_at()
            at_b = None
            at_a = None
            if ev.eval_at_sup():
                at_b = do_subs(exp, ev.eval_at_sup())
            if ev.eval_at_sub():
                at_a = do_subs(exp, ev.eval_at_sub())
            if at_b is not None and at_a is not None:
                exp = sympy.Add(at_b, -1 * at_a, evaluate=False)
            elif at_b is not None:
                exp = at_b
            elif at_a is not None:
                exp = at_a

    return exp


def convert_exp(exp):
    if hasattr(exp, 'exp'):
        exp_nested = exp.exp()
    else:
        exp_nested = exp.exp_nofunc()

    if exp_nested:
        base = convert_exp(exp_nested)
        if isinstance(base, list):
            raise LaTeXParsingError("Cannot raise derivative to power")
        if exp.atom():
            exponent = convert_atom(exp.atom())
        elif exp.expr():
            exponent = convert_expr(exp.expr())
        return sympy.Pow(base, exponent, evaluate=False)
    else:
        if hasattr(exp, 'comp'):
            return convert_comp(exp.comp())
        else:
            return convert_comp(exp.comp_nofunc())


def convert_comp(comp):
    if comp.group():
        return convert_expr(comp.group().expr())
    elif comp.abs_group():
        return sympy.Abs(convert_expr(comp.abs_group().expr()), evaluate=False)
    elif comp.atom():
        return convert_atom(comp.atom())
    elif comp.frac():
        return convert_frac(comp.frac())
    elif comp.binom():
        return convert_binom(comp.binom())
    elif comp.func():
        return convert_func(comp.func())


def convert_atom(atom):
    if atom.LETTER():
        subscriptName = ''
        if atom.subexpr():
            subscript = None
            if atom.subexpr().expr():  # subscript is expr
                subscript = convert_expr(atom.subexpr().expr())
            else:  # subscript is atom
                subscript = convert_atom(atom.subexpr().atom())
            subscriptName = '_{' + StrPrinter().doprint(subscript) + '}'
        return sympy.Symbol(atom.LETTER().getText() + subscriptName)
    elif atom.SYMBOL():
        s = atom.SYMBOL().getText()[1:]
        if s == "infty":
            return sympy.oo
        else:
            if atom.subexpr():
                subscript = None
                if atom.subexpr().expr():  # subscript is expr
                    subscript = convert_expr(atom.subexpr().expr())
                else:  # subscript is atom
                    subscript = convert_atom(atom.subexpr().atom())
                subscriptName = StrPrinter().doprint(subscript)
                s += '_{' + subscriptName + '}'
            return sympy.Symbol(s)
    elif atom.NUMBER():
        s = atom.NUMBER().getText().replace(",", "")
        return sympy.Number(s)
    elif atom.mathit():
        text = rule2text(atom.mathit().mathit_text())
        return sympy.Symbol(text)


def rule2text(ctx):
    stream = ctx.start.getInputStream()
    # starting index of starting token
    startIdx = ctx.start.start
    # stopping index of stopping token
    stopIdx = ctx.stop.stop

    return stream.getText(startIdx, stopIdx)


def convert_binom(binom):
    expr_n = convert_expr(binom.n)
    expr_k = convert_expr(binom.k)
    return sympy.binomial(expr_n, expr_k, evaluate=False)

def convert_func(func):
    if func.LETTER() or func.SYMBOL():
        if func.LETTER():
            fname = func.LETTER().getText()
        elif func.SYMBOL():
            fname = func.SYMBOL().getText()[1:]
        fname = str(fname)  # can't be unicode
        if func.subexpr():
            subscript = None
            if func.subexpr().expr():  # subscript is expr
                subscript = convert_expr(func.subexpr().expr())
            else:  # subscript is atom
                subscript = convert_atom(func.subexpr().atom())
            subscriptName = StrPrinter().doprint(subscript)
            fname += '_{' + subscriptName + '}'
        input_args = func.args()
        output_args = []
        while input_args.args():  # handle multiple arguments to function
            output_args.append(convert_expr(input_args.expr()))
            input_args = input_args.args()
        output_args.append(convert_expr(input_args.expr()))
        return sympy.Function(fname)(*output_args)
    elif func.FUNC_SUM():
        return handle_sum_or_prod(func, "summation")
    elif func.FUNC_PROD():
        return handle_sum_or_prod(func, "product")


def handle_sum_or_prod(func, name):
    val = convert_mp(func.mp())
    iter_var = convert_expr(func.subeq().equality().expr(0))
    start = convert_expr(func.subeq().equality().expr(1))
    if func.supexpr().expr():  # ^{expr}
        end = convert_expr(func.supexpr().expr())
    else:  # ^atom
        end = convert_atom(func.supexpr().atom())

    if name == "summation":
        return sympy.Sum(val, (iter_var, start, end))
    elif name == "product":
        return sympy.Product(val, (iter_var, start, end))
