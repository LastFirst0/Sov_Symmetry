# How Claims Move Through Sovereign Engine

## The short version

Sovereign Engine does not ask you to believe a claim because it sounds advanced, comes from a famous theory, or has a large amount of math behind it. A claim moves through a visible process. At each step, the system says what it can check, what it cannot check, and what evidence is still needed.

> The system can help organize and inspect evidence. It does not decide what reality is, choose a favorite theory, or turn missing evidence into certainty.

## Step 1: Name the claim

Someone writes down a specific claim in ordinary language and gives it a stable ID. They also say what kind of claim it is.

| Claim kind | Example of what happens next |
|---|---|
| Structural | “This finite graph is connected.” The kernel can run a named graph check. |
| Formal or computational | “This declared expression has this property.” The kernel can run a bounded predicate if one exists. |
| Empirical | “This measurement supports this effect.” The system requires dataset and uncertainty information. |
| Interpretive or metaphysical | “This means reality has this nature.” The system records it as interpretation, not a kernel fact. |

## Step 2: Show the inputs

For a structural claim, the input might be a matrix, graph, relation, or finite tensor. For an empirical claim, it includes data versions, where they came from, how they were changed, who was responsible, and what access or license limits apply.

If important input is missing, the correct outcome is **unverifiable**. That does not mean false. It means the current information is not enough for this particular process.

## Step 3: State the rule being checked

The rule must be named before the result appears. For example, “matrix symmetry” means comparing a matrix with its transpose. “Graph connectivity” means checking whether every vertex can be reached in a simple undirected graph. The system is not allowed to quietly swap in a different rule because it likes a framework label.

## Step 4: Record uncertainty and limits

Measurements and models have limits. The evidence packet records the estimate, units, uncertainty components, how they were combined, and the reason for any confidence statement. If the basis for a confidence claim is missing, it is marked as missing.

## Step 5: Run a bounded process

Structural checks return one of three outcomes: **holds in this check**, **does not hold in this check**, or **cannot be checked here**. Empirical claims need a separately named analysis method. Until that process runs, the structural kernel does not pretend to have an empirical answer.

## Step 6: Read the receipt

A receipt explains what was checked, why it produced its outcome, what input was used, and what the outcome does not prove. Advanced users can replay it and, where available, inspect local audit and integrity evidence.

## Step 7: Review and publish carefully

Before a new external adapter is added, it goes through eight gates. Independent reviewers examine what the predicate means and whether the code behaves deterministically. The same input is tested under several provenance labels. If the result changes because of a theory name, the adapter fails admission.

## What a passing result really means

A passing result means that a named rule held for the declared input under stated assumptions. It does **not** prove an entire research program, predict nature, or settle an interpretation. Those broader questions need broader evidence and open debate.

## What you can do

You can submit a well-described bounded claim, inspect why a result was produced, ask what assumptions were used, compare evidence packages, and see what remains uncertain. You should not treat a receipt as a replacement for scientific replication, peer review, measurement expertise, or philosophical judgment.
