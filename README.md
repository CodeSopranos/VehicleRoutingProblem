# VehicleRoutingProblem

The research work on Capacitated Vehicle Routing Problem (C-VRP) solving via Artifical Bee Colony (ABC) Algorithm which enhanced with *Local Search*.

---
**Problem example:**
![](output/images/problemn35-k5.vrp.png)
**Random solution:**
![](output/images/beforeABC_n35-k5.vrp.png)
**Fitness function of ABC:**
![](output/images/history_n35-k5.vrp.png)
**And solution (200 epochs):**
![](output/images/afterABC_n35-k5.vrp.png)
**Reference**:
[An artificial bee colony algorithm for the capacitated
vehicle routing problem](http://citeseerx.ist.psu.edu/viewdoc/downloa[d?doi=10.1.1.457.8027&rep=rep1&type=pdf)

# A-benchmarks

---

|    | benchmark     |   n_locations |   n_trucks |   capacity |   optimal_cost |   ABC_cost |     error | is_feasible   |
|---:|:--------------|--------------:|-----------:|-----------:|---------------:|-----------:|----------:|:--------------|
|  0 | A-n32-k5.vrp  |            32 |          5 |        100 |            784 |    842.433 | 0.0745315 | True          |
|  1 | A-n33-k5.vrp  |            33 |          5 |        100 |            661 |    713.307 | 0.0791329 | True          |
|  2 | A-n33-k6.vrp  |            33 |          6 |        100 |            742 |    787.046 | 0.0607091 | True          |
|  3 | A-n34-k5.vrp  |            34 |          5 |        100 |            778 |    809.088 | 0.0399594 | True          |
|  4 | A-n36-k5.vrp  |            36 |          5 |        100 |            799 |    828.697 | 0.0371682 | True          |
|  5 | A-n37-k5.vrp  |            37 |          5 |        100 |            669 |    732.588 | 0.0950493 | True          |
|  6 | A-n37-k6.vrp  |            37 |          6 |        100 |            949 |   1046.12  | 0.102344  | True          |
|  7 | A-n38-k5.vrp  |            38 |          5 |        100 |            730 |    829.51  | 0.136315  | True          |
|  8 | A-n39-k5.vrp  |            39 |          5 |        100 |            822 |    877.592 | 0.0676301 | True          |
|  9 | A-n39-k6.vrp  |            39 |          6 |        100 |            831 |    873.5   | 0.0511426 | True          |
| 10 | A-n44-k6.vrp  |            44 |          6 |        100 |            937 |   1025.23  | 0.0941666 | True          |
| 11 | A-n45-k6.vrp  |            45 |          6 |        100 |            944 |   1203.13  | 0.274502  | True          |
| 12 | A-n45-k7.vrp  |            45 |          7 |        100 |           1146 |   1238.66  | 0.0808508 | True          |
| 13 | A-n46-k7.vrp  |            46 |          7 |        100 |            914 |   1018.24  | 0.114046  | True          |
| 14 | A-n48-k7.vrp  |            48 |          7 |        100 |           1073 |   1272.04  | 0.185502  | True          |
| 15 | A-n53-k7.vrp  |            53 |          7 |        100 |           1010 |   1272.69  | 0.260087  | True          |
| 16 | A-n54-k7.vrp  |            54 |          7 |        100 |           1167 |   1349.58  | 0.156455  | True          |
| 17 | A-n55-k9.vrp  |            55 |          9 |        100 |           1073 |   1277.18  | 0.190285  | True          |
| 18 | A-n60-k9.vrp  |            60 |          9 |        100 |           1354 |   1595.71  | 0.178513  | True          |
| 19 | A-n61-k9.vrp  |            61 |          9 |        100 |           1034 |   1335.7   | 0.291779  | True          |
| 20 | A-n62-k8.vrp  |            62 |          8 |        100 |           1288 |   1530.41  | 0.188209  | True          |
| 21 | A-n63-k10.vrp |            63 |         10 |        100 |           1314 |   1567.9   | 0.193228  | True          |
| 22 | A-n63-k9.vrp  |            63 |          9 |        100 |           1616 |   1906.81  | 0.179959  | True          |
| 23 | A-n64-k9.vrp  |            64 |          9 |        100 |           1401 |   1754.17  | 0.252086  | True          |
| 24 | A-n65-k9.vrp  |            65 |          9 |        100 |           1174 |   1528.02  | 0.301549  | True          |
| 25 | A-n69-k9.vrp  |            69 |          9 |        100 |           1159 |   1547.32  | 0.335051  | True          |
| 26 | A-n80-k10.vrp |            80 |         10 |        100 |           1763 |   2280.44  | 0.2935    | True  


# B-benchmarks

---

|    | benchmark     |   n_locations |   n_trucks |   capacity |   optimal_cost |   ABC_cost |     error | is_feasible   |
|---:|:--------------|--------------:|-----------:|-----------:|---------------:|-----------:|----------:|:--------------|
|  0 | B-n31-k5.vrp  |            31 |          5 |        100 |            672 |    696.441 | 0.0363712 | True          |
|  1 | B-n34-k5.vrp  |            34 |          5 |        100 |            788 |    826.332 | 0.0486451 | True          |
|  2 | B-n35-k5.vrp  |            35 |          5 |        100 |            955 |   1004.02  | 0.0513304 | True          |
|  3 | B-n38-k6.vrp  |            38 |          6 |        100 |            805 |    857.6   | 0.0653414 | True          |
|  4 | B-n39-k5.vrp  |            39 |          5 |        100 |            549 |    570.94  | 0.039963  | True          |
|  5 | B-n41-k6.vrp  |            41 |          6 |        100 |            829 |   1011.49  | 0.220132  | True          |
|  6 | B-n43-k6.vrp  |            43 |          6 |        100 |            742 |    778.271 | 0.0488821 | True          |
|  7 | B-n44-k7.vrp  |            44 |          7 |        100 |            909 |   1026.42  | 0.129177  | True          |
|  8 | B-n45-k5.vrp  |            45 |          5 |        100 |            751 |    774.988 | 0.0319418 | True          |
|  9 | B-n45-k6.vrp  |            45 |          6 |        100 |            678 |   1000.68  | 0.475932  | True          |
| 10 | B-n50-k7.vrp  |            50 |          7 |        100 |            741 |    761.781 | 0.0280448 | True          |
| 11 | B-n50-k8.vrp  |            50 |          8 |        100 |           1312 |   1364.05  | 0.0396721 | True          |
| 12 | B-n52-k7.vrp  |            52 |          7 |        100 |            747 |    788.78  | 0.0559301 | True          |
| 13 | B-n56-k7.vrp  |            56 |          7 |        100 |            707 |    749.917 | 0.0607036 | True          |
| 14 | B-n57-k7.vrp  |            57 |          7 |        100 |           1153 |   1532.13  | 0.328819  | True          |
| 15 | B-n57-k9.vrp  |            57 |          9 |        100 |           1598 |   1747.21  | 0.0933744 | True          |
| 16 | B-n63-k10.vrp |            63 |         10 |        100 |           1496 |   1731.21  | 0.157224  | True          |
| 17 | B-n64-k9.vrp  |            64 |          9 |        100 |            861 |   1136.82  | 0.32035   | True          |
| 18 | B-n66-k9.vrp  |            66 |          9 |        100 |           1316 |   1616.46  | 0.228315  | True          |
| 19 | B-n67-k10.vrp |            67 |         10 |        100 |           1032 |   1179.78  | 0.1432    | True          |
| 20 | B-n68-k9.vrp  |            68 |          9 |        100 |           1272 |   1753.32  | 0.378397  | True          |
| 21 | B-n78-k10.vrp |            78 |         10 |        100 |           1221 |   1576.07  | 0.290804  | True          |
