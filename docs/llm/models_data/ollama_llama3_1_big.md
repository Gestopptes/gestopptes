[Source](https://storage.googleapis.com/ollama-assets/assets/mchiang0610/mikey3.1/73b11a5e-84e9-4397-9d47-f0299a6294b3?Expires=1722190227&GoogleAccessId=web-image-upload%40ollama.iam.gserviceaccount.com&Signature=IsTe33diBKqqinyYmqSCgupRxwfj%2BNc3AIXalwTSzIdHu93w%2B3JP2cAMIilcDzZZjgKHdq17EoeD6vyIKQzUQD5%2Bwx8DvCuK39KG%2BmOH5m0H4%2BRlKRSeoiyDUohAborau%2FZ5RlFstcDDcbswIpuGu7TIbpTHKWlQIRLkXsGg%2BdqBlUcayqoHx8AYArdJVt7LfunhqJUCFF4V%2F7AUwm0%2Fv5YQoZ0En%2FCRtbzI%2B1E2ivZkLp4hDlPg4qFtD1xmo3HPk8RJ9uIfCSB3N%2FEcRFUE4KHYmynOjCfE9xQxl8YOee88aX%2F985zPduG5pWbe1TrPge556iFdYKu6klQLxofAFw%3D%3D)
| Category       | Benchmark                  | Llama 3.1 405B | Nemotron 4 340B Instruct | GPT-4 (0125) | GPT-4 Omni | Claude 3.5 Sonnet |
|----------------|----------------------------|---------------|--------------------------|--------------|------------|--------------------|
| General        | MMLU (0-shot, CoT)         | 88.6          | 78.7 (non-CoT)           | 85.4         | 88.7       | 88.3               |
|                | MMLU PRO (5-shot, CoT)     | 73.3          | 62.7                     | 64.8         | 74.0       | 77.0               |
|                | IFEval                     | 88.6          | 85.1                     | 84.3         | 85.6       | 88.0               |
| Code           | HumanEval (0-shot)         | 89.0          | 73.2                     | 86.6         | 90.2       | 92.0               |
|                | MBPP EvalPlus (base) (0-shot) | 88.6        | 72.8                     | 83.6         | 87.8       | 90.5               |
| Math           | GSM8K (8-shot, CoT)        | 96.8          | 92.3 (0-shot)            | 94.2         | 96.1       | 96.4 (0-shot)      |
|                | MATH (0-shot, CoT)         | 73.8          | 41.1                     | 64.5         | 76.6       | 71.1               |
| Reasoning      | ARC Challenge (0-shot)     | 96.9          | 94.6                     | 96.4         | 96.7       | 96.7               |
|                | GPOQA (0-shot, CoT)        | 51.1          | -                        | -            | 41.4       | 59.4               |
| Tool use       | BFCL                       | 88.5          | 86.5                     | 88.3         | 80.5       | 90.2               |
|                | Nexus                      | 58.7          | -                        | -            | 50.3       | 45.7               |
| Long context   | ZeroSCROLLS/QuaLITY        | 95.2          | -                        | 95.2         | 90.5       | 90.5               |
|                | InfiniteBench/En.MC        | 83.4          | -                        | 72.1         | 82.5       | -                  |
|                | NIH/Multi-needle           | 98.1          | -                        | 100.0        | 100.0      | 90.8               |
| Multilingual   | Multilingual MGSM          | 91.6          | -                        | 85.9         | 90.5       | 91.6               |
