import json
import time
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path


class E2EReport:
    _steps = []

    @classmethod
    def start(cls):
        cls._steps = []

    @classmethod
    def record(cls, name, status, duration, details=None, error=""):
        cls._steps.append(
            {
                "name": name,
                "status": status,
                "duration": round(duration, 2),
                "details": details or [],
                "error": error,
            }
        )

    @classmethod
    def has_steps(cls):
        return bool(cls._steps)

    @classmethod
    def write_reports(cls, exitstatus=0):
        reports_dir = Path("reports")
        reports_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        html_path = reports_dir / f"e2e-report-{timestamp}.html"
        json_path = reports_dir / f"e2e-report-{timestamp}.json"

        passed_count = sum(1 for step in cls._steps if step["status"] == "PASSED")
        failed_count = len(cls._steps) - passed_count

        payload = {
            "generated_at": datetime.now().isoformat(),
            "overall_status": "PASSED" if exitstatus == 0 else "FAILED",
            "exit_code": exitstatus,
            "total_testcases": len(cls._steps),
            "passed_testcases": passed_count,
            "failed_testcases": failed_count,
            "total_duration_seconds": round(
                sum(step["duration"] for step in cls._steps), 2
            ),
            "testcases": cls._steps,
        }

        json_path.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        html_path.write_text(cls._build_html(payload), encoding="utf-8")

        return {"html": html_path, "json": json_path}

    @classmethod
    def _build_results_table_rows(cls, testcases):
        rows = []
        for step in testcases:
            status = step["status"]
            row_class = "passed" if status == "PASSED" else "failed"
            details = step.get("details") or []
            details_html = "<br>".join(details) if details else "-"
            if step.get("error"):
                details_html += f"<br><strong>Error:</strong> {step['error']}"

            rows.append(
                f"""
                <tr class="{row_class}">
                  <td class="col-result">{status}</td>
                  <td class="col-name">{step['name']}</td>
                  <td class="col-duration">{step['duration']}s</td>
                  <td class="col-details">{details_html}</td>
                </tr>
                """
            )
        return "".join(rows)

    @classmethod
    def _build_html(cls, payload):
        testcase_blocks = []
        for index, step in enumerate(payload["testcases"], start=1):
            status = step["status"]
            status_class = "passed" if status == "PASSED" else "failed"
            details = step.get("details") or []
            details_html = "".join(f"<li>{detail}</li>" for detail in details) or "<li>-</li>"
            error_html = (
                f"<p class='error'><strong>Error:</strong> {step['error']}</p>"
                if step.get("error")
                else ""
            )

            testcase_blocks.append(
                f"""
                <div class="testcase {status_class}">
                  <div class="testcase-header">
                    <h3>{index}. {step['name']}</h3>
                    <span class="badge {status.lower()}">{status}</span>
                    <span class="duration">{step['duration']}s</span>
                  </div>
                  <ul class="details">{details_html}</ul>
                  {error_html}
                </div>
                """
            )

        return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>E2E Test Report</title>
  <style>
    body {{
      font-family: Arial, sans-serif;
      margin: 24px;
      color: #1f2937;
      background: #f8fafc;
    }}
    .card {{
      background: #ffffff;
      border: 1px solid #e5e7eb;
      border-radius: 8px;
      padding: 20px;
      margin-bottom: 20px;
    }}
    .summary-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
      gap: 12px;
    }}
    .summary-item {{
      background: #f9fafb;
      border: 1px solid #e5e7eb;
      border-radius: 8px;
      padding: 12px;
    }}
    .summary-item strong {{
      display: block;
      margin-bottom: 6px;
      color: #6b7280;
      font-size: 12px;
      text-transform: uppercase;
    }}
    .testcase {{
      border: 1px solid #e5e7eb;
      border-radius: 8px;
      padding: 16px;
      margin-bottom: 12px;
      background: #ffffff;
    }}
    .testcase.passed {{
      border-left: 4px solid #22c55e;
    }}
    .testcase.failed {{
      border-left: 4px solid #ef4444;
      background: #fef2f2;
    }}
    .testcase-header {{
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 10px;
    }}
    .testcase-header h3 {{
      margin: 0;
      flex: 1;
    }}
    .badge {{
      display: inline-block;
      padding: 2px 8px;
      border-radius: 999px;
      font-size: 12px;
      font-weight: bold;
    }}
    .badge.passed {{
      background: #dcfce7;
      color: #166534;
    }}
    .badge.failed {{
      background: #fee2e2;
      color: #991b1b;
    }}
    .duration {{
      color: #6b7280;
      font-size: 14px;
    }}
    .details {{
      margin: 0;
      padding-left: 20px;
    }}
    .error {{
      color: #991b1b;
      margin: 10px 0 0;
    }}
    #results-table {{
      width: 100%;
      border-collapse: collapse;
      margin-top: 12px;
    }}
    #results-table th, #results-table td {{
      border: 1px solid #e5e7eb;
      padding: 10px 12px;
      text-align: left;
      vertical-align: top;
    }}
    #results-table th {{
      background: #f3f4f6;
    }}
    #results-table tr.passed {{
      background: #f0fdf4;
    }}
    #results-table tr.failed {{
      background: #fef2f2;
    }}
    .col-result {{
      width: 90px;
      font-weight: bold;
    }}
    .col-duration {{
      width: 90px;
      white-space: nowrap;
    }}
  </style>
</head>
<body>
  <div class="card">
    <h1>E2E Test Report</h1>
    <p>Generated at: {payload["generated_at"]}</p>
    <div class="summary-grid">
      <div class="summary-item"><strong>Overall Status</strong>{payload["overall_status"]}</div>
      <div class="summary-item"><strong>Total Testcases</strong>{payload["total_testcases"]}</div>
      <div class="summary-item"><strong>Passed</strong>{payload["passed_testcases"]}</div>
      <div class="summary-item"><strong>Failed</strong>{payload["failed_testcases"]}</div>
      <div class="summary-item"><strong>Total Duration</strong>{payload["total_duration_seconds"]}s</div>
    </div>
  </div>

  <div class="card">
    <h2>Results</h2>
    <table id="results-table">
      <thead>
        <tr>
          <th>Result</th>
          <th>Test</th>
          <th>Duration</th>
          <th>Details</th>
        </tr>
      </thead>
      <tbody>
        {cls._build_results_table_rows(payload["testcases"])}
      </tbody>
    </table>
  </div>

  <div class="card">
    <h2>Testcase Details</h2>
    {"".join(testcase_blocks)}
  </div>
</body>
</html>"""


class E2ESectionLog:
    def __init__(self):
        self._details = []

    def add(self, message):
        print(message)
        self._details.append(message)

    @property
    def details(self):
        return self._details


@contextmanager
def e2e_section(title):
    print(f"\n========== {title} ==========")
    log = E2ESectionLog()
    start = time.time()
    try:
        yield log
    except Exception as exc:
        E2EReport.record(
            title,
            "FAILED",
            time.time() - start,
            details=log.details,
            error=str(exc),
        )
        raise
    else:
        E2EReport.record(
            title,
            "PASSED",
            time.time() - start,
            details=log.details,
        )
