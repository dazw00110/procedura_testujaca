# Automated Discretization Framework

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

Framework for testing and evaluating data discretization algorithms. Automates quality assessment and generates comparative reports for different discretization methods.

## 📌 Key Features
- **Multi-algorithm testing** - support for multiple discretization algorithms
- **Automatic validation** of results
- **CSV report generation** with quality metrics
- **Scoring system** considering:
  - Number of non-deterministic pairs (`det`)
  - Total cut points (`cuts`)
  - Execution time (`time`)
- **Continuous integration** ready

## 🚀 Installation
1. Requirements:
   - Python 3.8+
   - Required packages: `pandas`, `numpy`, `scipy`

2. Install dependencies:
```bash
pip install -r requirements.txt
```

# 🧮 Project Structure
```bash 
discretization-framework/
├── test_data/
│   ├── data1.csv            # Sample input data
│   ├── data2.csv            # Sample input data
│   ├── data3.csv            # Sample input data
│   ├── DISC_*.csv           # Auto-generated results
│   └── raport_*.csv         # Test reports
│   └── DISCdata1.csv        # Discretized data
│   └── DISCdata2.csv        # Discretized data
│   └── DISCdata3.csv        # Discretized data
├── top_down_discretizer.py  # Sample discretization algorithm
├── csv_reader.py            # Data loading utilities
├── verifier.py              # Validation module
├── non_pairs.py             # Metrics calculations
└── main.py                  # Main testing script
```

# 🔧 Usage
1.Prepare test data in CSV format in the test_data directory

2.Run main script:
```pyth
python main.py
```
3.Example output report (generated in test_data/raport_*.csv):
```
=== TEST REPORT FOR top_down_discretizer ===
     File  det  cuts    time  Score
   data1    0    12  0.0045   3.06
   data2    2    18  0.0051  11.05
   data3    5    25  0.0052  15.05
     Σ      7    55  0.0148  29.16
```

# 📈 Evaluation Metrics
Algorithm score is calculated using:
```python
score = 0.5 * det + 0.25 * cuts + execution_time
```
Where:
- det: Number of non-deterministic pairs (lower is better)
- cuts: Total number of cut points (lower is better)
- execution_time: Algorithm runtime in seconds (lower is better)

# ➕ Extending the Framework
To add new algorithm:
1. Create new Python file (e.g., new_algorithm.py)
2. Implement discretization logic that:
   - Reads input CSV from test_data
   - Writes output CSV with DISC prefix
3. Update algorithm list in main.py:
```python
python
algorithms = [
    'top_down_discretizer.py',
    'new_algorithm.py' 
]
```

# 🧪 Test Cases
Sample test criteria:
1. Shape consistency between input/output
2. Valid numerical intervals
3. No data corruption during processing
4. Performance benchmarks

# 📜 License
MIT License

