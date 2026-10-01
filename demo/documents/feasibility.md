# Round 2 feasibility and indicative economics

Prepared 1 October 2026. Round 1 is software only. These are proposed parts and a validation plan; no hardware has been built, ordered or purchased. `configs/feasibility.json` is the machine-readable cost source used by the website and judge packet.

## Local problem and proposed contribution

The World Bank identifies sites with major construction and traffic among the studied pollution settings in Dhaka. This supports a local motivation, not a claim that this prototype reduces citywide pollution or improves health. [World Bank, 8 December 2022](https://blogs.worldbank.org/en/endpovertyinsouthasia/bangladesh-urgent-call-clean-air).

Compare simple continuous spraying and threshold-based reactive control with forecast-guided zone control. Our software contribution is an inspectable causal forecast, a common simulation for all four strategies and trace-derived water/exposure comparisons. Continuous has the lowest mean simulated concentration, with greater water use. Predictive reduces water relative to continuous while using more than reactive in the higher-risk cases. Field effectiveness is unmeasured.

## Pilot architecture

Start with a limited three-monitor comparison: one near-source node and two exposed boundary nodes selected after siting. Expand to one source plus A north, B east, C south and D west only after the first calibration/logging gate. The two-node boundary pilot cannot establish four-boundary containment.

Each proposed node acquires PM readings and timestamps with a local buffer. Wind direction and speed enter the site hub through a verified interface. A local laptop/hub runs the existing Python artifact and baseline; the candidate ESP32 nodes acquire/relay data, not the joblib model. The hub records input freshness, predictions, source/boundary observations, commands, acknowledgments and measured water. A separate actuator bridge, heartbeat and manual override are proposed; firmware, pin assignments, relay wiring and the physical circuit are not implemented or validated.

The training monitor is OPC-N3. The lower-cost candidate SEN0177 is a different instrument with a listed 0–1000 µg/m³ range and response up to 10 seconds. Several training/replay peaks exceed that range, and the accepted task needs fresh one-second snapshots. It cannot be substituted into the trained pipeline as an equivalent sensor. Obtain an adequate construction-range monitor or define a new native-cadence task with new calibration and untouched evaluation measurements. [DFRobot sensor listing](https://www.dfrobot.com/product-1272.html).

Humidity, temperature and sensor selectivity can change readings; reference comparison and field calibration are necessary. Locate monitors so mist droplets do not become apparent dust changes, and log humidity alongside PM. [US EPA air-sensor guidance](https://www.epa.gov/air-sensor-toolbox/frequent-questions-about-air-sensors).

## Dated component listing basis

Prices checked on 1 October 2026. Public supplier listings are indicative prices, not formal quotations. Use listed single-unit prices without bulk discounts; retain USD and BDT separately without an invented exchange rate. Stock and specifications may change. DFRobot currently announces shipping resumes 8 October; this does not affect a software-only Round 1.

| Item | Three-monitor pilot qty | Five-monitor proposal qty | Listed unit price | Evidence / qualification |
|---|---:|---:|---:|---|
| Candidate laser PM SEN0177 | 3 | 5 | USD 46.90 | [DFRobot](https://www.dfrobot.com/product-1272.html); out of stock; range/cadence gap above |
| ESP32-E DFR0654 node | 3 | 5 | USD 8.90 | [DFRobot](https://www.dfrobot.com/product-2195.html); acquisition/link candidate |
| RS485 wind speed SEN0483 | 1 | 1 | USD 45.00 | [DFRobot](https://www.dfrobot.com/product-2339.html); adapter/siting needed |
| RS485 wind direction SEN0482 | 1 | 1 | USD 45.00 | [DFRobot](https://www.dfrobot.com/product-2340.html); calibration needed |
| 12 V diaphragm pump set | 1 | 1 | BDT 1360.04 | [TechShopBD](https://techshopbd.com/product/high-pressure-single-motor-water-pump-set-fl-4200); includes adapter/pipe/spray gun, not calibrated mist heads |
| Normally closed 12 V valve | 4 | 4 | BDT 450.05 | [TechShopBD](https://techshopbd.com/product/solenoid-valve-12v-34-inch/); out of stock |
| Four-channel 12 V relay | 1 | 1 | BDT 280.04 | [TechShopBD](https://techshopbd.com/product/relay-module-4-channel-12v); 3.3 V logic and protection unverified |

Three-monitor listed subtotal: **USD 257.40 plus BDT 3440.28**. Five-monitor listed subtotal: **USD 369.00 plus BDT 3440.28**. Neither is a complete installed-system cost. These do not include an adequate replacement for the sensor range/cadence gap, nozzle manifold, flow meter, filtering, pressure verification, suitable supplies/protection, RS485 adapters, node links, enclosures, mounting, reference calibration, labour, shipping, import duties or tax. Obtain formal supplier quotes after the team authorizes the physical design.

The pump listing names FL4200 in the URL but OD3.6 in its table. It states 12 V and 1.6–3 A (19.2–36 W), and also 80 W; its pressure figures conflict. Confirm model, measured pressure/flow and electrical demand before selecting it. No compatible wiring or field coverage is inferred from these listings. The simulator's total four-zone flow is 2 L/min at the default 0.5 L/min per zone; a catalogue free-flow figure does not prove this flow at a misting pressure.

## Water, energy and running cost

Water is the sum of each valve's active seconds × flow in L/min ÷ 60. The default eight-minute east case gives continuous **16.000 L**, reactive **1.250 L** and predictive **1.842 L**, from the saved traces. This is a software assumption, not measured consumption. Do not multiply it into daily savings without a declared activity and operating schedule.

Energy estimate: `pump watts × pump-on seconds / 3,600,000` kWh. At an explicitly assumed 80 W for eight minutes continuously, the illustrative energy is **0.01067 kWh**. The pump's power is unverified; electronics, valves and reference devices add their own demand. For actual economics measure power and flow and use current local tariffs. Cost per run = litres × water price/1000 L + kWh × electricity price/kWh + allocated maintenance/calibration. No tariff, payback or return on investment is invented.

Before each proposed pilot session, inspect leaks/filters, sensor inlets, pressure and manual stop, then confirm timestamps and sensor/reference agreement. Review fouling and drift after every session; set longer cleaning and calibration intervals from observed drift and manufacturer guidance. Installation and recurring labour remain quote dependencies.

## Gate before hardware and field claims

The team must explicitly start Round 2. Then establish an appropriate sensor range/cadence, confirmed pressure-rated components, measured nozzle coverage/flow, isolated protected power and a manual stop. Collect synchronized source/wind/boundary/reference data from independent activities and sites. Freeze the new split and strategies before evaluation. Compare baseline error, forecast warning timing, measured exposure above background, actual litres and switching under the same activity/weather conditions. Record failures, humidity interference and uncertainty. Qualification and judge feedback remain unknown until supplied by the team.
