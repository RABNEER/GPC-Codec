# IRIS / ISEF National Science Fair: Oral Defense & Judging Guide
**Project:** Generalized Pāṭha Codes: Resolving Strand Address Dropout in Nanopore DNA Storage via Permutation Synchronization  
**Category:** Computational Biology & Bioinformatics (CBIO) / Systems Software (SOFT)  
**Author:** Student Investigator  

---

## 1. The 3-Minute Booth Elevator Pitch

*(Deliver this with confident eye contact, pointing clearly to your poster figures and your laptop running `demo_iris.py`.)*

### Hook & Problem (0:00 – 0:45)
> "Hello! Did you know that all the digital data generated in the world could theoretically fit into a teacup of synthetic DNA? DNA has an information density millions of times higher than silicon hard drives and lasts for thousands of years without electricity.
>
> But there is a major physical bottleneck during readout: **Strand Address Dropout**.
> When you sequence DNA using modern Oxford Nanopore sequencers, the DNA strand is pulled through a tiny protein pore by a motor enzyme. Frequently, the motor enzyme slips, creating a burst deletion of 5 to 15 nucleotides. Because DNA files are split across millions of unordered short strands, each strand needs an address header to tell the computer its file coordinates. 
> 
> If a motor slip deletes even a few bases of that address, the coordinate is destroyed. The sequencer cannot determine where the data belongs, and the entire 150-nucleotide strand is discarded. Current error-correcting codes collapse completely under burst deletions, resulting in 100% strand loss."

### The Core Idea & Ancient Inspiration (0:45 – 1:30)
> "To solve this, I looked at a historical precedent: **how did ancient oral scholars preserve massive texts without writing?**
>
> 2,500 years ago in India, scholars faced an acoustic memory channel prone to spoken omissions and transpositions. They developed cyclic permutation recitation modes called *vikṛti-pāṭhas*, specifically *Ghana-pāṭha*, which repeats phrases in forward and backward overlapping trigrams: $1-2, 2-1, 1-2-3, 3-2-1, 1-2-3$. If a chanter drops a word, the forward-backward symmetry breaks immediately, localizing the omission in real time.
>
> I translated this ancient mnemonic principle into a modern mathematical coding framework: **Generalized Pāṭha Codes (GPC)**. GPC arranges address bits into five cyclic forward-reverse permutation passes anchored by deterministic pilot bits, creating a parameterized code family $M = 13K + 6$."

### The Engineering Solution & 16.20% Overhead Math (1:30 – 2:15)
> "Now, you might ask: *'Doesn't repeating data make the code slow?'* GPC has an inner code rate of 6.9%. If you applied that to the entire file, it would inflate data size by 14 times.
>
> But here is my key engineering insight: **We don't encode the payload with GPC; we encode only the 29-nucleotide Address Header.**
> 
> Think of an envelope. You don't need to write the letter twice, but you do want the address written in waterproof ink. Adding our 29-nt GPC address to a 150-nt biological payload results in a 179-nucleotide strand. That is only **16.20% total overhead**, well within the 200-nucleotide commercial synthesis limit of Twist Bioscience. For a 16% insurance policy, we guarantee the strand survives."

### Results & Failure Boundaries (2:15 – 3:00)
> "To test this scientifically, I built an in-silico sequencing simulator using published Oxford Nanopore R10.4 translocation error distributions on the authentic, Sanger-sequenced genome of **Bacteriophage $\Phi$X174** from NCBI.
>
> Across 72,732 machine trials:
> 1. GPC achieved **0.0% strand loss** up to 10-nucleotide (20-bit) motor stalls, while state-of-the-art codes like Schoeny et al. collapsed to 100% loss at 8 nucleotides.
> 2. Under realistic compound noise (substitutions, insertions, and stalls), GPC bound strand loss between 2.8% and 7.2%, safely within outer fountain code recovery margins.
> 3. To prove edge-device viability, I designed a synthesizable decoder in **Verilog RTL**, decoding strands in just $81.6\,\mu\text{s}$ at $1.3\text{ mW}$.
>
> To be scientifically rigorous, GPC has boundaries: when burst deletions exceed 23 nucleotides or background substitutions exceed 15%, consensus voting degrades. But rather than corrupting data silently, GPC flags an erasure so outer fountain codes can re-read the strand.
> 
> In summary, GPC turns an ancient oral tradition into a practical, 16% overhead physical layer header that prevents strand dropout in DNA data storage."

---

## 2. The 5 Deadliest Judge Questions & How to Defend Them

### Q1: "Did you actually synthesize DNA or run an Oxford Nanopore sequencer in a wet lab?"
* **The Trap:** If you claim wet-lab experiments without evidence, you will be caught and penalized.
* **The Truthful Student Defense:**
  > "No, sir/ma'am. As an independent high school project, physical wet-lab synthesis with Twist Bioscience and MinION flow cells was beyond our available laboratory budget. 
  > 
  > Instead, we conducted a rigorous computational study categorized under Computational Biology. We used the authentic 5,386-base genome of Bacteriophage $\Phi$X174 directly from NCBI (`NC_001422.1`), and injected the exact empirical translocation stall and error distributions measured in published Oxford Nanopore R10.4 literature across 72,732 trials. Physical synthesis and sequencing is our designated next-phase research grant objective."

### Q2: "A code rate of 6.9% ($R = 4/58$) is terribly inefficient. Why would anyone use this?"
* **The Trap:** The judge is testing your understanding of Shannon channel capacity and storage economics.
* **The Truthful Student Defense:**
  > "If GPC were used on bulk payload data, a 6.9% rate would indeed be completely unacceptable. But that is why we decouple the header from the payload.
  > 
  > In DNA storage, strands in the pool are unindexed. If a 10-base motor stall wipes out the address, the entire 150-base payload must be discarded—a 100% loss. By spending 29 nucleotides of GPC on the address header, our total strand length is 179 nt. 
  > 
  > That is an overall strand overhead of only **16.20%**. Spending 16% redundancy on the address to prevent 100% discarding of the biological payload is a highly favorable engineering trade-off."

### Q3: "Did you fabricate a real 28nm silicon ASIC chip?"
* **The Trap:** Testing whether you understand the difference between chip fabrication and digital simulation.
* **The Truthful Student Defense:**
  > "No, we did not tape out physical silicon. We wrote synthesizable digital logic in **Verilog RTL** and performed logic synthesis and timing verification targeting FPGA architectures. 
  > 
  > The $81.6\,\mu\text{s}$ latency and $1.3\text{ mW}$ power consumption are post-synthesis gate-level simulation benchmarks. This confirms that GPC decoding can run on low-cost FPGA accelerators directly attached to a handheld MinION sequencer without requiring expensive server CPUs."

### Q4: "Where does your algorithm fail? What are its limitations?"
* **The Trap:** Judges love to see if a student understands their system's weaknesses or if they blindly claim 100% perfection everywhere.
* **The Truthful Student Defense:**
  > "GPC has four distinct operational boundaries:
  > 1. **Burst Length Limit ($B_E = 10K+7$):** For $K=4$, if an isolated burst deletion exceeds 23 nucleotides (47 symbols), it obliterates more than two consecutive pilots and the decoder begins to experience strand loss (2.6% at 12 nt, 24% at 16 nt).
  > 2. **High Background Substitutions ($>15\%$):** GPC uses consensus voting across the 5 permutation passes. If random substitutions flip more than half the copies of a bit simultaneously, consensus fails.
  > 3. **Worst-Case Periodic Ties:** If the payload is completely periodic (like `101010`), candidate displacement scores can tie, pushing decoding time from linear $\mathcal{O}(M)$ to quadratic $\mathcal{O}(M^2)$.
  > 4. **In-Silico Simulation:** Real chemical synthesis introduces secondary structures like hairpins and G-quadruplexes that purely statistical error models do not capture."

### Q5: "What makes your work fundamentally novel compared to existing codes like Schoeny et al. or Varshamov-Tenengolts (VT) codes?"
* **The Trap:** Testing if you actually understand the prior art.
* **The Truthful Student Defense:**
  > "VT codes are designed strictly for single deletions; when hit by a 5-base burst, their syndrome arithmetic breaks and strand loss is 100%. 
  > 
  > Schoeny et al. (IEEE 2017) introduced burst deletion codes using cyclic shift constraints, but their design radius is limited to $b \le 6\text{ nt}$. When a nanopore motor stall exceeds 6 bases, Schoeny collapses to 100% loss because it lacks multi-scale forward-reverse cross-checks. 
  > 
  > GPC's novelty is the bidirectional permutation architecture inspired by *Ghana-pāṭha*: by interleaving forward and backward passes between deterministic pilots, we create a topological invariant where an unaligned shift creates detectable margin contradictions in $\mathcal{O}(M)$ time, surviving stalls up to 10 nucleotides."

---

## 3. Poster Display Board Architecture (3-Panel Layout)

```
+---------------------------+-----------------------------------+-----------------------------+
|        LEFT PANEL         |           CENTER PANEL            |         RIGHT PANEL         |
|  (The Problem & Heritage) |       (Method & Architecture)     |   (Real Results & Impact)   |
+---------------------------+-----------------------------------+-----------------------------+
| 1. THE MOTIVATION         | 4. THE GPC(K) MATHEMATICAL CODEC  | 7. PHIX174 BENCHMARK        |
|    - Why DNA Storage?     |    - M = 13K + 6 Codeword Family  |    - 0% loss @ 10-nt burst  |
|    - Oxford Nanopore      |    - 5 Permutation Passes         |    - Baselines collapse @ 8 |
|      Translocation Physics|    - 6 Deterministic Pilot Anchors|    - Fig 4: Burst Confinement|
|                           |    - B_E = 10K + 7 Exact Span     |                             |
| 2. THE BOTTLENECK:        |                                   | 8. COMPOUND NOISE & IMAGE   |
|    STRAND ADDRESS DROPOUT | 5. ALGORITHM 1: TWO-PHASE DECODER |    - R10.4 mixed error model|
|    - Motor slips (5-15 nt)|    - Pilot Distance Checking      |    - Fig 6: 2D Image Recovery|
|    - Lost index = 100%    |    - Consensus Margin Voting      |                             |
|      strand discarded!    |    - Average O(M) Complexity      | 9. HONEST FAILURE CASES     |
|                           |                                   |    - Burst > 23 nt behavior |
| 3. ANCIENT INSPIRATION    | 6. THE 16.20% OVERHEAD SOLUTION   |    - Substitution boundaries|
|    - Vedic Ghana-patha    |    - 29-nt Header + 150-nt Payload|                             |
|    - Bidirectional cyclic |    - 179 nt < 200 nt Twist Limit  | 10. FPGA VERILOG RTL & NEXT |
|      permutations (1-2-3, |    - Solving the Rate Paradox     |    - 81.6 us latency @ 1.3mW|
|      3-2-1, 1-2-3)        |                                   |    - Next: Wet-lab testing  |
+---------------------------+-----------------------------------+-----------------------------+
```
