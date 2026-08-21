# M0 Public Source Selection

**Selected source:** Genomic Benchmarks `human_nontata_promoters`, version 0, distributed through Zenodo record **16605299**. The repository identifies the task as a binary positive/negative non-TATA promoter benchmark with 251-base intervals and published train/test sets. Its public repository is Apache-2.0 licensed; the Zenodo dataset record is open and states a CC BY 4.0 license. [1] [2]

> **Scope boundary:** The source is used only as a public, non-clinical sequence-classification benchmark. It does not provide personal genomic analysis, disease prediction, gene-function validation, or therapeutic inference.

The source is suitable for M0 because it supplies a compact public archive and an external record/DOI. It is not the exact GUE corpus originally proposed, so the experiment will identify it as a **Genomic Benchmarks M0 pilot**. A later GUE replication remains a separately pinned work package. The original archive has train/test partitions but no validation partition, so M0 will derive validation only from the upstream train data by a fixed, seed-recorded, label-stratified split; upstream test will remain untouched.

| Source property | M0 treatment |
|---|---|
| Zenodo record | Pin record ID, DOI, archive URL, publisher-provided MD5, retrieved SHA-256, and source Git commit. |
| Sequence archive | Keep raw zip untouched; derive canonical records as a new artifact with its own digest. |
| Upstream train/test | Preserve test untouched; derive validation from train under a frozen seed and manifest. |
| Public human-reference sequence context | Treat as non-clinical public benchmark material; prohibit health or individual-level interpretation. |
| Dataset license | Record CC BY 4.0 from the Zenodo record and Apache-2.0 for the code repository; retain attribution in reports. |

## References

[1]: https://github.com/ML-Bioinfo-CEITEC/genomic_benchmarks "Genomic Benchmarks repository"
[2]: https://zenodo.org/records/16605299 "Genomic Benchmarks version 1, Zenodo record 16605299"
