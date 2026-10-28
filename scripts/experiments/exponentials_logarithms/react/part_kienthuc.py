# -*- coding: utf-8 -*-
"""PART_KIENTHUC: foundational knowledge of the Exponential and Logarithm
chapter (Vietnamese high school curriculum). Identical for every problem
type of this chapter; it only grows when a new type needs a new fact."""

PART_KIENTHUC = r'''
**PART 1: FOUNDATIONAL KNOWLEDGE OF EXPONENTIALS AND LOGARITHMS**

1. **Powers**: for $a>0$ and real $m,n$: $a^m a^n=a^{m+n}$, $\dfrac{a^m}{a^n}=a^{m-n}$, $(a^m)^n=a^{mn}$, $(ab)^n=a^n b^n$, $a^{-n}=\dfrac{1}{a^n}$, $a^0=1$, and $a^{m/n}=\sqrt[n]{a^m}$.
2. **Exponential function** $y=a^x$ with $a>0$, $a\ne1$: it is defined for every real $x$, and $a^x>0$ always (it never equals 0 and is never negative). It is strictly increasing when $a>1$ and strictly decreasing when $0<a<1$.
3. **Exponential equations**: $a^{f}=a^{g}\iff f=g$. For a number $c$: $a^{f}=c$ has a solution only when $c>0$, and then $f=\log_a c$.
4. **Exponential inequalities** (same base): if $a>1$, then $a^{f}<a^{g}\iff f<g$ (direction kept). If $0<a<1$, then $a^{f}<a^{g}\iff f>g$ (direction reversed). In particular the sign of $a^{u}-a^{v}$ equals the sign of $u-v$ when $a>1$.
5. **Substitution $t=a^x$**: because $a^x>0$, the new variable must satisfy $t>0$. Then $a^{2x}=t^2$ and $a^{x+k}=a^k\,t$.
6. **Definition of the logarithm**: for $a>0$, $a\ne1$, $b>0$: $\log_a b=c\iff a^c=b$. The base must be positive and not equal to 1, and the argument must be strictly positive.
7. **Basic values**: $\log_a 1=0$, $\log_a a=1$, $\log_a a^c=c$, and $a^{\log_a b}=b$ for $b>0$.
8. **Product, quotient, power** (for $x,y>0$): $\log_a(xy)=\log_a x+\log_a y$, $\log_a\dfrac{x}{y}=\log_a x-\log_a y$, $\log_a x^{n}=n\log_a x$. For an even power of a number $x\ne0$ that may be negative: $\log_a x^{2k}=2k\log_a|x|$. Also $\log_{a^m}x=\dfrac{1}{m}\log_a x$ and $\log_a\sqrt[n]{x}=\dfrac{1}{n}\log_a x$.
9. **Change of base**: $\log_a b=\dfrac{\log_c b}{\log_c a}$ for any base $c>0$, $c\ne1$. Consequences: $\log_a b=\dfrac{1}{\log_b a}$ (for $b\ne1$) and $\log_a b\cdot\log_b c=\log_a c$.
10. **Natural and common logarithm**: $\ln x=\log_e x$ and $\log x=\log_{10}x$. In particular $\log_a b=\dfrac{\ln b}{\ln a}$.
11. **Exchanging base and exponent**: $a^{\log_b c}=c^{\log_b a}$ for $a,c>0$ and $b>0$, $b\ne1$. Reason: taking $\log_b$ of each side gives $\log_b c\cdot\log_b a$ on both sides, and two positive numbers with the same logarithm are equal.
12. **Logarithmic function** $y=\log_a x$: its domain is $x>0$. It is strictly increasing when $a>1$ and strictly decreasing when $0<a<1$. If $a>1$: $\log_a u<\log_a v\iff 0<u<v$ (direction kept). If $0<a<1$: $\log_a u<\log_a v\iff u>v>0$ (direction reversed). In both cases the arguments must be positive first.
13. **Logarithmic equations**: first state the domain (every argument $>0$). Then $\log_a f=\log_a g\iff f=g$, and $\log_a f=c\iff f=a^c$. A solution is accepted only if it satisfies the domain.
14. **Logarithmic inequalities with a constant**: if $a>1$: $\log_a f>c\iff f>a^c$ and $\log_a f<c\iff 0<f<a^c$. If $0<a<1$: $\log_a f>c\iff 0<f<a^c$ and $\log_a f<c\iff f>a^c$.
15. **Substitution $t=\log_a x$**: here $x>0$ and $t$ can be any real number. Then $\log_a^2 x=t^2$ and $x=a^t$.
16. **Always find the domain first**: every logarithm argument $>0$, every base positive and not 1, every denominator $\ne0$, every expression under a square root $\ge0$. Any value found later is accepted only if it satisfies this domain.
17. **Sign of a difference of two logarithms** (base $a>1$, arguments $u,v>0$): the sign of $\log_a u-\log_a v$ equals the sign of $u-v$. In particular $\log_a u-\log_a v=0\iff u=v$.
18. **Products and square roots**: $A\cdot B=0$ means $A=0$ or $B=0$. For $A\cdot\sqrt{B}=0$: either $A=0$ (and then $B\ge0$ must hold so that the square root exists), or $B=0$. The sign of a product $A\cdot B$ is decided by the signs of its two factors: $A\cdot B\le 0$ means one factor is $\ge0$ and the other is $\le0$.
19. **Derivatives**: $(a^x)'=a^x\ln a$, $(e^x)'=e^x$, $(a^u)'=u'\,a^u\ln a$. Also $(\log_a x)'=\dfrac{1}{x\ln a}$, $(\ln x)'=\dfrac{1}{x}$, $(\log_a u)'=\dfrac{u'}{u\ln a}$, and for a quotient $\left(\dfrac{u}{v}\right)'=\dfrac{u'v-uv'}{v^2}$.
20. **Derivative and monotonicity**: if $f'(x)>0$ on an interval, $f$ is strictly increasing there; if $f'(x)<0$, it is strictly decreasing. A strictly increasing function satisfies $f(u)<f(v)\iff u<v$ and $f(u)=f(v)\iff u=v$, so the equation $f=k$ has at most one solution.
21. **A power function with exponent above 1**: if $\alpha>1$ then $f(t)=t^{\alpha}-t$ has $f'(t)=\alpha t^{\alpha-1}-1$, and for $t\ge1$ we get $t^{\alpha-1}\ge1$, so $f'(t)\ge\alpha-1>0$: $f$ is strictly increasing on $[1,+\infty)$.
22. **Comparing the bases**: if $a>b>1$ then $\log_b a=\dfrac{\ln a}{\ln b}>1$.
23. **Integers**: a sum or difference of integers is an integer, and a positive integer is at least 1. Different integer values of $t$ give different values of $y=t-x$ for a fixed integer $x$, so counting the integers $y$ is the same as counting the integers $t$.
24. **Counting integers**: for real numbers $p<q$, the number of integers strictly between them (open interval $(p,q)$) is $(\lceil q\rceil-1)-(\lfloor p\rfloor+1)+1=\lceil q\rceil-\lfloor p\rfloor-1$. The number of integers in the closed interval $[p,q]$ is $\lfloor q\rfloor-\lceil p\rceil+1$. Here $\lfloor u\rfloor$ is the greatest integer not above $u$ and $\lceil u\rceil$ is the least integer not below $u$. The integers $1,2,\dots,T$ are exactly $T$ numbers.
25. **Quadratic equation** $ax^2+bx+c=0$ ($a\ne0$): $\Delta=b^2-4ac$. If $\Delta>0$ there are two distinct real roots $x_{1,2}=\dfrac{-b\pm\sqrt{\Delta}}{2a}$; if $\Delta=0$ one double root; if $\Delta<0$ no real root. Viète: $x_1+x_2=-\dfrac{b}{a}$ and $x_1x_2=\dfrac{c}{a}$.
26. **Quadratic inequality**: for $a>0$ and $\Delta>0$ with roots $x_1<x_2$: $ax^2+bx+c<0\iff x_1<x<x_2$, and $ax^2+bx+c>0\iff x<x_1$ or $x>x_2$. The two roots themselves are included only for the non strict signs $\le$ and $\ge$.
27. **Two distinct positive roots**: the quadratic $at^2+bt+c=0$ has two distinct positive roots if and only if $\Delta>0$, $x_1+x_2>0$ and $x_1x_2>0$.
28. **Squares and square roots**: $\sqrt{u^2}=|u|$. For $k>0$: $x^2<k\iff-\sqrt{k}<x<\sqrt{k}$ and $x^2>k\iff x<-\sqrt{k}$ or $x>\sqrt{k}$.
29. **Inequality of the arithmetic and geometric means**: for $u,v\ge0$: $u+v\ge2\sqrt{uv}$, with equality if and only if $u=v$.
30. **Bunyakovsky inequality** (also called Cauchy and Schwarz): for real numbers $p,q,x,y$: $(px+qy)^2\le(p^2+q^2)(x^2+y^2)$, with equality if and only if $(p,q)$ and $(x,y)$ are proportional.
31. **Values of a continuous monotone function**: if $f$ is continuous and strictly increasing on $[p,q]$, then on the open interval $(p,q)$ it takes every value strictly between $f(p)$ and $f(q)$ exactly once, and no other value. So $f(x)=k$ has a solution in $(p,q)$ if and only if $f(p)<k<f(q)$. For a strictly decreasing $f$ the roles of $f(p)$ and $f(q)$ swap.
32. **Behaviour at the ends** (base $a>1$): $a^x\to0^+$ when $x\to-\infty$ and $a^x\to+\infty$ when $x\to+\infty$; $\ln x\to-\infty$ when $x\to0^+$ and $\ln x\to+\infty$ when $x\to+\infty$. A function that goes from $-\infty$ up to a local maximum, down to a local minimum, then up to $+\infty$ crosses the $x$ axis 3 times if the maximum is positive and the minimum is negative, and once otherwise.
33. **Quadratic in $t=a^x>0$**: the roots of $t^2+Bt+D=0$ are accepted only if they are positive. If $D<0$ the roots have opposite signs, and $t^2+Bt+D>0$ with $t>0$ means $t$ above the larger root. A negative sign in front of a number is part of the number: for example in $t^2-12t+35$ we have $B=-12$.
'''
