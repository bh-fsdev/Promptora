#!/usr/bin/env python3
"""Create GitHub Issues from the Task Register in docs/ai/TASKS.md.

Idempotent: a task that already has an Issue titled "[TASK-ID] ..." is never duplicated.
Labels: status:ready or status:backlog, worker:1 or worker:2.
Only tasks assigned to "Worker 1" or "Worker 2" are synced (owner tasks are skipped).
A task is labeled status:ready only if the register says READY and every TASK-nnn it depends on
is DONE. TASK-000 (owner bootstrap) counts as done because this script only runs from main.

Usage: python3 scripts/sync_tasks.py [--dry-run]
Requires the GitHub CLI (`gh`) authenticated through GH_TOKEN, except with --dry-run.
"""
import json, os, re, subprocess, sys

DRY = "--dry-run" in sys.argv
PATH = "docs/ai/TASKS.md"
LABELS = {
    "status:backlog": ("c5def5", "Task defined but not startable yet"),
    "status:ready": ("0e8a16", "Ready for a worker to pick up"),
    "status:in-progress": ("fbca04", "A worker is working on it"),
    "status:review": ("1d76db", "Branch pushed, waiting for PR, CI, and review"),
    "status:needs-changes": ("d93f0b", "Review found problems; worker should fix on the same branch"),
    "status:blocked": ("b60205", "Blocked; see comments"),
    "worker:1": ("5319e7", "Worker 1 (backend)"),
    "worker:2": ("0052cc", "Worker 2 (frontend)"),
}

def sh(args, check=True):
    r = subprocess.run(args, capture_output=True, text=True)
    if check and r.returncode != 0:
        sys.exit(f"command failed: {' '.join(args)}\n{r.stderr}")
    return r.stdout

def parse(text):
    tasks = {}
    for m in re.finditer(r"^\|\s*(TASK-\d{3})\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*([A-Z_]+)\s*\|\s*(.*?)\s*\|\s*$", text, re.M):
        tid, title, worker, status, deps = m.groups()
        tasks[tid] = dict(id=tid, title=title, worker=worker, status=status,
                          deps=re.findall(r"TASK-\d{3}", deps), deps_text=deps)
    # detailed sections: "## TASK-001: ..." up to the next "---" line or next "## "
    for m in re.finditer(r"^## (TASK-\d{3}):.*?\n(.*?)(?=^---\s*$|^## )", text, re.M | re.S):
        if m.group(1) in tasks:
            tasks[m.group(1)]["spec"] = m.group(0).strip()
    return tasks

def main():
    tasks = parse(open(PATH, encoding="utf-8").read())
    if not tasks:
        sys.exit("no tasks parsed from register")
    if not DRY:
        for name, (color, desc) in LABELS.items():
            sh(["gh", "label", "create", name, "--color", color, "--description", desc, "--force"])
        existing = json.loads(sh(["gh", "issue", "list", "--state", "all", "--limit", "500",
                                  "--json", "number,title,labels,state"]))
    else:
        existing = []
    by_id = {}
    for i in existing:
        m = re.match(r"\[(TASK-\d{3})\]", i["title"])
        if m:
            by_id[m.group(1)] = i
    lines = []
    for t in tasks.values():
        wm = re.match(r"Worker ([12])", t["worker"])
        if not wm:
            continue
        done = lambda d: d == "TASK-000" or tasks.get(d, {}).get("status") == "DONE"
        deps_ok = all(done(d) for d in t["deps"])
        ready = t["status"] == "READY" and deps_ok
        status_label = "status:ready" if ready else "status:backlog"
        if t["status"] not in ("READY", "BACKLOG"):
            continue
        worker_label = f"worker:{wm.group(1)}"
        title = f"[{t['id']}] {t['title']}"
        body = (t.get("spec") or f"{t['title']}\n\n(See the backlog outline in docs/ai/TASKS.md.)")
        body += (f"\n\n---\n**Worker:** {t['worker']}  \n**Dependencies:** {t['deps_text'] or 'none'}  \n"
                 "Source of truth: the Task Register in `docs/ai/TASKS.md`. "
                 "Do not edit scope here; change the register through a PR.")
        if t["id"] in by_id:
            issue = by_id[t["id"]]
            names = {l["name"] for l in issue["labels"]}
            if issue["state"] == "OPEN" and "status:backlog" in names and ready:
                lines.append(f"{t['id']}: promote backlog -> ready (#{issue['number']})")
                if not DRY:
                    sh(["gh", "issue", "edit", str(issue["number"]), "--remove-label", "status:backlog",
                        "--add-label", "status:ready"])
            else:
                lines.append(f"{t['id']}: exists (#{issue['number']}), unchanged")
            continue
        lines.append(f"{t['id']}: create issue, labels {status_label}, {worker_label}")
        if not DRY:
            sh(["gh", "issue", "create", "--title", title, "--body", body,
                "--label", status_label, "--label", worker_label])
    print("\n".join(lines))
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a") as f:
            f.write("### Task sync\n\n" + "\n".join(f"- {l}" for l in lines) + "\n")

if __name__ == "__main__":
    main()
