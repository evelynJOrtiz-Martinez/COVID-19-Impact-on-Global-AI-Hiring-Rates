# COVID-19-Impact-on-Global-AI-Hiring-Rates
This analysis examines the impact of COVID-19 on AI hiring rates across 28 countries using data from Stanford's AI Index Report 2024. The project was part of the winning solution for the WMU Business Analytics Case Competition, where our team (Gigabyte) secured first place.

## Problem Statement
Using the "fig.4.2.13.csv" dataset containing "Relative AI hiring rate year-over-year ratio by geographic area, 2018–23", analyze the impact of COVID-19 (2020-2022) on global AI hiring trends. Develop metrics to quantify and summarize this impact across different regions.

## Data Source
- Dataset: fig.4.2.13.csv from Stanford University (AI Index Report | Stanford HAI)
- Time period: 2018-2023
- Coverage: 28 countries
- Metrics: Relative AI hiring rate year-over-year ratio

## Requirements
- Python 3.x
- pandas
- numpy
- scipy
- matplotlib
- seaborn

## Installation
```bash
pip install pandas numpy scipy matplotlib seaborn
```

## Usage
1. Clone the repository:
```bash
git clone https://github.com/yourusername/covid-ai-hiring-analysis.git
cd covid-ai-hiring-analysis
```

2. Place the data file (fig_4.2.13.csv) in the project directory

3. Run the analysis:
```bash
python analysis.py
```

## Methodology
The analysis follows these key steps:
1. Data preprocessing and cleaning
2. Period-based analysis (Pre-COVID, During-COVID, Post-COVID)
3. Statistical analysis including t-tests
4. Visualization generation
5. Impact metric calculations

## Results
The analysis produces several visualizations:
1. impact_by_country.png - Overall impact visualization
2. period_distribution.png - Distribution of rates across different periods
3. top_10_impacted.png - Most impacted countries
4. recovery_analysis.png - Impact vs recovery analysis

## Project Structure
```
.
├── README.md
├── analysis.py          # Main analysis script
├── requirements.txt     # Project dependencies
├── data/               # Data directory
│   └── fig_4.2.13.csv  # Input data (not included in repo)
├── output/             # Generated visualizations
│   ├── impact_by_country.png
│   ├── period_distribution.png
│   ├── top_10_impacted.png
│   └── recovery_analysis.png
└── LICENSE             # MIT License
```

## Team Gigabyte
- Evelyn Ortiz-Martinez
- Raiyan Hrid
- Nick Ford
- Arshpreet Singh

## License
This project is licensed under the MIT License - see the LICENSE file for details.
