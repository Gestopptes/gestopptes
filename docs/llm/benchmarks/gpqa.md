[Source](https://arxiv.org/pdf/2311.12022) [Extracted with](https://chatgpt.com/share/e/91b9d444-7f74-45a2-9605-7775ef37cce1)
## Summary of "GPQA: A Graduate-Level Google-Proof Q&A Benchmark"

### Abstract

GPQA (Graduate-Level Google-Proof Q&A Benchmark) is a dataset of 448 challenging multiple-choice questions in biology, physics, and chemistry. These questions, written by domain experts, are designed to be extremely difficult. Experts with PhDs in the respective fields achieve a 65% accuracy rate, while non-experts with access to the internet only achieve 34%. GPT-4, a state-of-the-art AI, reaches 39% accuracy. The purpose of GPQA is to enable the development of scalable oversight methods for AI systems that help humans advance scientific knowledge.

### Introduction

The rapid advancements in large language model (LLM) capabilities suggest that AI could soon help in advancing human knowledge. However, aligning models to ensure they provide truthful information, especially on questions beyond human verification, remains a challenge. GPQA aims to serve as a testbed for scalable oversight methods, ensuring that even highly skilled non-experts cannot solve these questions easily, making it suitable for future AI evaluation.

### Data Collection

GPQA consists of questions written by domain experts who are either pursuing or have completed a PhD. The collection process involves four main stages: question writing, expert validation, question revision, and non-expert validation. This process ensures the questions are difficult, objective, and vetted by experts in the field.

#### Collection Pipeline

1. **Question Writing**: Experts write challenging questions within their domain, ensuring other experts can answer them without needing the multiple-choice options.
2. **Expert Validation**: Another expert in the same domain validates the question, providing feedback and suggested revisions.
3. **Question Revision**: The question writer revises the question based on the first expert’s feedback.
4. **Second Expert Validation**: A second expert validates the revised question. Feedback from this step helps in judging the objectivity of the question.
5. **Non-Expert Validation**: Non-experts, skilled in other domains, attempt to answer the questions. They have unrestricted internet access but cannot use LLM assistants.

### Domains and Subdomains

GPQA covers three main domains: biology, physics, and chemistry, with questions further categorized into specific subdomains:

- **Biology**: Molecular Biology, Genetics
- **Physics**: Quantum Mechanics, High-Energy Particle Physics, Astrophysics, Electromagnetism and Photonics, among others.
- **Chemistry**: Organic Chemistry, General Chemistry, Inorganic Chemistry, Analytical Chemistry, Physical Chemistry

### Dataset Statistics

The dataset consists of 564 questions, with a median length of 561 characters. It is divided into three subsets:

1. **GPQA Extended**: 546 questions.
2. **GPQA (Main Set)**: 448 questions, recommended for primary use.
3. **GPQA Diamond**: 198 questions, the highest quality subset.

### Question Objectivity

Question objectivity is assessed through expert validation and post-hoc agreement. Expert validators report a high level of expertise in 90.7% of validations. The estimated objectivity rate is 74% for GPQA Extended and higher for the main and diamond sets.

### Question Difficulty

The questions are designed to be challenging, with non-expert accuracy averaging 34.1%. This ensures the questions are difficult even for highly skilled non-experts with internet access.

### Baseline Evaluations

Baseline model evaluations are conducted in both closed-book and open-book settings:

- **Closed-Book**: Models like Llama-2-70B-chat, GPT-3.5-turbo-16k, and GPT-4 are evaluated using various prompting methods. GPT-4 with few-shot chain-of-thought prompting performs best with up to 40% accuracy.
- **Open-Book**: GPT-4 with internet access performs slightly better but has a high abstention rate.

### Related Work

GPQA is compared to other QA benchmarks like SQuAD, TriviaQA, and MMLU. Unlike these, GPQA focuses on questions that are beyond the reach of non-experts even with internet access, making it suitable for scalable oversight experiments.

### Limitations

GPQA has several limitations:

- **Small Size**: With only 448 questions in the main set, it has limited statistical power for accuracy comparisons.
- **Specialized Non-Experts**: The dataset uses highly skilled non-experts, which might not directly translate to real-world settings.
- **Bias**: Sourced from Upwork, there might be regional and demographic biases in the expertise included.
- **Applicability**: While designed for scalable oversight, it is an imperfect proxy for supervising superhuman AI systems.

### Conclusion

GPQA is a challenging dataset designed to test scalable oversight methods for future AI systems. With high difficulty and vetted objectivity, it provides a robust testbed for developing protocols to supervise superhuman AI models.

## Extracted Tables

### Table 1: Example Questions

| Domain           | Question                                                                                                                                   | Options                        | Correct Answer | Explanation                                                                                           |
|------------------|---------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------|----------------|-------------------------------------------------------------------------------------------------------|
| Chemistry (general) | A reaction of a liquid organic compound at 80°C and 20 bar for 24 hours results in signals shifting in the proton NMR spectrum. What compounds were likely added? | A) Metal compound from the fifth period B) Metal compound from the fifth period and a non-metal compound from the third period C) Metal compound from the fourth period D) Metal compound from the fourth period and a non-metal compound from the second period | A) | A metal compound from the fifth period is typically used in such industrial processes.                 |
| Organic Chemistry  | Methylcyclopentadiene reacts with methyl isoamyl ketone and pyrrolidine to form a bright yellow product. How many chemically distinct isomers make up the final product (excluding stereoisomers)? | A) 2 B) 16 C) 8 D) 4            | B)             | There are 16 possible products considering the interconverting mixture of isomers and directions of approach. |
| Genetics           | If a sperm from species A is injected into an egg from species B, what would cause the resulting zygote mortality?                         | A) Species-specific zona pellucida proteins B) Epistatic interactions between genes C) Chromosomal incompatibilities D) Chromosomal recombination | C)             | Chromosomal incompatibilities will cause failure of meiosis leading to zygote death.                   |
| Molecular Biology  | A scientist finds a protein contributing to heat tolerance in barley but not synthesized in wheat. What could be the reason?               | A) miRNA targeting protein B) Trimethylation of histone H3 C) Stop-codon in 5’-UTR D) Proteolysis disrupting quaternary structure | B)             | Trimethylation of lysine of H3 histone at the gene promoter could prevent protein synthesis.           |
| Astrophysics       | Astronomers study a star with Teff ~6000 K using spectral lines of two elements. Which lines are most sensitive to surface gravity?        | A) El2 I (neutral) B) El1 II (singly ionized) C) El2 II (singly ionized) D) El1 I (neutral) | C)             | El2 II (singly ionized) lines are most sensitive to surface gravity under these conditions.            |
| Quantum Mechanics  | Given a depolarizing channel operation with Kraus operators, what is the correct Kraus representation of the state?                         | A) (1 − p)ρ + (p/3)XρX + (p/3)YρY + (p/3)ZρZ B) (1 − p)ρ + (p/3)Xρ²X + (p/3)Yρ²Y + (p/3)Zρ²Z C) (1 − p)ρ + (p/4)XρX + (p/4)YρY + (p/4)ZρZ D) (1 − p)ρ² + (p/3)Xρ²X + (p/3)Yρ²Y + (p/3)Zρ²Z | A)             | The correct representation accounts for the depolarizing noise in the state.                            |

### Table 2: Dataset Statistics

| Data Split        | Count | Expert Accuracy (%) | Non-Expert Accuracy (%) | Sufficient Expertise (%) |
|-------------------|-------|---------------------|--------------------------|--------------------------|
| GPQA Extended     | 546   | 64.8                | 34.1                     | 90.7                     |
| GPQA (Main Set)   | 448   | 71.9*               | 30.4*                    | 93.5                     |
| GPQA Diamond      | 198   | 81.3*               | 22.1*                    | 97.0                     |

### Table 3: Domain Statistics

| Domain  | Count | Expert Accuracy (%) | Non-Expert Accuracy (%) | Δ (pts) |
|---------|-------|---------------------|--------------------------|---------|
| Biology | 105   | 66.7                | 43.2                     | 23.5    |
| Physics | 227   | 57.3                | 32.5                     | 24.8    |
| Chemistry| 214  | 72.0                | 31.4                     | 40.6    |

### Table 4: Expert Validator Feedback

| Category                                   | Count | Percentage (%) | Total (%) |
|--------------------------------------------|-------|----------------|-----------|
| 1: Question is good, clear mistake identified | 48    | 25.1           | 45.6     

 |
| 2: Question is good, demonstrates understanding of explanation | 15    | 7.9            |           |
| 3: Question is good, no description of mistake | 24    | 12.6           |           |
| 4: Question may be good, disclaims expertise | 32    | 16.8           | 24.1      |
| 5: Question seems potentially bad, expression of doubt | 14    | 7.3            |           |
| 6: Question is bad, answer is arguable      | 15    | 7.9            | 28.3      |
| 7: Question is bad, assumptions are missing from question | 16    | 8.4            |           |
| 8: Question is bad, answer is wrong         | 23    | 12.0           |           |
| Feedback and revisions missing              | 4     | 2.1            |           |

### Table 5: Baseline Model Accuracies

| Evaluation Method and Model                    | Extended Set (%) | Main Set (%) | Diamond Set (%) |
|------------------------------------------------|------------------|--------------|------------------|
| Few-Shot CoT Llama-2-70B-chat                  | 30.4             | 29.1         | 28.1             |
| Few-Shot CoT GPT-3.5-turbo-16k                 | 28.2             | 28.0         | 29.6             |
| Few-Shot CoT GPT-4                             | 38.7             | 39.7         | 38.8             |
| GPT-4 with search (backoff to CoT on abstention)| 39.4             | 41.0         | 38.8             |
| Expert Human Validators                        | 65.4             | 72.5*        | 81.2*            |
| Non-Expert Human Validators                    | 33.9             | 30.5*        | 21.9*            |

### Conclusion

GPQA presents a set of extremely challenging questions that push the boundaries of human expertise and AI capabilities. By leveraging this dataset, researchers can develop and test methods for ensuring AI systems provide truthful and accurate information, even on topics that are difficult to validate.