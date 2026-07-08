# Expected Value

Companion notes for [`notebooks/expected_value.ipynb`](../notebooks/expected_value.ipynb),
a nine-section walkthrough of expected value (EV) in poker — from a coin-flip
warm-up through Kuhn Poker, GTO, and Counterfactual Regret Minimization (CFR).

Every decision in poker — call, fold, bet, raise — is a probability-weighted
average of its outcomes:

```
EV = Σ P(outcome_i) × value(outcome_i)
```

A **+EV** play wins money on average over many repetitions; a **−EV** play loses
it. Good play is consistently choosing +EV lines regardless of short-term swings.

## Running the notebook

The notebook depends on `pkpy` (the Python bindings for the `pkcore` poker
engine) and `jupyterquiz` for the inline quizzes. Both are installed in the
Docker image:

```bash
docker compose build   # installs pkpython (provides the pkpy module) + jupyterquiz
docker compose up      # JupyterLab on http://localhost:8888
```

> **Note:** the PyPI distribution is named `pkpython`; the import name is `pkpy`.
> The notebook runs top-to-bottom without errors against `pkpython 0.1.0`.

## Section map

| # | Section | Core idea | Key pkpy API |
|---|---------|-----------|--------------|
| 1 | EV Fundamentals | EV as a probability-weighted sum, via a coin-flip bet | — |
| 2 | Pot Odds & Break-Even Equity | Minimum equity needed for a +EV call | — |
| 3 | Preflop All-In EV vs a Range | EV of calling a shove, hand-by-hand vs a range | `pkpy.Versus` |
| 4 | Drawing Hand EV on the Turn | Exact turn→river equity by enumerating all 44 rivers | `pkpy.Game.turn_case_evals()`, `pkpy.Outs` |
| 5 | Kuhn Poker Game Tree | Enumerate every deal × action sequence exactly | `pkpy.KuhnCard`, `KuhnState` |
| 6 | EV Under Different Strategies | Default heuristic vs GTO (Nash) per-hand EV | `pkpy.KuhnStrategy` |
| 7 | Exploitability & CFR | How much EV a non-GTO strategy leaks; CFR convergence | `pkpy.KuhnCfr` |
| 8 | GTO Action Probabilities | Converged CFR probs vs the closed-form Nash solution | `KuhnStrategy.action_probs` |
| 9 | EV Comparison vs GTO | Any deviation from Nash is exploitable by a best response | `KuhnStrategy.gto(alpha)` |

## Formulas worth memorizing

- **Break-even equity** facing a bet:
  `break_even = call / (pot + 2 × call)`
  (`pot` is the pot *before* the bet; the pot after calling is `pot + 2 × call`.)
- **EV of a call/showdown:**
  `EV(call) = equity × total_pot − (1 − equity) × call_amount`, with `EV(fold) = 0` by convention.
- **Kuhn Poker Nash value:** Player 0's equilibrium EV is **−1/18 ≈ −0.0556**
  chips/hand — a structural penalty for acting first without information.
- **Kuhn GTO bluff frequency:** P0 bluffs the Jack at rate `alpha ∈ [0, 1/3]`.
  `1/3` is the ceiling — it's the exact frequency that leaves P1 *indifferent* to
  calling with a Queen. Beyond `1/3` the strategy is no longer a Nash
  equilibrium, and `pkpy.KuhnStrategy.gto()` refuses to build it (raises
  `ValueError`). See Section 9 / Quiz 9 for the boundary demonstration.

## Resources

### Kuhn Poker & CFR
- Harold W. Kuhn, *"A Simplified Two-Person Poker"* (1950) — the original
  three-card game analyzed in Sections 5–9.
- Zinkevich, Johanson, Bowling & Piccione, *"Regret Minimization in Games with
  Incomplete Information"* (NeurIPS 2007) — the CFR algorithm behind `KuhnCfr`.
- [Kuhn poker — Wikipedia](https://en.wikipedia.org/wiki/Kuhn_poker) — concise
  summary of the game tree and equilibrium strategies.

### Engine
- [`ImperialBower/pkpy`](https://github.com/ImperialBower/pkpy) — Python bindings.
- [`ImperialBower/pkcore`](https://github.com/ImperialBower/pkcore) — the Rust
  poker engine underneath.

### General EV / pot odds
- Bill Chen & Jerrod Ankenman, *The Mathematics of Poker* (2006) — the standard
  reference for EV, equity, and equilibrium reasoning.
