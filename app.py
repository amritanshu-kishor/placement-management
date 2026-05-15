"""
Flask backend — REST API for Placement Management System.
"""

from flask import Flask, jsonify, request, send_from_directory

from dbconnection import ROOT, init_db, get_db

app = Flask(__name__, static_folder="static", static_url_path="")


@app.route("/")
def index():
    return send_from_directory(ROOT / "static", "index.html")


# ---------- Students ----------
@app.route("/api/students", methods=["GET", "POST"])
def students():
    if request.method == "GET":
        with get_db() as conn:
            cur = conn.execute("SELECT * FROM students ORDER BY student_id DESC")
            rows = cur.fetchall()
            return jsonify(rows)
    data = request.get_json(force=True, silent=True) or {}
    required = ["roll_no", "full_name", "email", "department", "cgpa"]
    for key in required:
        if key not in data:
            return jsonify({"error": f"Missing field: {key}"}), 400
    try:
        with get_db() as conn:
            ex = conn.execute(
                """INSERT INTO students (roll_no, full_name, email, department, cgpa, phone)
                   VALUES (%s, %s, %s, %s, %s, %s)""",
                (
                    data["roll_no"],
                    data["full_name"],
                    data["email"],
                    data["department"],
                    float(data["cgpa"]),
                    data.get("phone"),
                ),
            )
            sid = ex.lastrowid
            cur = conn.execute(
                "SELECT * FROM students WHERE student_id = %s", (sid,)
            )
            return jsonify(dict(cur.fetchone())), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    with get_db() as conn:
        conn.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
    return "", 204


# ---------- Companies ----------
@app.route("/api/companies", methods=["GET", "POST"])
def companies():
    if request.method == "GET":
        with get_db() as conn:
            cur = conn.execute("SELECT * FROM companies ORDER BY company_id DESC")
            return jsonify(cur.fetchall())
    data = request.get_json(force=True, silent=True) or {}
    if "name" not in data:
        return jsonify({"error": "Missing field: name"}), 400
    try:
        with get_db() as conn:
            ex = conn.execute(
                """INSERT INTO companies (name, sector, headquarters, website)
                   VALUES (%s, %s, %s, %s)""",
                (
                    data["name"],
                    data.get("sector"),
                    data.get("headquarters"),
                    data.get("website"),
                ),
            )
            cid = ex.lastrowid
            cur = conn.execute(
                "SELECT * FROM companies WHERE company_id = %s", (cid,)
            )
            return jsonify(dict(cur.fetchone())), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/companies/<int:company_id>", methods=["DELETE"])
def delete_company(company_id):
    with get_db() as conn:
        conn.execute("DELETE FROM companies WHERE company_id = %s", (company_id,))
    return "", 204


# ---------- Jobs ----------
@app.route("/api/jobs", methods=["GET", "POST"])
def jobs():
    if request.method == "GET":
        with get_db() as conn:
            cur = conn.execute(
                """SELECT j.*, c.name AS company_name
                   FROM jobs j
                   JOIN companies c ON c.company_id = j.company_id
                   ORDER BY j.job_id DESC"""
            )
            return jsonify(cur.fetchall())
    data = request.get_json(force=True, silent=True) or {}
    for key in ["company_id", "role_title", "package_lpa"]:
        if key not in data:
            return jsonify({"error": f"Missing field: {key}"}), 400
    try:
        with get_db() as conn:
            ex = conn.execute(
                """INSERT INTO jobs (company_id, role_title, job_type, package_lpa,
                                    min_cgpa, openings, deadline)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (
                    int(data["company_id"]),
                    data["role_title"],
                    data.get("job_type") or "Full-time",
                    float(data["package_lpa"]),
                    float(data.get("min_cgpa") or 0),
                    int(data.get("openings") or 1),
                    data.get("deadline") or None,
                ),
            )
            jid = ex.lastrowid
            cur = conn.execute(
                """SELECT j.*, c.name AS company_name FROM jobs j
                   JOIN companies c ON c.company_id = j.company_id
                   WHERE j.job_id = %s""",
                (jid,),
            )
            return jsonify(dict(cur.fetchone())), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/jobs/<int:job_id>", methods=["DELETE"])
def delete_job(job_id):
    with get_db() as conn:
        conn.execute("DELETE FROM jobs WHERE job_id = %s", (job_id,))
    return "", 204


# ---------- Applications ----------
@app.route("/api/applications", methods=["GET", "POST"])
def applications():
    if request.method == "GET":
        with get_db() as conn:
            cur = conn.execute(
                """SELECT a.*,
                          s.full_name AS student_name, s.roll_no,
                          j.role_title, j.package_lpa,
                          c.name AS company_name
                   FROM applications a
                   JOIN students s ON s.student_id = a.student_id
                   JOIN jobs j ON j.job_id = a.job_id
                   JOIN companies c ON c.company_id = j.company_id
                   ORDER BY a.application_id DESC"""
            )
            return jsonify(cur.fetchall())
    data = request.get_json(force=True, silent=True) or {}
    if "student_id" not in data or "job_id" not in data:
        return jsonify({"error": "student_id and job_id required"}), 400
    try:
        with get_db() as conn:
            ex = conn.execute(
                """INSERT INTO applications (student_id, job_id, status)
                   VALUES (%s, %s, %s)""",
                (
                    int(data["student_id"]),
                    int(data["job_id"]),
                    data.get("status") or "Applied",
                ),
            )
            aid = ex.lastrowid
            cur = conn.execute(
                """SELECT a.*,
                          s.full_name AS student_name, s.roll_no,
                          j.role_title, j.package_lpa,
                          c.name AS company_name
                   FROM applications a
                   JOIN students s ON s.student_id = a.student_id
                   JOIN jobs j ON j.job_id = a.job_id
                   JOIN companies c ON c.company_id = j.company_id
                   WHERE a.application_id = %s""",
                (aid,),
            )
            return jsonify(dict(cur.fetchone())), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/applications/<int:application_id>", methods=["PATCH"])
def patch_application(application_id):
    data = request.get_json(force=True, silent=True) or {}
    if "status" not in data:
        return jsonify({"error": "Missing status"}), 400
    allowed = {"Applied", "Shortlisted", "Interview", "Offer", "Rejected"}
    if data["status"] not in allowed:
        return jsonify({"error": "Invalid status"}), 400
    with get_db() as conn:
        conn.execute(
            "UPDATE applications SET status = %s WHERE application_id = %s",
            (data["status"], application_id),
        )
        cur = conn.execute(
            """SELECT a.*,
                      s.full_name AS student_name, s.roll_no,
                      j.role_title, j.package_lpa,
                      c.name AS company_name
               FROM applications a
               JOIN students s ON s.student_id = a.student_id
               JOIN jobs j ON j.job_id = a.job_id
               JOIN companies c ON c.company_id = j.company_id
               WHERE a.application_id = %s""",
            (application_id,),
        )
        row = cur.fetchone()
        if not row:
            return jsonify({"error": "Not found"}), 404
        return jsonify(dict(row))


@app.route("/api/stats", methods=["GET"])
def stats():
    with get_db() as conn:
        students = conn.execute(
            "SELECT COUNT(*) AS c FROM students"
        ).fetchone()["c"]
        companies = conn.execute(
            "SELECT COUNT(*) AS c FROM companies"
        ).fetchone()["c"]
        jobs_n = conn.execute("SELECT COUNT(*) AS c FROM jobs").fetchone()["c"]
        apps = conn.execute(
            "SELECT COUNT(*) AS c FROM applications"
        ).fetchone()["c"]
    return jsonify(
        {
            "students": students,
            "companies": companies,
            "jobs": jobs_n,
            "applications": apps,
        }
    )


@app.route("/api/reports", methods=["GET"])
def reports():
    with get_db() as conn:
        by_status = conn.execute(
            """SELECT status, COUNT(*) AS count
               FROM applications GROUP BY status ORDER BY count DESC"""
        ).fetchall()
        by_company = conn.execute(
            """SELECT c.name AS company_name,
                      COUNT(a.application_id) AS application_count
               FROM companies c
               LEFT JOIN jobs j ON j.company_id = c.company_id
               LEFT JOIN applications a ON a.job_id = j.job_id
               GROUP BY c.company_id, c.name
               ORDER BY application_count DESC, c.name"""
        ).fetchall()
        offers = conn.execute(
            """SELECT DISTINCT s.student_id, s.full_name, s.roll_no
               FROM students s
               JOIN applications a ON a.student_id = s.student_id
               WHERE a.status = 'Offer'"""
        ).fetchall()
        row = conn.execute(
            "SELECT AVG(package_lpa) AS a FROM jobs"
        ).fetchone()
        avg_package = row["a"] if row else None
    return jsonify(
        {
            "applications_by_status": by_status,
            "applications_by_company": by_company,
            "students_with_offer": offers,
            "avg_package_lpa": round(float(avg_package), 2)
            if avg_package is not None
            else None,
        }
    )


if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="127.0.0.1", port=5000)
