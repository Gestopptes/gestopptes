[Source](https://arxiv.org/pdf/2103.03874) [Extracted with](https://chatgpt.com/share/e/64046a3a-ef8d-4c61-8650-eaea3cb8108e)
### Measuring Mathematical Problem Solving With the MATH Dataset

**Authors**: Dan Hendrycks, Collin Burns, Saurav Kadavath, Akul Arora, Steven Basart, Eric Tang, Dawn Song, Jacob Steinhardt

---

#### Abstract
Mathematical problem solving remains a challenging task for computers. To assess and improve this ability in machine learning models, the MATH dataset has been introduced. It contains 12,500 challenging competition math problems with step-by-step solutions. An auxiliary pretraining dataset helps in teaching models fundamental math concepts. Despite improvements, the accuracy remains low, suggesting the need for new algorithmic advancements.

---

### Introduction
Mathematics is integral to various intellectual endeavors due to its consistency and logic-based nature. It is essential for modeling phenomena in sciences and engineering. The MATH dataset measures the problem-solving ability of machine learning models, distinguishing it from basic calculation skills. It comprises 12,500 problems from high school math competitions, tagged by difficulty levels and covering seven subjects. This dataset is aimed at evaluating and enhancing mathematical reasoning in AI models.

### Related Work
Previous work on mathematical reasoning in AI includes automated theorem proving benchmarks like Coq, HOLStep, and Metamath, and symbolic calculation tasks by DeepMind. These tasks are generally simpler compared to MATH, which involves more complex problem-solving. Transformers have shown success in many NLP tasks, but MATH remains a significant challenge, requiring innovative algorithmic approaches.

### Datasets
#### The MATH Dataset
MATH consists of 12,500 problems from competitions like AMC 10, AMC 12, and AIME, categorized into seven subjects with five difficulty levels. Each problem has a step-by-step solution in LaTeX and Asymptote, enabling models to process figures and diagrams. The exact match scoring method ensures consistency in evaluation.

#### The AMPS Dataset
The Auxiliary Mathematics Problems and Solutions (AMPS) dataset supports pretraining. It includes 100,000 Khan Academy problems and 5 million Mathematica-generated problems, covering a wide range of topics in algebra, calculus, geometry, and more. Pretraining on AMPS significantly boosts model performance.

### Experiments
#### Experimental Setup
The experiments use GPT-2 and GPT-3 models with various sizes, pretrained on AMPS. During fine-tuning, models predict final answers and generate step-by-step solutions. The performance is evaluated using beam search.

#### Results
AMPS pretraining improves performance significantly, comparable to a 130x increase in model size. However, the overall accuracy remains low, even for large models. The accuracy increases slowly with model size, indicating the need for new techniques. Models perform better when provided with partial solutions or when trained on step-by-step solutions.

### Analysis
#### Error Detection
Models exhibit high overconfidence, with an AUROC of 68.8%, indicating room for improvement in detecting incorrect answers.

#### Step-by-Step Solutions
Generating step-by-step solutions before final answers decreases accuracy due to error propagation. However, partial solutions improve performance, demonstrating their potential benefit.

### Conclusion
The MATH dataset provides a benchmark for mathematical problem-solving in AI, highlighting the current limitations of large language models. Significant progress will require new algorithmic advancements, not just larger models. Solving MATH would be a substantial step forward for AI in mathematics and beyond.

---

### Tables

**Table 1: Topics Covered by AMPS Dataset**

| Subject          | Topics                                                                                                                                                           |
|------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Algebra          | Conic sections, polynomial GCD, De Moivre’s theorem, function inverses, ...                                                                                       |
| Calculus         | Arclength, Jacobian, Laplacian, divergence, curl, gradients, integrals, ...                                                                                       |
| Statistics       | Expectation, geometric mean, harmonic mean, KL divergence, variance, ...                                                                                         |
| Geometry         | Triangle area, triangle inradius, polygon angles, polyhedron diameter, ...                                                                                       |
| Linear Algebra   | Characteristic polynomials, eigenvalues, reduced row echelon form, ...                                                                                            |
| Number Theory    | Modular inverse, Euler’s totient function, Chinese remainder theorem, ...                                                                                        |

**Table 2: MATH Accuracies Across Subjects**

| Model          | Prealgebra | Algebra | Number Theory | Counting & Probability | Geometry | Intermediate Algebra | Precalculus | Average | Improvement (%) |
|----------------|------------|---------|---------------|------------------------|----------|----------------------|-------------|---------|------------------|
| GPT-2 0.1B     | 5.2        | 5.1     | 5.0           | 2.8                    | 5.7      | 6.5                  | 7.3         | 5.4     | 0                |
| GPT-2 0.3B     | 6.7        | 6.6     | 5.5           | 3.8                    | 6.9      | 6.0                  | 7.1         | 6.2     | +15              |
| GPT-2 0.7B     | 6.9        | 6.1     | 5.5           | 5.1                    | 8.2      | 5.8                  | 7.7         | 6.4     | +19              |
| GPT-2 1.5B     | 8.3        | 6.2     | 4.8           | 5.4                    | 8.7      | 6.1                  | 8.8         | 6.9     | +28              |
| GPT-3 13B*     | 4.1        | 2.4     | 3.3           | 4.5                    | 1.0      | 3.2                  | 2.0         | 3.0     | -44              |
| GPT-3 13B      | 6.8        | 5.3     | 5.5           | 4.1                    | 7.1      | 4.7                  | 5.8         | 5.6     | +4               |
| GPT-3 175B*    | 7.7        | 6.0     | 4.4           | 4.7                    | 3.1      | 4.4                  | 4.0         | 5.2     | -4               |

---

### Appendix
The appendix provides additional comparisons with previous datasets, details on the logic and intelligence tests, further dataset information, and results with the BART architecture. It also includes the human evaluation methodology and comprehensive breakdowns of MATH accuracy across different difficulty levels and subjects.

This summary provides an overview of the main sections and findings of the paper, including the key datasets, experimental results, and the necessity for future research to enhance mathematical problem-solving in AI models.