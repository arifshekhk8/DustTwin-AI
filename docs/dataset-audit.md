# Construction dataset audit

Audited 1 October 2026, Asia/Dhaka. No model training or accuracy evaluation was performed in this audit.

## 2020 candidate: rejected for the planned raw 30-second task

Source: Daniel Cheriyan, [Mendeley Data V1](https://data.mendeley.com/datasets/6fd493866k/1), DOI `10.17632/6fd493866k.1`, CC BY 4.0. File: `DIB -data.xlsx`, 189,414 bytes. The downloaded SHA-256 matches the repository's published hash:

```text
42c273d1f89c7d57181478334547934a049637f109e31d7f8132f9c29ecdb613
```

The published page describes PM10, PM2.5 and PM1, and the [associated article](https://pmc.ncbi.nlm.nih.gov/articles/PMC7644872/) calls the linked resource raw. The actual workbook has three sheets: `Alpha sensor 10 min moving avg`, `Sharp sensor 10 min moving avg`, and `Description of dataset`. Its description explicitly identifies both measurement sheets as **PM10 filtered to ten-minute moving averages**. PM2.5, PM1 and unfiltered channels are absent from this file.

The moving-average alignment and edge treatment are unspecified. There are no formulas from which to reconstruct how the averaging was done. A two-second output cadence does not undo ten minutes of smoothing. We cannot prove that past inputs exclude future raw readings, and a 30-second target would chiefly measure predictability of an already smoothed signal. This file is rejected for raw short-horizon forecasting. It remains an attributed descriptive construction trace, with its processing clearly identified.

### Actual structure and coverage

Both measurement sheets contain 1,201 populated data rows, Excel rows 3–1203. Their recorded time-of-day runs from 03:20:00 through 04:00:00, inclusive, with 1,200 consecutive two-second intervals. Calendar date and timezone are absent. There are no duplicate times, reversed times or cadence gaps. Stored sheet dimensions extend beyond populated records; formatted empty rows/columns are not observations.

| Channel | Observed | Missing | Minimum PM10, µg/m³ | Maximum PM10, µg/m³ |
|---|---:|---:|---:|---:|
| OPC-N2 A1 | 1,201 | 0 | 195.74 | 6,532.42 |
| OPC-N2 A2 | 1,201 | 0 | 344.56 | 10,931.21 |
| OPC-N2 A3 | 931 | 270 | 246.12 | 3,288.91 |
| Sharp D1 | 1,201 | 0 | 40.03 | 349.53 |
| Sharp D2 | 1,201 | 0 | 25.33 | 295.70 |
| Sharp D3 | 1,201 | 0 | 0.50 | 195.93 |

A3 is missing its first 270 rows, from 03:20:00 through 03:28:58. No observed numeric values are negative, zero or nonfinite. The published article reports that the Sharp sensor saturation range was exceeded during the experiment and excludes Sharp from further analysis. Averaged released Sharp values cannot recover those saturated raw measurements. OPC channels contain no identical ceiling plateau, which alone does not establish calibration or a valid upper range.

The workbook describes four minutes of preparation, sixteen minutes of mixing and twenty minutes of block laying. Monitors were 1 m horizontally from the source and 0.8 m above the floor. There is **one construction experiment**, with simultaneous co-located sensors. The file contains no wind, boundary monitors, misting intervention, independent field episodes or source-emission-rate measurement. It does not validate outdoor transport or containment.

### Reproduction and outputs

```sh
python3 scripts/download_data.py --dataset 6fd493866k
python3 scripts/audit_filtered_candidate.py
```

Install the audit requirements in a project environment before running the second command. Original files are unchanged and ignored by Git. Aggregate findings are in [the machine-readable summary](../reports/data-audit/mendeley-2020-summary.json). Derived plots, when generated, are credited to this dataset and labelled as moving-average data. These outputs are audit evidence, not model results.

## Replacement investigation

The newer [2024 construction/outdoor profiles dataset](https://data.mendeley.com/datasets/7f22n9v7hp/1), DOI `10.17632/7f22n9v7hp.1`, is being acquired for inspection. Its page names OPC-N3, Sniffer4d and PMS5003 instruments and PM1/PM2.5/PM10. Downloadable schema, preprocessing and independent episode coverage must pass an actual audit before acceptance.

The related 2019 candidate's page also explicitly describes ten-minute filtered PM10. It is not an assumed independent raw-data alternative. UCI's hourly ambient data remains a separate native-hourly fallback rather than evidence for the construction forecast.
