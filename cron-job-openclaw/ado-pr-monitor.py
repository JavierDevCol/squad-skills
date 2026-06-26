#!/usr/bin/env python3
"""
Azure DevOps PR Monitor + Auto-Pull
Cron job: runs every hour
- Detects newly merged PRs to develop/documentacion_fase2
- Detects open PRs pending merge
- Outputs messages for ONAD to send via Telegram
"""
import json
import os
import subprocess
import sys
import urllib.request
import urllib.error
from datetime import datetime, timezone

# === CONFIG ===
STATE_FILE = "/home/onad/openclaw-onad/workspace/memory/ado-pr-state.json"
ENV_FILE = "/home/onad/openclaw-onad/workspace/.env"
REPO_BASE = "/home/onad/openclaw-onad/workspace/REPO_BMM"

# Load PAT from .env
def load_pat():
    with open(ENV_FILE) as f:
        for line in f:
            if line.startswith("ADO_MCP_AUTH_TOKEN="):
                return line.strip().split("=", 1)[1]
    raise ValueError("PAT not found in .env")

PAT = load_pat()
ORG = "GestionRequerimientos"
API_VERSION = "7.1"

# Projects and their repos with target branches
PROJECTS = {
    "BancaPorWhatsappCICD": {
        "target_branch": "develop",
        "repos": {
            "Infra_BancaPorWhatsapp": "Infra_BancaPorWhatsapp",
            "comun-svc-lib": "comun-svc-lib",
            "ms-banca-auditoria": "ms-banca-auditoria",
            "ms-banca-autenticacion": "ms-banca-autenticacion",
            "ms-banca-conversacion": "ms-banca-conversacion",
            "ms-banca-notificaciones": "ms-banca-notificaciones",
            "ms-banca-productos": "ms-banca-productos",
            "ms-banca-referidos": "ms-banca-referidos",
            "ms-banca-reportes": "ms-banca-reportes",
            "ms-banca-retiros": "ms-banca-retiros",
            "ms-banca-terminos-condiciones": "ms-banca-terminos-condiciones",
            "Doc_BancaPorWhatsapp": "Doc_BancaPorWhatsapp",
        },
        # Doc repo has different branch
        "branch_overrides": {
            "Doc_BancaPorWhatsapp": "documentacion_fase2"
        }
    },
    "Middleware-CICD": {
        "target_branch": "develop",
        "repos": {
            "bmm-middleware-iac-infra": "bmm-middleware-iac-infra",
            "bmm-middleware-ms-datos-maestros": "bmm-middleware-ms-datos-maestros",
            "bmm-middleware-ms-rabbitmq": "bmm-middleware-ms-rabbitmq",
            "bmm-middleware-ms-vault": "bmm-middleware-ms-vault",
        }
    },
    "OnbordingCICD": {
        "target_branch": "develop",
        "repos": {
            "bmm-onboarding-iac": "bmm-onboarding-iac",
            "bmm-onboarding-ms-auditoria-trazabilidad": "bmm-onboarding-ms-auditoria-trazabilidad",
            "bmm-onboarding-ms-checkpoints-retoma": "bmm-onboarding-ms-checkpoints-retoma",
            "bmm-onboarding-ms-orquestador-bus": "bmm-onboarding-ms-orquestador-bus",
            "bmm-onboarding-ms-registro-usuario": "bmm-onboarding-ms-registro-usuario",
        }
    }
}

def api_get(url):
    """Make authenticated GET to Azure DevOps API."""
    import base64
    auth = base64.b64encode(f":{PAT}".encode()).decode()
    req = urllib.request.Request(url, headers={
        "Authorization": f"Basic {auth}",
        "Content-Type": "application/json"
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        print(f"API Error {e.code}: {url}", file=sys.stderr)
        return {"value": [], "count": 0}
    except Exception as e:
        print(f"Request Error: {e}", file=sys.stderr)
        return {"value": [], "count": 0}

def load_state():
    """Load previous state."""
    try:
        with open(STATE_FILE) as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"last_check_utc": "2000-01-01T00:00:00Z", "known_completed_prs": [], "known_active_prs": []}

def save_state(state):
    """Save current state."""
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def git_pull(repo_name, branch):
    """Pull latest changes for a repo."""
    repo_path = os.path.join(REPO_BASE, repo_name)
    if not os.path.isdir(repo_path):
        return False, f"Repo dir not found: {repo_path}"
    try:
        result = subprocess.run(
            ["git", "pull", "origin", branch],
            cwd=repo_path, capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0:
            # Get current commit
            commit = subprocess.run(
                ["git", "rev-parse", "--short", "HEAD"],
                cwd=repo_path, capture_output=True, text=True
            )
            return True, commit.stdout.strip()
        else:
            return False, result.stderr.strip()[:200]
    except Exception as e:
        return False, str(e)[:200]

def time_ago(dt_str):
    """Human readable time ago."""
    try:
        dt = datetime.fromisoformat(dt_str.replace("Z", "+00:00"))
        diff = datetime.now(timezone.utc) - dt
        minutes = int(diff.total_seconds() / 60)
        if minutes < 60:
            return f"{minutes} min"
        hours = minutes // 60
        if hours < 24:
            return f"{hours}h"
        days = hours // 24
        return f"{days}d"
    except:
        return "?"

def main():
    state = load_state()
    known_completed = set(state.get("known_completed_prs", []))
    known_active = set(state.get("known_active_prs", []))
    
    messages = []
    new_completed = set()
    current_active = set()
    
    for project, config in PROJECTS.items():
        default_branch = config["target_branch"]
        branch_overrides = config.get("branch_overrides", {})
        
        # --- Check COMPLETED PRs ---
        url = (f"https://dev.azure.com/{ORG}/{project}/_apis/git/pullrequests"
               f"?searchCriteria.status=completed&$top=20&api-version={API_VERSION}")
        data = api_get(url)
        
        for pr in data.get("value", []):
            pr_id = str(pr["pullRequestId"])
            repo_name = pr.get("repository", {}).get("name", "unknown")
            target_branch = pr.get("targetRefName", "").split("/")[-1]
            expected_branch = branch_overrides.get(repo_name, default_branch)
            
            # Only care about PRs to our tracked branches
            if target_branch != expected_branch:
                continue
            
            # Only care about repos we track
            if repo_name not in config["repos"]:
                continue
            
            pr_key = f"{project}:{pr_id}"
            new_completed.add(pr_key)
            
            if pr_key not in known_completed:
                # NEW merged PR!
                title = pr["title"][:80]
                author = pr.get("createdBy", {}).get("displayName", "Unknown")
                closed = pr.get("closedDate", "")
                ago = time_ago(closed) if closed else "?"
                
                messages.append({
                    "type": "merged",
                    "repo": repo_name,
                    "branch": target_branch,
                    "pr_id": pr["pullRequestId"],
                    "title": title,
                    "author": author,
                    "ago": ago,
                    "project": project,
                    "local_repo": config["repos"][repo_name]
                })
        
        # --- Check ACTIVE PRs ---
        url = (f"https://dev.azure.com/{ORG}/{project}/_apis/git/pullrequests"
               f"?searchCriteria.status=active&api-version={API_VERSION}")
        data = api_get(url)
        
        for pr in data.get("value", []):
            pr_id = str(pr["pullRequestId"])
            repo_name = pr.get("repository", {}).get("name", "unknown")
            target_branch = pr.get("targetRefName", "").split("/")[-1]
            expected_branch = branch_overrides.get(repo_name, default_branch)
            
            if target_branch != expected_branch:
                continue
            if repo_name not in config["repos"]:
                continue
            
            pr_key = f"{project}:{pr_id}"
            current_active.add(pr_key)
            
            if pr_key not in known_active:
                # NEW active PR detected
                title = pr["title"][:80]
                author = pr.get("createdBy", {}).get("displayName", "Unknown")
                created = pr.get("creationDate", "")
                ago = time_ago(created) if created else "?"
                reviewers = [r.get("displayName", "?") for r in pr.get("reviewers", [])]
                reviewer_str = ", ".join(reviewers) if reviewers else "sin asignar"
                
                messages.append({
                    "type": "active",
                    "repo": repo_name,
                    "branch": target_branch,
                    "pr_id": pr["pullRequestId"],
                    "title": title,
                    "author": author,
                    "ago": ago,
                    "reviewers": reviewer_str,
                    "project": project
                })
    
    # --- Process messages ---
    output_lines = []
    
    for msg in messages:
        if msg["type"] == "merged":
            # Notify about merge
            output_lines.append(
                f"🔀 Nuevo merge a {msg['branch']} en **{msg['repo']}**\n"
                f"PR #{msg['pr_id']}: \"{msg['title']}\"\n"
                f"Autor: {msg['author']} | Hace: {msg['ago']}"
            )
            
            # Auto-pull
            success, result = git_pull(msg["local_repo"], msg["branch"])
            if success:
                output_lines.append(
                    f"✅ Pull completado en REPO_BMM/{msg['local_repo']}\n"
                    f"{msg['branch']} actualizado a commit {result}"
                )
            else:
                output_lines.append(
                    f"❌ Error en pull de REPO_BMM/{msg['local_repo']}: {result}"
                )
        
        elif msg["type"] == "active":
            output_lines.append(
                f"📋 PR abierto pendiente en **{msg['repo']}**\n"
                f"PR #{msg['pr_id']}: \"{msg['title']}\" → {msg['branch']}\n"
                f"Autor: {msg['author']} | Creado hace: {msg['ago']}\n"
                f"Reviewers: {msg['reviewers']}"
            )
    
    # Save state
    state["last_check_utc"] = datetime.now(timezone.utc).isoformat()
    state["known_completed_prs"] = list(new_completed)
    state["known_active_prs"] = list(current_active)
    save_state(state)
    
    # Output
    if output_lines:
        print("\n---\n".join(output_lines))
    else:
        print("NO_CHANGES")

if __name__ == "__main__":
    main()
