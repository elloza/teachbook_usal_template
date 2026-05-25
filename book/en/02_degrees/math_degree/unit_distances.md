# Planar Point Sets with Many Unit Distances

This page explains the manuscript *Planar Point Sets with Many Unit Distances* {cite:p}`openai2026planarunitdistances` from the perspective of a mathematics course. The goal is not to reproduce every technical detail from algebraic number theory, but to make the architecture of the proof clear: an arithmetic construction in number fields eventually produces finite planar point sets with many pairs at distance exactly one.

## The Unit-Distance Problem

Let $P \subset \mathbb{R}^2$ be a finite point set. Define

$$
\nu(P)=\#\bigl\{\{p,q\}\subset P:\lVert p-q\rVert_2=1\bigr\},
$$

the number of unordered pairs of points of $P$ at Euclidean distance one. Also define

$$
\nu(n)=\max_{|P|=n}\nu(P),
$$

the largest possible number of unit distances among $n$ planar points.

The conjecture discussed in the manuscript goes back to Erdős. In one asymptotic form, it predicted an absolute constant $C$ such that, for all sufficiently large $n$,

$$
\nu(n)\leq n^{1+C/\log\log n}.
$$ (eq-unit-distance-erdos-en)

The main result of the manuscript asserts the opposite: there is a fixed constant $\delta>0$ and infinitely many values of $n$ for which

$$
\nu(n)\geq n^{1+\delta}.
$$ (eq-unit-distance-main-en)

Equation {eq}`eq-unit-distance-main-en` is not merely a small improvement over a known estimate. It says that, along an infinite sequence of sizes, the number of unit distances grows with an exponent strictly larger than one.

```{admonition} Conceptual reading
:class: note
The argument is not an elementary recipe for drawing a small example by hand. It is an existence proof: it builds planar point sets from infinite towers of number fields and then projects them to the plane.
```

## Proof Map

The proof has two halves. The first is geometric: if we have enough algebraic norm-one elements, they can be interpreted as translations of length one. The second is arithmetic: it constructs number fields in which many such elements exist.

**Table. Logical map of the argument.**

| Block | Main object | Contribution |
|---|---|---|
| Planar problem | Finite set $P\subset\mathbb{R}^2$ | We want many pairs at distance $1$ |
| Geometry of numbers | Minkowski lattice in $\mathbb{C}^f$ | Counts points and translations inside a bounded window |
| Arithmetic | Fields $L$, $K=L(i)$ and split primes | Produces many elements $u$ with $u\,c(u)=1$ |
| Projection | One complex coordinate $\mathbb{C}^f\to\mathbb{C}$ | Turns algebraic translations into planar unit segments |

## Admissible Data

The geometric part starts with an admissible datum:

- a totally real field $L$ of degree $f=[L:\mathbb{Q}]$;
- the CM field $K=L(i)$, with relative complex conjugation $c$;
- distinct rational primes $q_1,\ldots,q_t$, all congruent to $1$ modulo $4$ and splitting completely in $L$.

If $Q=\prod_b q_b$, the complete splitting of these primes produces many conjugate pairs of prime ideals in $K$:

$$
\{P_s,cP_s\},\qquad s=1,\ldots,m,\qquad m=tf.
$$

For each binary vector $\varepsilon\in\{0,1\}^m$, choose an ideal

$$
A_\varepsilon=\prod_{\varepsilon_s=1}P_s
\prod_{\varepsilon_s=0}cP_s.
$$

There are $2^m$ choices but only $h(K)$ ideal classes. By the pigeonhole principle, many of those choices lie in the same ideal class. Comparing one such choice with another gives elements

$$
u_\varepsilon=\frac{\alpha_\varepsilon}{c(\alpha_\varepsilon)}
$$

which satisfy

$$
u_\varepsilon\,c(u_\varepsilon)=1.
$$ (eq-unit-distance-norm-one-en)

Since $L$ is totally real, under any complex embedding $\sigma:K\hookrightarrow \mathbb{C}$ the automorphism $c$ becomes ordinary complex conjugation. Therefore {eq}`eq-unit-distance-norm-one-en` implies

$$
|\sigma(u_\varepsilon)|=1.
$$

This is the key idea: the algebraic elements constructed in the proof have length one in every relevant complex coordinate.

## Minkowski Window and Counting

Choose a Minkowski embedding

$$
\Phi:K\longrightarrow \mathbb{C}^f,\qquad
\Phi(x)=(\sigma_1(x),\ldots,\sigma_f(x)).
$$

The fractional ideal $D^{-1}\mathcal{O}_K$, with $D=Q^2$, becomes a lattice $\Lambda\subset\mathbb{C}^f$. The elements $u\in U$ constructed above belong to this lattice and have every coordinate of modulus one.

Now take a window

$$
B_R=\{z\in\mathbb{C}^f:\lVert z\rVert_\infty\leq R\},
$$

which is a product of discs of radius $R$. For a translate $a+\Lambda$, consider the points

$$
X_a=(a+\Lambda)\cap B_R.
$$

The manuscript averages over the torus $\mathbb{C}^f/\Lambda$. The intuition is simple: if the lattice is shifted at random, the expected number of points inside the window is proportional to the volume of $B_R$, and the expected number of pairs $(x,x+u)$ with $u\in U$ depends on the overlap of $B_R$ with $B_R-u$.

If $\gamma=t\log 2-\log H>0$, this averaging gives a translate with many pairs:

$$
E_a\geq e^{\gamma f/2}|X_a|.
$$ (eq-unit-distance-many-pairs-en)

Then $X_a\subset\mathbb{C}^f$ is projected to the first complex coordinate. The projection is injective on the lattice coset being used: if two points have the same first coordinate, their difference comes from an algebraic integer with one zero embedding, and hence it is zero. This gives a planar set

$$
P=\pi_1(X_a)\subset\mathbb{C}\simeq \mathbb{R}^2.
$$

Every pair counted in {eq}`eq-unit-distance-many-pairs-en` projects to a segment of length one, because the first coordinate of each $u\in U$ has modulus one.

## Controlling the Size of $P$

To turn the estimate into a statement about $n=|P|$, one must control how many points fit inside the window. The manuscript uses a packing argument: two distinct lattice points cannot be too close in every coordinate at once, because the product of their coordinate differences is controlled by the algebraic norm.

This gives a uniform exponential upper bound

$$
|P|\leq e^{Bf}
$$

for a constant $B$ fixed by the parameters. Together with the unit-pair estimate, this gives

$$
\nu(P)\geq \frac{1}{2}|P|e^{\gamma f/2}.
$$

Since $|P|\leq e^{Bf}$, the factor $e^{\gamma f/2}$ can be rewritten as a positive power of $|P|$. Absorbing constants for large degree yields

$$
\nu(P)\geq |P|^{1+\delta}
$$

for some $\delta>0$.

## Arithmetic Construction of the Fields

The arithmetic step produces a sequence of totally real fields

$$
F=F_0\subset F_1\subset F_2\subset\cdots
$$

with degrees $f_j=[F_j:\mathbb{Q}]$ tending to infinity. The tower is everywhere unramified and has Galois groups of $3$-power order. This matters for two reasons:

1. because the tower is unramified, the root discriminant stays controlled;
2. because the proof works with pro-$3$ groups, the generator-relation count can keep the tower infinite.

The starting point is a cyclic cubic field $F$ built from cubic characters and cyclotomic fields. Rational primes $q_b$ are then chosen by Chebotarev so that they split completely in every level of the tower. To impose this splitting, the proof kills Frobenius classes lying in the Frattini subgroup. The Golod-Shafarevich inequality ensures that, even after adding those relations, the resulting pro-$3$ group remains infinite.

Finally, one sets

$$
K_j=F_j(i).
$$

The root discriminant of $K_j$ is bounded independently of $j$, and a Minkowski class-number estimate gives

$$
h(K_j)\leq H^{f_j}.
$$

The parameter $t$ is chosen on the order of $\ell^2$, while $\log H$ grows only like $O(\ell\log\ell)$. Therefore, for large $\ell$,

$$
t\log 2-\log H>0.
$$

This inequality supplies the positive parameter $\gamma>0$ used in the geometric part.

```{admonition} Student takeaway
:class: tip
The proof looks abstract because it combines combinatorial geometry, lattices, number fields, and pro-$p$ groups. A useful way to read it is to follow the gains and losses: one gains $2^{tf}$ choices of ideals, loses a controlled class-number factor, and then turns the remaining exponential gain into many planar unit distances.
```

## Bibliographic Context

The original problem and the classical unit-distance bounds are connected to Erdős, Kővári-Sós-Turán, Spencer-Szemerédi-Trotter, Székely, Ágoston-Pálvölgyi, and Guth-Katz {cite:p}`erdos1946distances,kovari1954zarankiewicz,spencer1984unitdistances,szekely1997crossing,agoston2022unitdistanceconstant,guth2015distinctdistances`. Variants for norms and related convexity problems appear in work by Brass, Brass-Moser-Pach, Eisenbrand-Pach-Rothvoß-Sopher, Bílka-Buchin-Fulek-Kiyomi-Okamoto-Tanigawa-Tóth, Matoušek, Alon-Bucić-Sauermann, Greilhuber-Schildkraut-Tidor, Valtr, and Erdős-Fishburn {cite:p}`brass1996normedspaces,brass2005researchproblems,eisenbrand2008convexlyindependent,bilka2010convexlyindependent,matousek2011unitdistancesnorms,alon2025typicalnorms,greilhuber2025unitdistancesnorms,valtr2005strictlyconvex,erdos1997equidistance`. The algebraic part uses standard tools from class field towers, pro-$p$ theory, Chebotarev, cyclotomic fields, discriminants, and class numbers {cite:p}`golod1964classfieldtower,golod1965classfieldtowers,shafarevich1963extensions,shafarevich1966extensions,neukirch1999algebraicnumbertheory,neukirch2008cohomology,koch2002galois,ribes2010profinite,dixon1999analyticpropgroups,washington1997cyclotomic,lang1994algebraicnumbertheory,davenport2000multiplicative,tschebotareff1926dichtigkeit,hajir2001globalfieldtowers,hajir2021cuttingtowers`.

````{only} html
## Page References

```{bibliography}
:filter: key in {"openai2026planarunitdistances", "erdos1946distances", "kovari1954zarankiewicz", "spencer1984unitdistances", "szekely1997crossing", "agoston2022unitdistanceconstant", "guth2015distinctdistances", "brass1996normedspaces", "brass2005researchproblems", "eisenbrand2008convexlyindependent", "bilka2010convexlyindependent", "matousek2011unitdistancesnorms", "alon2025typicalnorms", "greilhuber2025unitdistancesnorms", "valtr2005strictlyconvex", "erdos1997equidistance", "golod1964classfieldtower", "golod1965classfieldtowers", "shafarevich1963extensions", "shafarevich1966extensions", "neukirch1999algebraicnumbertheory", "neukirch2008cohomology", "koch2002galois", "ribes2010profinite", "dixon1999analyticpropgroups", "washington1997cyclotomic", "lang1994algebraicnumbertheory", "davenport2000multiplicative", "tschebotareff1926dichtigkeit", "hajir2001globalfieldtowers", "hajir2021cuttingtowers"}
```
````
