This project was edited by [Aristotle](https://aristotle.harmonic.fun).

To cite Aristotle:
- Tag @Aristotle-Harmonic on GitHub PRs/issues
- Add as co-author to commits:
```
Co-authored-by: Aristotle (Harmonic) <aristotle-harmonic@harmonic.fun>
```

# Start Here

Sovereign Engine checks a **declared finite structure** against a **named rule** and produces a readable receipt. The current public adapters check matrix symmetry, matrix identity, matrix inverse, finite partial orders, undirected graph connectivity, and rank-three tensor last-index symmetry.

The three public outcomes are:

| Outcome | Everyday meaning |
|---|---|
| `verified` | The named rule holds for this declared input and this check. |
| `fail` | The named rule does not hold for this declared input; the receipt explains where it differs. |
| `unverifiable` | The current input, method, or evidence is insufficient for this check. |

None of these outcomes proves a theory, predicts reality, or settles an interpretation. Begin with `python tools/sov_kernel.py --help`, then see `../how-to/README.md`.

