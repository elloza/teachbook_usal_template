# Balances and Conservation

## Problem statement

A solution of reactant A with concentration $C_{A0} = 2.0 \; \text{mol/L}$ is fed into a continuous stirred-tank reactor (CSTR) at a volumetric flow rate $Q = 10 \; \text{L/min}$. The reaction is:

$$A \longrightarrow B \quad \text{with} \quad r_A = -k \, C_A$$

where $k = 0.5 \; \text{min}^{-1}$. The reactor volume is $V = 100 \; \text{L}$.

Determine the outlet concentration $C_A$.

## Mass balance equation

The steady-state mass balance for component A is:

$$0 = Q \, C_{A0} - Q \, C_A + r_A \, V$$

Substituting the reaction rate expression:

$$0 = Q \, C_{A0} - Q \, C_A - k \, C_A \, V$$

## Step-by-step solution

**Step 1**: Group terms with $C_A$.

$$Q \, C_{A0} = C_A \left( Q + k V \right)$$

**Step 2**: Solve for $C_A$.

$$C_A = \frac{Q \, C_{A0}}{Q + k V}$$

**Step 3**: Substitute numerical values.

$$C_A = \frac{10 \times 2.0}{10 + 0.5 \times 100} = \frac{20}{60} = 0.333 \; \text{mol/L}$$

## Conversion

The reactor conversion is defined as:

$$X = 1 - \frac{C_A}{C_{A0}} = 1 - \frac{0.333}{2.0} = 0.833 \; (83.3\%)$$

```{admonition} Quick verification
:class: tip
Residence time: $\tau = V / Q = 100 / 10 = 10 \; \text{min}$. For a first-order CSTR: $X = k\tau / (1 + k\tau) = 5 / 6 = 0.833$. The results match.
```

## Cross-disciplinary applications

- **Chemical Engineering**: reactor design, stoichiometric calculations
- **Biology and environment**: bioreactor, ecosystem, and wastewater treatment models
- **Medicine**: pharmacokinetics and compartment models
- **Economics**: income, expenses, debt, and accumulation flows
- **Logistics**: inputs, outputs, and material storage
- **Energy**: power balances, consumption, and losses
