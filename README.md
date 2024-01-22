# TOPSIS Web App

## Overview

This web application performs TOPSIS analysis for multiple-criteria decision making (MCDM). It uses Flask for the backend and offers a user-friendly interface to upload data files, set weights and impacts, and receive TOPSIS results via email.

## Installation

### Prerequisites

- Python installed
- Pip installed

### Clone the Repository

git clone [repository_url]
cd [repository_name]

### Install Dependencies

pip install -r requirements.txt

## Usage

1. Run the Flask application:

python app.py

2. Open your web browser and navigate to http://127.0.0.1:5000/ to access the web app.

## How to Use the Web App

1. Upload your input file (CSV or Excel) containing the data for TOPSIS analysis.
2. Enter the weights and impacts as required.
3. Provide your email address to receive the TOPSIS result.
4. Click the "Submit" button.

### Input File (data.csv)

| Fund Name | P1   | P2   | P3  | P4   | P5    |
| --------- | ---- | ---- | --- | ---- | ----- |
| M1        | 0.84 | 0.71 | 6.7 | 42.1 | 12.59 |
| M2        | 0.91 | 0.83 | 7   | 31.7 | 10.11 |
| M3        | 0.79 | 0.62 | 4.8 | 46.7 | 13.23 |
| M4        | 0.78 | 0.61 | 6.4 | 42.4 | 12.55 |
| M5        | 0.94 | 0.88 | 3.6 | 62.2 | 16.91 |
| M6        | 0.88 | 0.77 | 6.5 | 51.5 | 14.91 |
| M7        | 0.66 | 0.44 | 5.3 | 48.9 | 13.83 |
| M8        | 0.93 | 0.86 | 3.4 | 37   | 10.55 |

`weights` = "2,2,3,3,4"
`impacts `= "-,+,-,+,-"

### Output File (result.csv)

| Fund Name | P1   | P2   | P3  | P4   | P5    | score               | rank |
| --------- | ---- | ---- | --- | ---- | ----- | ------------------- | ---- |
| M1        | 0.84 | 0.71 | 6.7 | 42.1 | 12.59 | 0.46648384839516    | 6    |
| M2        | 0.91 | 0.83 | 7   | 31.7 | 10.11 | 0.5565665031302564  | 2    |
| M3        | 0.79 | 0.62 | 4.8 | 46.7 | 13.23 | 0.5552632203730501  | 3    |
| M4        | 0.78 | 0.61 | 6.4 | 42.4 | 12.55 | 0.5091638066448925  | 5    |
| M5        | 0.94 | 0.88 | 3.6 | 62.2 | 16.91 | 0.36399291864067096 | 7    |
| M6        | 0.88 | 0.77 | 6.5 | 51.5 | 14.91 | 0.26936075735436416 | 8    |
| M7        | 0.66 | 0.44 | 5.3 | 48.9 | 13.83 | 0.5251983566077868  | 4    |
| M8        | 0.93 | 0.86 | 3.4 | 37   | 10.55 | 0.6986963797749929  | 1    |

The output file contains columns of the input file along with two additional columns having **Topsis_score** and **Rank**.


