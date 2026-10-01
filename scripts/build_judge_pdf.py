"""Build the locally sourced, printable Round 1 evidence packet with ReportLab."""

import json
import csv
import gzip
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Image, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from reportlab.graphics.shapes import Drawing, Line, PolyLine, String

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output/pdf/dusttwin-judge-packet.pdf"
NAVY = colors.HexColor("#14232c")
MINT = colors.HexColor("#2b7150")
GREY = colors.HexColor("#536873")
PALE = colors.HexColor("#eaf4ee")
WIDTH = A4[0] - 88
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="DTTitle", fontName="Helvetica-Bold", fontSize=28, leading=32, textColor=NAVY, spaceAfter=14))
styles.add(ParagraphStyle(name="DTHeading", fontName="Helvetica-Bold", fontSize=14, leading=18, textColor=NAVY, spaceAfter=8, spaceBefore=10))
styles.add(ParagraphStyle(name="DTBody", fontName="Helvetica", fontSize=9.5, leading=14, textColor=NAVY, spaceAfter=8))
styles.add(ParagraphStyle(name="DTNote", fontName="Helvetica", fontSize=8.5, leading=12, textColor=GREY, spaceAfter=9))
styles.add(ParagraphStyle(name="DTCell", fontName="Helvetica", fontSize=8, leading=10.5, textColor=NAVY))
styles.add(ParagraphStyle(name="DTKicker", fontName="Helvetica-Bold", fontSize=8, leading=13, textColor=MINT, spaceAfter=13))


def p(text, style="DTBody"):
    return Paragraph(text, styles[style])


def table(rows, widths, highlight=()):
    converted = [[p(str(cell), "DTCell") for cell in row] for row in rows]
    t = Table(converted, colWidths=widths, repeatRows=1, hAlign="LEFT")
    commands = [("BACKGROUND", (0, 0), (-1, 0), PALE), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("LINEBELOW", (0, 0), (-1, 0), .5, colors.HexColor("#96bda6")),
                ("LINEBELOW", (0, 1), (-1, -1), .3, colors.HexColor("#d8e2dc"))]
    commands += [("BACKGROUND", (0, row), (-1, row), PALE) for row in highlight]
    t.setStyle(TableStyle(commands))
    return t


def image(path, width=WIDTH):
    w, h = ImageReader(str(path)).getSize()
    scale = min(width / w, 185 / h)
    return Image(str(path), width=w * scale, height=h * scale)


def header(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(NAVY)
    canvas.rect(0, A4[1] - 48, A4[0], 48, fill=1, stroke=0)
    canvas.setFillColor(colors.white)
    canvas.setFont("Helvetica-Bold", 11)
    canvas.drawString(44, A4[1] - 29, "DustTwin / CTRL_V")
    canvas.setFont("Helvetica", 8)
    canvas.drawRightString(A4[0] - 44, A4[1] - 29, "THEME 2  |  ROUND 1 SOFTWARE")
    canvas.setStrokeColor(colors.HexColor("#d1ddd5"))
    canvas.line(44, 42, A4[0] - 44, 42)
    canvas.setFillColor(GREY)
    canvas.setFont("Helvetica", 8)
    canvas.drawString(44, 27, "1 October 2026  |  Measured forecast + illustrative site simulation")
    canvas.drawRightString(A4[0] - 44, 27, str(doc.page))
    canvas.restoreState()


def recorded_window():
    """Vector plot of unchanged exported target-aligned rows; no new evaluation."""
    with gzip.open(ROOT / "reports/evaluation/test-forecast-traces.csv.gz", "rt") as stream:
        rows = [row for row in csv.DictReader(stream) if row["episode_id"] == "lab_e4_drill90" and 1030 <= int(row["target_second"]) <= 1230]
    drawing = Drawing(WIDTH, 192)
    left, right, bottom, top = 47, WIDTH - 10, 29, 170
    ceiling = max(float(r["actual_pm10_ug_m3"]) for r in rows) * 1.08
    x = lambda n: left + (n - 1030) / 200 * (right - left)
    y = lambda n: bottom + n / ceiling * (top - bottom)
    for fraction in (0, .25, .5, .75, 1):
        value = fraction * ceiling
        drawing.add(Line(left, y(value), right, y(value), strokeColor=colors.HexColor("#dce5df"), strokeWidth=.5))
        drawing.add(String(left - 7, y(value) - 3, str(round(value)), fontSize=7, textAnchor="end", fillColor=GREY))
    series = [("actual", "Actual", "#263741"), ("selected_model", "Model", "#2b7150"), ("persistence", "Persistence", "#587bae"), ("trailing_mean", "Mean", "#b88739")]
    for i, (key, label, colour) in enumerate(series):
        points = [coord for r in rows for coord in (x(int(r["target_second"])), y(float(r[key + "_pm10_ug_m3"])))]
        drawing.add(PolyLine(points, strokeColor=colors.HexColor(colour), strokeWidth=.8))
        px = left + i * 107
        drawing.add(Line(px, 183, px + 14, 183, strokeColor=colors.HexColor(colour), strokeWidth=1.5))
        drawing.add(String(px + 19, 180, label, fontSize=7, fillColor=GREY))
    for value in (1030, 1080, 1130, 1180, 1230):
        drawing.add(String(x(value), 15, f"{value//60:02}:{value%60:02}", fontSize=7, textAnchor="middle", fillColor=GREY))
    drawing.add(String(left, 2, "Recorded target elapsed time / PM10 ug/m3", fontSize=7, fillColor=GREY))
    return drawing


def main():
    def read(relative):
        return json.loads((ROOT / relative).read_text())
    e = read("demo/evidence.json")
    sim = read("demo/simulation/index.json")
    costs = read("configs/feasibility.json")
    team = read("configs/team.json")
    s = []
    s += [p("ROUND 1 / EVIDENCE PACKET", "DTKicker"), p("Forecast dust.<br/>Control the edge.", "DTTitle"),
          p("A working software prototype for an inspectable construction-dust forecast and proposed zone-based misting control."),
          table([["What is implemented", "What it establishes"], ["Frozen trained model + local inference", "A preliminary laboratory monitor forecast"], ["Measured-data replay + honest baselines", "Past input, model output and later recorded actual"], ["Four controllers in five common scenarios", "Simulated water/exposure tradeoffs under stated assumptions"], ["Original website + offline saved backup", "An integrated, reviewable Round 1 demonstration"]], [230, WIDTH - 230]),
          Spacer(1, 18), p("Why this problem", "DTHeading"),
          p('World Bank reporting identifies major construction with traffic among studied pollution settings in Dhaka. This motivates the site-monitoring proposal; it does not prove our system reduces pollution or improves health. <link href="https://blogs.worldbank.org/en/endpovertyinsouthasia/bangladesh-urgent-call-clean-air" color="#2b7150">World Bank source [1]</link>.'),
          p("Proposed contribution", "DTHeading"), p("Compare forecast-guided zone selection with continuous and reactive control, while exposing the forecast input, failures, water accounting and controller assumptions."),
          p("Round 1 boundary", "DTHeading"), p("No physical hardware has been built or purchased. Outdoor boundary accuracy and physical misting effectiveness remain unvalidated. Hardware starts only with the team's explicit Round 2 instruction."),
          p("Team CTRL_V", "DTHeading"), p("<br/>".join(team["members"])), p("Team ID: not issued by organizers according to the team. Contact details and qualification/feedback are not supplied.", "DTNote"), PageBreak()]
    metrics = e["test"]["models"]
    s += [p("01 / MEASURED FORECAST", "DTKicker"), p("A real model.<br/>A mixed test result.", "DTTitle"),
          p('Askarov and Choi (2024), Mendeley V1, DOI 10.17632/7f22n9v7hp.1, CC BY 4.0. Twelve laboratory OPC-N3 recordings; raw PM10. <link href="https://data.mendeley.com/datasets/7f22n9v7hp/1" color="#2b7150">Data source [2]</link>.'),
          p("Causal one-second grid; observation age at most 1.5 s. Each forecast uses 121 snapshots over the previous 120 s and predicts the latest-observed snapshot 30 s ahead. Sixteen PM10-only lag/statistic features; no event clock, drilling label or future wind as learned input."),
          p("Whole groups 1/2 train (24,818 windows), 3 selects (12,113), 4 tests (15,065). The test group is labelled increased temperature. Missing calendar dates mean this is a group holdout, not strict global chronology."),
          table([["Predictor", "Test MAE (ug/m3)", "Test RMSE (ug/m3)"]] + [[name, f'{metrics[key]["mae_ug_m3"]:.3f}', f'{metrics[key]["rmse_ug_m3"]:.3f}'] for key,name in [("persistence","Persistence"),("trailing_mean","Trailing mean"),("selected_model","Trained boosting model")]], [210,145,WIDTH-355], highlight=(3,)),
          Spacer(1,12), p("Model MAE is 7.62% below persistence and 8.39% above the trailing mean. The mean is the stronger MAE baseline. No test-driven refit or retuning was done. Error improvement is not pollution reduction."),
          recorded_window(),
          p("Figure: target-aligned held-out 90-second-label window; each forecast was issued 30 s before its target. Full profiles and failure windows are included in reports/evaluation. Overlapping windows are correlated within only three records. Abrupt rises/peaks and the ten-second-label record are weaknesses.", "DTNote"),
          p("At a predeclared illustrative 500 ug/m3 warning setting: model 13/18 matched crossing runs, 15 false alerts; mean 13/18, 8 false alerts. Only one of three first onsets receives advance learned warning. A 30-second horizon is not reliable 30-second warning lead.", "DTNote"), PageBreak()]
    rows = [["Case / strategy", "Water (L)", "Mean max PM10", "Above 250 (s)", "Switches"]]
    highlights = []
    names = {"no_control":"No control","continuous":"Continuous","reactive":"Reactive","predictive":"Predictive"}
    for case in sim["scenarios"]:
        for key in names:
            m = case["metrics"][key]
            rows.append([f'{case["id"]} / {names[key]}',f'{m["water_litres"]:.3f}',f'{m["mean_max_boundary_pm10_ug_m3"]:.1f}',m["exceedance_seconds"],m["zone_switches"]])
            if key == "predictive":
                highlights.append(len(rows)-1)
    t = table(rows, [181,72,98,83,WIDTH-434], highlights)
    t.setStyle(TableStyle([("TOPPADDING",(0,0),(-1,-1),3),("BOTTOMPADDING",(0,0),(-1,-1),3)]))
    s += [p("02 / COMMON SITE EXPERIMENT", "DTKicker"), p("One environment.<br/>Four control strategies.", "DTTitle"),
          p("All cases use the same source/weather for every controller, equal actuator limits, a 480-second window and four boundaries. PM10 units are ug/m3; the mean is the time average of the maximum boundary each second. Settings are illustrative, not regulatory."), t, Spacer(1, 13),
          p("Continuous has the lowest mean concentration and highest water use. Predictive uses less water than continuous but more than reactive in the higher-risk cases. The frozen cases include low risk, eastward plume, two boundaries, wind shift and identical sensor loss.", "DTNote"),
          p("Assumptions: 120 x 80 m site; background 40; wind 3 m/s; flow 0.5 L/min/zone; incoming construction fraction removed 0.65; actuator delay 5 s; minimum on/off 15 s. Background is preserved. Water integrates commanded flow. Source proxy is concentration, not an emission rate.", "DTNote"),
          p("The learned source endpoint is mapped through an assumed linear path, held-current wind and untreated boundary rollout. This transfer is uncalibrated and does not establish physical suppression or field boundary accuracy.", "DTNote"), PageBreak()]
    s += [p("03 / WORKING SOFTWARE", "DTKicker"), p("Show the input.<br/>Reveal the outcome.", "DTTitle"),
          table([["Step", "Judge demonstration"], ["Measured replay", "Observe current PM10, the model's +30 s endpoint and both baselines. Open the 121-input/16-feature detail and artifact identity."], ["Time catches up", "Advance the recorded clock to reveal an earlier forecast's recorded target. Future actual is never supplied to the model."], ["Site experiment", "Diagonal case at 100 s: A north and B east are exposed. Compare strategies at the same clock, then inspect the full eight-minute table."], ["Recovery", "Local live mode executes the fitted Python model without internet after setup. Saved fallback shows previously computed results and disables new assumption runs."]], [120,WIDTH-120]),
          p("Verification evidence", "DTHeading"),
          p("Twenty focused Python tests pass. Independent simulation checks verify all 20 runs / 9,600 intervals: water, metrics, switching, background, capacity and hashes. Five browser journeys pass: all five fixed fixture predictions to 1e-8, API/display agreement, no early target reveal, playback, stale-response rejection, custom flow, saved/live equality and mobile pages."),
          p("Offline rehearsal", "DTHeading"), p("A real ten-minute browser journey denies every external network request while using local live inference and saved recovery. Its exact result is in reports/readiness. Physical Wi-Fi is not disabled. A software check does not verify the team's spoken pitch or venue projector."),
          p("On the prepared Mac", "DTHeading"), p("Double-click Start DustTwin.command. Keep the terminal open and confirm Local model ready. For recovery use Start Saved Replay.command and explicitly identify Saved replay mode."),
          p("On another computer", "DTHeading"), p("Unzip the release. Saved mode needs only Python 3 and a modern browser; no Node or package install. Live mode requires Python 3.14 and pinned service packages installed once. The archive contains the built website, permitted data/evidence and the frozen model; it does not bundle a Python runtime."),
          p("Artifact SHA-256", "DTHeading"), p(e["metadata"]["artifact_sha256"], "DTNote"), p("54,679 bytes / hist_gb_depth3_iter100. Source, configuration, artifact and trace hashes are public. Input snapshot IDs and source attribution are inspectable in the live replay.", "DTNote"), PageBreak()]
    costrows = [["Candidate item", "Qty", "Listed unit price", "Important qualification"]]
    for item in costs["items"][:7]:
        costrows.append([item["name"],item["quantity"],f'{item["currency"]} {item["unit_price"]:.2f}',item["note"]])
    ct=table(costrows,[151,28,90,WIDTH-269]);ct.setStyle(TableStyle([("TOPPADDING",(0,0),(-1,-1),6),("BOTTOMPADDING",(0,0),(-1,-1),6)]))
    s += [p("04 / PROPOSED ROUND 2", "DTKicker"), p("Cost basis.<br/>Calibration before deployment.", "DTTitle"),
          p("Listed prices checked 1 October 2026; not formal quotations, purchased hardware or a complete installed-system cost. References [3]-[9]. USD and BDT remain separate; no exchange rate or payback is invented."), ct, Spacer(1,12),
          p("Five-monitor listed subtotal: USD 369.00 plus BDT 3440.28. Three-monitor pilot: USD 257.40 plus BDT 3440.28. Excludes suitable construction-range replacements, mist heads/manifold, flow meter, protection, enclosures, links, reference calibration, labour, shipping/duties/tax."),
          p("The proposed low-cost PM sensor differs from OPC-N3: its listed 0-1000 ug/m3 range and up-to-10 s response cannot support all replay peaks or the current one-second task without new data/task validation. It is listed out of stock, as are the valves. Confirm pressure compatibility and relay logic/protection before any physical build.", "DTNote"),
          p("The pump listing's electrical/pressure specifications conflict. Measure demand, flow and coverage instead of assuming catalogue maxima. Energy = watts x on-seconds / 3,600,000 kWh; at an explicitly assumed 80 W for 480 s, 0.01067 kWh. Add valves/electronics. Actual tariffs, installation and maintenance still need quotes.", "DTNote"),
          p('Reference calibration, sensor saturation, humidity and mist interference, clean inlets/filters and independent site events are pilot gates. <link href="https://www.epa.gov/air-sensor-toolbox/frequent-questions-about-air-sensors" color="#2b7150">EPA sensor guidance [10]</link>. No physical design or firmware is validated by this packet.', "DTNote"), PageBreak()]
    story=[("0:00-0:45","Introduce CTRL_V and the software prototype"),("0:45-1:45","Local problem; continuous/reactive approaches; proposed contribution"),("1:45-2:45","Dataset, causal task, split and laboratory limitation"),("2:45-4:15","Live measured replay, inputs, baselines and later actual"),("4:15-5:15","Mixed held-out errors and warning failures"),("5:15-6:45","Diagonal site replay, wind shift and sensor loss"),("6:45-7:45","Water/exposure tradeoff and shared assumptions"),("7:45-9:00","Proposed architecture, costs and pilot validation"),("9:00-10:00","Completed software, team and request for pilot feedback")]
    s += [p("05 / TEN-MINUTE STORY", "DTKicker"), p("Lead with the demo.<br/>Keep the evidence honest.", "DTTitle"),table([["Time", "Show / say"]]+story,[105,WIDTH-105]),
          p("Questions the team should prepare for", "DTHeading"),
          p("<b>Why use the model if the mean wins?</b> The mean is a credible baseline. This model is a preliminary learned demonstration; lower RMSE does not establish universal superiority. New model research needs new untouched evaluation data."),
          p("<b>Does it predict a real boundary?</b> No. It forecasts the measured lab monitor; spatial mapping and misting response are separate, labelled assumptions."),
          p("<b>How much water will a site save?</b> Unknown. Compare actual flow and exposure under comparable independent activities before claiming field or daily savings."),
          p("<b>Where is the hardware?</b> Deferred. The team must explicitly authorize a calibrated Round 2 pilot. Qualification and feedback are not inferred."),
          p("<b>What if the service fails?</b> Use the labelled saved inference replay and PDF/screenshots. Do not describe saved output as fresh model execution."),
          p("The full speaking script is included as docs/judge-script.md and downloadable from Present. Practice spoken delivery with a real timer and check projector readability. The automated rehearsal verifies software only.", "DTNote"), PageBreak()]
    refs=[("1","World Bank / local construction and traffic context","https://blogs.worldbank.org/en/endpovertyinsouthasia/bangladesh-urgent-call-clean-air"),("2","Askarov and Choi 2024 / Mendeley V1 / CC BY 4.0","https://data.mendeley.com/datasets/7f22n9v7hp/1"),("3","DFRobot / SEN0177 PM monitor","https://www.dfrobot.com/product-1272.html"),("4","DFRobot / ESP32-E DFR0654","https://www.dfrobot.com/product-2195.html"),("5","DFRobot / SEN0483 wind speed","https://www.dfrobot.com/product-2339.html"),("6","DFRobot / SEN0482 wind direction","https://www.dfrobot.com/product-2340.html"),("7","TechShopBD / pump set","https://techshopbd.com/product/high-pressure-single-motor-water-pump-set-fl-4200"),("8","TechShopBD / 12 V valve","https://techshopbd.com/product/solenoid-valve-12v-34-inch/"),("9","TechShopBD / four-channel relay","https://techshopbd.com/product/relay-module-4-channel-12v"),("10","US EPA / sensor limitations and calibration","https://www.epa.gov/air-sensor-toolbox/frequent-questions-about-air-sensors")]
    s += [p("06 / SOURCE AND REPRODUCIBILITY", "DTKicker"),p("Sources you can inspect.","DTTitle")]
    for n,title,url in refs:
        s += [p(f'<b>[{n}] {title}</b><br/><link href="{url}" color="#2b7150">{url}</link>',"DTNote")]
    s += [p("Dataset reuse", "DTHeading"),p("Derived replay, causal preparation, forecasts and audit/evaluation plots credit Komiljon Askarov and Jae-ho Choi (2024), DOI 10.17632/7f22n9v7hp.1, CC BY 4.0. Originals are unchanged. Gridding/features/forecasts are project transformations. No contributor endorsement. The rejected 2020 data's separate attribution appears in README.md.","DTNote"),
          p("Local evidence", "DTHeading"),p("models/model-card.md; reports/evaluation/test-metrics.json; compressed full test traces; reports/training/validation-selection.json; reports/simulation/summary.json; configs/forecast-task.json; configs/feasibility.json; data/manifest.json; reports/readiness/.","DTNote"),
          p('<link href="https://github.com/arifshekhk8/DustTwin-AI" color="#2b7150">Public source: github.com/arifshekhk8/DustTwin-AI</link>',"DTNote"),
          p("The website was implemented originally; no code was imported from the reference frontend, whose reuse license was not recorded. All runtime evidence needed for the demonstration is included locally.","DTNote")]
    OUT.parent.mkdir(parents=True,exist_ok=True)
    doc=SimpleDocTemplate(str(OUT),pagesize=A4,leftMargin=44,rightMargin=44,topMargin=73,bottomMargin=60,title="DustTwin / CTRL_V / Round 1 Evidence",author="CTRL_V")
    doc.build(s,onFirstPage=header,onLaterPages=header)
    print(OUT)


if __name__ == "__main__":
    main()
