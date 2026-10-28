# -*- coding: utf-8 -*-
"""Problem type D79: count the integers x such that, for each such x, there
are at most N integers y satisfying log_a(x^2+y) >= log_b(x+y), with a > b > 1.

The method (PART_HUONGGIAI) is the one written by the author of the thesis,
translated faithfully into English. PART_TOOL and PART_KIENTHUC are shared
with every other problem type of the chapter and live in their own files.
"""

MA_DANG = "D79"
FREE_UNKNOWNS = {"x"}

# ---------------------------------------------------------------------------
# PART 2: lecture on WHY the method works (continuous prose, no checklist)
# ---------------------------------------------------------------------------
PART_HUONGGIAI = r'''
**PART 2: THE SOLUTION METHOD FOR THIS PROBLEM TYPE**

Problem shape: the problem gives two logarithms with different bases $a>b>1$ and a bound $N$, and asks how many integers $x$ have the following property: for this $x$, there are at most $N$ integers $y$ satisfying $\log_a(x^2+y)\ge\log_b(x+y)$.

**Domain.** Both logarithms need a positive argument, so we need $x+y>0$ and $x^2+y>0$. The numbers $x$ and $y$ are integers, so $x+y$ is an integer, and a positive integer is at least 1. The first condition therefore says $x+y\ge1$.

**A new variable that separates $x$ from $y$.** The two arguments share the sum $x+y$, so we give it a name: $t=x+y$, an integer with $t\ge1$. From $y=t-x$, the other argument becomes $x^2+y=x^2-x+t$. The inequality is now $\log_a(x^2-x+t)\ge\log_b t$.

**Separating the two variables.** The aim is to have only $x$ on one side and only $t$ on the other. Since $a>1$, the function $u\mapsto a^u$ is strictly increasing, so raising $a$ to both sides keeps the direction of the inequality: $x^2-x+t\ge a^{\log_b t}$. The power on the right has $t$ inside the exponent, and exchanging base and exponent turns it into $a^{\log_b t}=t^{\log_b a}$. Moving $t$ to the right side gives
$$x^2-x\ \ge\ t^{\log_b a}-t.$$
Now $x$ appears only on the left and $t$ only on the right.

**Studying the right side.** Let $f(t)=t^{\log_b a}-t$. Because $a>b>1$, the exponent $\log_b a$ is greater than 1, so $f'(t)=\log_b a\cdot t^{\log_b a-1}-1\ge\log_b a-1>0$ for $t\ge1$. Hence $f$ is strictly increasing on $[1,+\infty)$: as $t$ takes the values $1,2,3,\dots$, the value $f(t)$ only grows.

**Turning "at most $N$ values of $y$" into a condition on $x$.** For a fixed integer $x$, each integer $t\ge1$ gives exactly one integer $y=t-x$, so counting the integers $y$ is the same as counting the integers $t$ with $f(t)\le x^2-x$. Because $f$ increases, these values of $t$ form an unbroken run $1,2,\dots,T$: once $f(t)$ rises above $x^2-x$, it stays above. This run has at most $N$ members exactly when the next integer $N+1$ already breaks the inequality, that is when $f(N+1)>x^2-x$. Indeed, if $N+1$ fails, every larger integer fails as well; and if $N+1$ does not fail, the run reaches at least $N+1$ and has too many members. So the property required of $x$ is
$$x^2-x<f(N+1).$$

**Conclusion.** Putting $N+1$ into $f$ gives one definite real number $C=f(N+1)=(N+1)^{\log_b a}-(N+1)$. The condition on $x$ becomes $x^2-x-C<0$. This quadratic has a positive leading coefficient and two real roots $x_1<x_2$ (its discriminant $1+4C$ is positive), so it is negative exactly for $x_1<x<x_2$. Since $x$ is an integer, the answer is the number of integers strictly between $x_1$ and $x_2$. This count is then compared with the four options.
'''

# ---------------------------------------------------------------------------
# PART 3: worked example (steps; the Observations are produced by running the
# real Calculator backend when the notebook is built)
# ---------------------------------------------------------------------------
EXAMPLE_QUESTION = (
    "Có bao nhiêu số nguyên $x$ sao cho ứng với mỗi $x$ có không quá 120 số nguyên $y$ "
    "thỏa mãn $\\log_{7}(x^2+y)\\ge \\log_{5}(x+y)$?\n"
    "\n"
    "A. $27$.\n"
    "B. $29$.\n"
    "C. $28$.\n"
    "D. $30$."
)
EXAMPLE_ANSWER = "C"
# independent brute force over the original inequality: 28 integers x.
EXAMPLE_COUNT = 28

EXAMPLE_INTRO = ""   # the forced prefix already starts the trace with "Thought:"

EXAMPLE_STEPS = [
    # (thought, action_input or None)
    ("I read the problem. The first logarithm is $\\log_7(x^2+y)$, so its base is 7; the second is $\\log_5(x+y)$, so its base is 5; and the bound is 120 integers $y$. The method says the decisive integer is the bound plus 1, the first value of $t$ that must fail, so I ask the Calculator for it first.",
     "n_plus_1 = 120 + 1"),
    ("After the substitution $t=x+y$ the inequality became $x^2-x\\ge t^{\\log_5 7}-t$, so the exponent I need is $\\log_5 7$, the base of the first logarithm written as a logarithm to the base of the second. The Calculator only has natural logarithms, so I use the change of base formula $\\log(7)/\\log(5)$.",
     "exponent = log(7)/log(5)"),
    ("Now the threshold $C=f(121)=121^{\\log_5 7}-121$. I need it as a decimal, because the next step must locate two roots between consecutive integers, so I wrap the expression in N with 20 digits.",
     "threshold = N(n_plus_1**exponent - n_plus_1, 20)"),
    ("The condition on $x$ is $x^2-x<C$, so I solve the quadratic equation $x^2-x-C=0$. Its leading coefficient is positive, so the inequality will hold strictly between the two roots.",
     "x_roots = solve(x**2 - x - threshold, x)"),
    ("The solver may list the two roots in either order, so I do not rely on their positions. I store the smaller root by taking the minimum of the two.",
     "x_low = Min(x_roots[0], x_roots[1])"),
    ("Now the larger root, taking the maximum of the two.",
     "x_high = Max(x_roots[0], x_roots[1])"),
    ("The integers $x$ must satisfy $x_{low}<x<x_{high}$ strictly. The first integer strictly above $x_{low}$ is the floor of $x_{low}$ plus 1; this stays correct even if $x_{low}$ were itself an integer, because that value would then be excluded.",
     "first_x = floor(x_low) + 1"),
    ("The last integer strictly below $x_{high}$ is the ceiling of $x_{high}$ minus 1, for the same reason.",
     "last_x = ceiling(x_high) - 1"),
    ("The integers from first_x to last_x inclusive are last_x minus first_x plus 1 numbers, and this is the number of valid $x$.",
     "count = last_x - first_x + 1"),
    ("The count is stored. Before testing anything, I copy all four options exactly as they are written in the problem, side by side: A: 27, B: 29, C: 28, D: 30. I will test each of them against the count, one call per option, and read each result next to the option I copied here.",
     None),
    ("Option A is 27.",
     "test_A = Eq(count, 27)"),
    ("Option B is 29.",
     "test_B = Eq(count, 29)"),
    ("Option C is 28.",
     "test_C = Eq(count, 28)"),
    ("Option D is 30.",
     "test_D = Eq(count, 30)"),
    ("Lining up what I copied with the stored results: A: 27 gives False, B: 29 gives False, C: 28 gives True, D: 30 gives False. Exactly one option matches, and it is C.",
     None),
]

# ---------------------------------------------------------------------------
# PART 4: step by step task list for this problem type
# ---------------------------------------------------------------------------
PART_NHIEMVU = r'''
**PART 4: YOUR TURN**

Open a `<think>` tag as the very first thing you write, and close it with `</think>`. Think in English inside the tags. Work through the method of PART 2, and use a Calculator call for every computation; never compute anything yourself:

[Step 1] Read the problem and write down, without computing: the base $a$ of the first logarithm $\log_a(x^2+y)$, the base $b$ of the second logarithm $\log_b(x+y)$, and the bound, which is the number in the phrase "at most ... integers $y$".
[Step 2] Store `n_plus_1 = <the bound> + 1`, writing the number from the problem in place of `<the bound>`.
[Step 3] Store `exponent = log(a)/log(b)`, writing the two bases from the problem. This is $\log_b a$ by the change of base formula.
[Step 4] Store `threshold = N(n_plus_1**exponent - n_plus_1, 20)`. This is the real number $C=f(N+1)$.
[Step 5] Store `x_roots = solve(x**2 - x - threshold, x)`.
[Step 6] Store `x_low = Min(x_roots[0], x_roots[1])` and then `x_high = Max(x_roots[0], x_roots[1])`.
[Step 7] Store `first_x = floor(x_low) + 1`, then `last_x = ceiling(x_high) - 1`, then `count = last_x - first_x + 1`.
[Step 8] Copy all four options side by side in one Thought. Then test every option in order with `test_A = Eq(count, <option A>)`, then `test_B`, `test_C`, `test_D` in the same way. Finally line up each copied option next to its stored result; exactly one of them is `True`. Do not pick the letter by eye.

Then, immediately after `</think>`, write exactly:
Final Answer: \boxed{<Letter>}

Đề bài:
{de_bai}
'''
