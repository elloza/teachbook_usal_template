# Practice Questions: Statistics

Test your knowledge of fundamental statistics concepts.
Expand each question to reveal the answer.

---

```{admonition} Question 1 — p-value
:class: dropdown

**What exactly does a p-value of 0.03 mean in a hypothesis test?**

A p-value of 0.03 means that, **if the null hypothesis $H_0$ were true**,
the probability of observing a result as extreme or more extreme than the one
obtained would be 3%.

**Important:** It is NOT the probability that $H_0$ is true. It is the probability
of the data (or more extreme) given $H_0$.

Since 0.03 < 0.05 (the typical significance level), we would reject $H_0$.
```

```{admonition} Question 2 — Confidence interval
:class: dropdown

**Interpret a 95% confidence interval for a mean: $[12.3, 15.7]$.**

It does NOT mean the population mean has a 95% probability of being in that interval.
The correct frequentist interpretation is:

> If we repeat the experiment many times, 95% of the intervals constructed
> with the same method will contain the true parameter value.

For this particular interval, the population mean is either inside or outside — there
is no intermediate probability. What has 95% confidence is the **construction method**.
```

```{admonition} Question 3 — Normal distribution
:class: dropdown

**What proportion of data falls within ±2 standard deviations of the mean
in a normal distribution?**

Using the empirical rule (68-95-99.7 rule):


The following table summarizes the main elements of this section.

**Table. Practice Questions: Statistics.**

| Range | Proportion |
|-------|-----------|
| $\mu \pm 1\sigma$ | ≈ 68.27% |
| $\mu \pm 2\sigma$ | ≈ 95.45% |
| $\mu \pm 3\sigma$ | ≈ 99.73% |

Therefore, approximately **95.45%** of data falls within $\mu \pm 2\sigma$.
```

```{admonition} Question 4 — Correlation vs. Causation
:class: dropdown

**If two variables have a correlation of $r = 0.85$, can you conclude that one causes the other?**

**No.** Correlation does not imply causation. A strong correlation only indicates linear
association. Possible explanations include:

1. **$X$ causes $Y$** — possible but not proven by $r$ alone.
2. **$Y$ causes $X$** — the direction could be reversed.
3. **A confounding variable $Z$** causes both.
4. **Coincidence** — especially with small datasets.

Establishing causation requires experimental studies (randomized controlled trials),
not just observational data.
```

```{admonition} Question 5 — Type I and Type II Errors
:class: dropdown

**Define Type I and Type II errors. Which one is directly controlled by the α level?**


The following table summarizes the main elements of this section.

**Table. Practice Questions: Statistics.**

| Type | Occurs when... | Called |
|------|----------------|--------|
| **Type I Error** | We reject $H_0$ when it is true | False positive |
| **Type II Error** | We fail to reject $H_0$ when it is false | False negative |

The **significance level $\alpha$** directly controls the probability of committing
a Type I error: $P(\text{Type I}) = \alpha$.

The probability of a Type II error is denoted $\beta$, and the power of a test is
$1 - \beta$. Decreasing $\alpha$ generally increases $\beta$.
```

```{admonition} Question 6 — Central Limit Theorem
:class: dropdown

**State the Central Limit Theorem and explain its practical importance.**

The **Central Limit Theorem (CLT)** states that, for sufficiently large samples
($n \geq 30$, approximately), the distribution of the sample mean $\bar{X}$
approaches a normal distribution:

$$\bar{X} \sim N\left(\mu, \frac{\sigma^2}{n}\right)$$

regardless of the original population distribution.

**Practical importance:** It justifies using the normal distribution to construct
confidence intervals and perform hypothesis tests about the mean, even when the
population is not normal. It is the foundation of much of inferential statistics.
```
