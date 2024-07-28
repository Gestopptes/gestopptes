[Source](https://arxiv.org/pdf/2009.03300) [Extracted with](https://chatgpt.com/share/e/4bc6b406-c8f4-43f9-9e53-5a2b2c05b619)
### Summary of "Measuring Massive Multitask Language Understanding"

**Abstract:**
The paper introduces a new benchmark to measure the multitask accuracy of text models across 57 tasks spanning various domains such as mathematics, history, computer science, and law. The results show that while large models like GPT-3 outperform random chance, there is a significant gap between their performance and expert-level accuracy. The paper highlights the limitations of current models, especially in socially important subjects like morality and law, and suggests the new benchmark can help in identifying these shortcomings.

**1. Introduction:**
- NLP models have achieved superhuman performance on many benchmarks but still lag in overall language understanding.
- Existing benchmarks like GLUE and SuperGLUE focus more on linguistic skills than comprehensive knowledge.
- Transformer models pretrained on vast text corpora have vast domain knowledge, but their real-world application capabilities remain untested.
- A new benchmark evaluates models on 57 subjects, ranging from elementary to advanced professional levels, to measure knowledge and problem-solving abilities.

**2. Related Work:**
- **Pretraining:** Large models are pretrained on massive text corpora, exposing them to a wide range of topics.
- **Benchmarks:** Recent benchmarks focus on commonsense reasoning, but models have quickly approached human-level performance.
- **Need for a New Benchmark:** Current benchmarks do not cover the wide-ranging knowledge required for real-world applications.

**3. A Multitask Test:**
- The test includes multiple-choice questions from humanities, social sciences, STEM, and other areas.
- Questions were manually collected from online sources, including practice exams for various professional tests.
- The dataset has 15,908 questions split into a few-shot development set, a validation set, and a test set.

**3.1 Humanities:**
- Includes law, philosophy, history, etc.
- Tests require understanding complex scenarios and applying appropriate precedents.

**3.2 Social Science:**
- Covers economics, sociology, psychology, etc.
- Questions require a mixture of world knowledge, qualitative reasoning, and quantitative reasoning.

**3.3 STEM:**
- Includes physics, computer science, mathematics, etc.
- Questions test conceptual understanding and problem-solving abilities at various levels.

**3.4 Other:**
- Includes professional medicine, business topics, and global facts.
- Questions require specialized knowledge and understanding.

**4. Experiments:**
- **Setup:** Evaluated GPT-3 and UnifiedQA models.
- **Model Sizes:** GPT-3 models range from 2.7 billion to 175 billion parameters.
- **Few-Shot Prompt:** Models are tested with few-shot learning, providing a few example questions and answers before the actual question.

**4.1 Results:**
- Larger models perform better, with GPT-3 X-Large achieving 43.9% accuracy.
- UnifiedQA, fine-tuned on other datasets, outperforms GPT-3 with an accuracy of 48.9%.
- Models have lopsided performance, excelling in some areas but performing poorly in others.

**4.2 Calibration:**
- Models are often miscalibrated, with confidence not correlating well with accuracy.

**5. Discussion:**
- **Multimodal Understanding:** Future benchmarks should include multimodal inputs.
- **Training Methods:** Models should learn from diverse text sources, similar to human learning.
- **Model Limitations:** Current models struggle with procedural knowledge and socially relevant subjects.

**6. Conclusion:**
- The new benchmark measures text models' knowledge across a broad range of subjects.
- Current models show progress but still have significant gaps, especially in socially important areas.
- The benchmark can help pinpoint model shortcomings and guide future research.

**Acknowledgements:**
- The authors thank several individuals for their contributions and support.
- The research was supported by the NSF GRFP Fellowship and an Open Philanthropy Project Fellowship.

**References:**
The paper cites various works related to pretraining, benchmarks, and the evaluation of NLP models.

### Tables

**Table 1: Average weighted accuracy for each model on all four broad disciplines.**

| Model                | Humanities | Social Science | STEM  | Other | Average |
|----------------------|------------|----------------|-------|-------|---------|
| Random Baseline      | 25.0       | 25.0           | 25.0  | 25.0  | 25.0    |
| RoBERTa              | 27.9       | 28.8           | 27.0  | 27.7  | 27.9    |
| ALBERT               | 27.2       | 25.7           | 27.7  | 27.9  | 27.1    |
| GPT-2                | 32.8       | 33.3           | 30.2  | 33.1  | 32.4    |
| UnifiedQA            | 45.6       | 56.6           | 40.2  | 54.6  | 48.9    |
| GPT-3 Small (few-shot) | 24.4       | 30.9           | 26.0  | 24.1  | 25.9    |
| GPT-3 Medium (few-shot) | 26.1       | 21.6           | 25.6  | 25.5  | 24.9    |
| GPT-3 Large (few-shot)  | 27.1       | 25.6           | 24.3  | 26.5  | 26.0    |
| GPT-3 X-Large (few-shot) | 40.8       | 50.4           | 36.7  | 48.8  | 43.9    |

**Figure 1:**
- Few Shot Prompt and Predicted Answer: Examples of questions and answers.
- GPT-3 Few Shot Test Performance: Comparison of model performance on different benchmarks.

**Figure 6:**
- Accuracy comparison of GPT-3 and UnifiedQA across 57 tasks.

### Detailed Examples of Questions:

**Table 2: Summary of All 57 Tasks**

| Task | Tested Concepts | Supercategory |
|------|-----------------|----------------|
| Abstract Algebra | Groups, rings, fields, vector spaces, ... | STEM |
| Anatomy | Central nervous system, circulatory system, ... | STEM |
| Astronomy | Solar system, galaxies, asteroids, ... | STEM |
| Business Ethics | Corporate responsibility, stakeholders, regulation, ... | Other |
| Clinical Knowledge | Spot diagnosis, joints, abdominal examination, ... | Other |
| College Biology | Cellular structure, molecular biology, ecology, ... | STEM |
| College Chemistry | Analytical, organic, inorganic, physical, ... | STEM |
| College Computer Science | Algorithms, systems, graphs, recursion, ... | STEM |
| College Mathematics | Differential equations, real analysis, combinatorics, ... | STEM |
| College Medicine | Introductory biochemistry, sociology, reasoning, ... | Other |
| College Physics | Electromagnetism, thermodynamics, special relativity, ... | STEM |
| Computer Security | Cryptography, malware, side channels, fuzzing, ... | STEM |
| Conceptual Physics | Newton’s laws, rotational motion, gravity, sound, ... | STEM |
| Econometrics | Volatility, long-run relationships, forecasting, ... | Social Sciences |
| Electrical Engineering | Circuits, power systems, electrical drives, ... | STEM |
| Elementary Mathematics | Word problems, multiplication, remainders, rounding, ... | STEM |
| Formal Logic | Propositions, predicate logic, first-order logic, ... | Humanities |
| Global Facts | Extreme poverty, literacy rates, life expectancy, ... | Other |
| High School Biology | Natural selection, heredity, cell cycle, Krebs cycle, ... | STEM |
| High School Chemistry | Chemical reactions, ions, acids and bases, ... | STEM |
| High School Computer Science | Arrays, conditionals, iteration, inheritance, ... | STEM |
| High School European History | Renaissance, reformation, industrialization, ... | Humanities |
| High School Geography | Population migration, rural land-use, urban processes, ... | Social Sciences |
| High School Gov’t and Politics | Branches of government, civil liberties, political ideologies, ... | Social Sciences |
| High School Macroeconomics | Economic indicators, national income, international trade, ... | Social Sciences |
| High School Mathematics | Pre-algebra, algebra, trigonometry, calculus, ... | STEM |
| High School Microeconomics | Supply and demand, imperfect competition, market failure, ... | Social Sciences |
| High School Physics | Kinematics, energy, torque, fluid pressure, ... | STEM |
| High School Psychology | Behavior, personality, emotions, learning, ... | Social Sciences |
| High School Statistics | Random variables, sampling distributions, chi-square tests, ... | STEM |
| High School US History | Civil War, the Great Depression, The Great Society, ... | Humanities |
| High School World History | Ottoman empire, economic imperialism, World War I, ... | Humanities |
| Human Aging | Senescence, dementia, longevity, personality changes, ... | Other |
| Human Sexuality | Pregnancy, sexual differentiation, sexual orientation, ... | Social Sciences |
| International Law | Human rights, sovereignty, law of the sea, use of force, ... | Humanities |
| Jurisprudence | Natural law, classical legal positivism, legal realism, ... | Humanities |
| Logical Fallacies | No true Scotsman, base rate fallacy, composition fallacy, ... | Humanities |
| Machine Learning | SVMs, VC dimension, deep learning architectures, ... | STEM |
| Management | Organizing, communication, organizational structure, ... | Other |
| Marketing | Segmentation, pricing, market research, ... | Other |
| Medical Genetics | Genes and cancer, common chromosome disorders, ... | Other |
| Miscellaneous | Agriculture, Fermi estimation, pop culture, ... | Other |
| Moral Disputes | Freedom of speech, addiction, the death penalty, ... | Humanities |
| Moral Scenarios | Detecting physical violence, stealing, externalities, ... | Humanities |
| Nutrition | Metabolism, water-soluble vitamins, diabetes, ... | Other |
| Philosophy | Skepticism, phronesis, skepticism, Singer’s Drowning Child, ... | Humanities |
| Prehistory | Neanderthals, Mesoamerica, extinction, stone tools, ... | Humanities |
| Professional Accounting | Auditing, reporting, regulation, valuation, ... | Other |
| Professional Law | Torts, criminal law, contracts, property, evidence, ... | Humanities |
| Professional Medicine | Diagnosis, pharmacotherapy, disease prevention, ... | Other |
| Professional Psychology | Diagnosis, biology and behavior, lifespan development, ... | Social Sciences |
| Public Relations | Media theory, crisis management, intelligence gathering, ... | Social Sciences |
| Security Studies | Environmental security, terrorism, weapons of mass destruction, ... | Social Sciences |
| Sociology | Socialization, cities and community, inequality and wealth, ... | Social Sciences |
| US Foreign Policy | Soft power, Cold War foreign policy, isolationism, ... | Social Sciences |
| Virology | Epidemiology, coronaviruses, retroviruses, herpesviruses, ... | Other |
| World Religions | Judaism, Christianity, Islam, Buddhism, Jainism, ... | Humanities |