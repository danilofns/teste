#!/usr/bin/env python3
"""Coleta métricas públicas do GitHub e gera docs/productivity/metrics.json.

Requisitos (idempotência): sempre reescreve o arquivo completo.

Env:
- GITHUB_TOKEN: token do GitHub (necessário)
- GITHUB_REPOSITORY: no formato owner/repo (opcional; se ausente, tenta detectar)

Também aceita:
- GITHUB_API_URL (opcional; padrão https://api.github.com)

Execução local:
  python docs/productivity/collect_metrics.py

"""

from __future__ import annotations

import json
import os
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from typing import Any, Dict, Iterable, List, Optional, Tuple

from github import Github
from github.AuthenticatedUser import AuthenticatedUser
from github.Issue import Issue
from github.PullRequest import PullRequest
from github.Repository import Repository


UNICODE_DAY_TO_INDEX = {
    "Mon": 0,
    "Tue": 1,
    "Wed": 2,
    "Thu": 3,
    "Fri": 4,
    "Sat": 5,
    "Sun": 6,
}


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def parse_week_key(dt: datetime) -> str:
    # dt em UTC
    iso_year, iso_week, _ = dt.isocalendar()
    return f"{iso_year}-W{iso_week:02d}"


def safe_int(x: Any, default: int = 0) -> int:
    try:
        return int(x)
    except Exception:
        return default


def chunked(iterable: Iterable[Any], n: int) -> Iterable[List[Any]]:
    buf: List[Any] = []
    for item in iterable:
        buf.append(item)
        if len(buf) >= n:
            yield buf
            buf = []
    if buf:
        yield buf


def normalize_username(user: Any) -> str:
    # PyGithub user.login
    return getattr(user, "login", None) or str(user)


@dataclass
class PersonAgg:
    username: str
    name: str
    avatar_url: str
    commits: int = 0
    prs_opened: int = 0
    issues_opened: int = 0
    issues_closed: int = 0

    def to_top_committers(self) -> Dict[str, Any]:
        return {"username": self.username, "name": self.name, "commits": self.commits, "avatar_url": self.avatar_url}

    def to_top_pr_authors(self) -> Dict[str, Any]:
        return {"username": self.username, "name": self.name, "prs_opened": self.prs_opened, "avatar_url": self.avatar_url}

    def to_top_issue_contributors(self) -> Dict[str, Any]:
        total = self.issues_opened + self.issues_closed
        return {
            "username": self.username,
            "name": self.name,
            "opened": self.issues_opened,
            "closed": self.issues_closed,
            "total": total,
            "avatar_url": self.avatar_url,
        }


COAUTHORED_BY_RE = re.compile(r"^Co-authored-by:\s*(.+?)\s*<([^>]+)>\s*$", re.IGNORECASE | re.MULTILINE)


def parse_coauthors(commit_message: str) -> List[Tuple[str, str]]:
    """Retorna lista de (name, email). Ignora formatos inválidos."""
    if not commit_message:
        return []
    out: List[Tuple[str, str]] = []
    for m in COAUTHORED_BY_RE.finditer(commit_message):
        name = (m.group(1) or "").strip()
        email = (m.group(2) or "").strip().lower()
        if not name or not email or "@" not in email:
            continue
        out.append((name, email))
    return out


def classify_commit_message_histogram(message: str) -> str:
    # Conte caracteres na mensagem
    n = len(message or "")
    if n <= 20:
        return "0-20"
    if n <= 50:
        return "21-50"
    if n <= 100:
        return "51-100"
    if n <= 200:
        return "101-200"
    return "200+"


def ensure_days_hours_heatmap(dataset: Dict[Tuple[int, int], int]) -> List[Dict[str, int]]:
    # Mantemos apenas bins com dados; a UI pode inferir ausência como zero.
    res = []
    for (day_idx, hour), count in sorted(dataset.items(), key=lambda x: (x[0][0], x[0][1])):
        if count:
            res.append({"day": day_idx, "hour": hour, "count": count})
    return res


def build_issue_week_aggregates(repo: Repository) -> Tuple[Dict[str, int], Dict[str, int]]:
    opened_by_week: Dict[str, int] = defaultdict(int)
    closed_by_week: Dict[str, int] = defaultdict(int)

    # Considera issues e PRs? A spec pede issues abertas vs fechadas.
    # Implementação conservadora: apenas Issues (sem PR).
    # PyGithub permite repo.issues(state=..., since=...): inclui PRs também, então filtramos.
    # Vamos buscar tudo paginado, mas com paginação: repos pequenos.

    # Janela: pega desde 52 semanas atrás (ou menos, se não houver dados).
    since = datetime.now(timezone.utc) - timedelta(weeks=104)

    for state, target in [("open", opened_by_week), ("closed", closed_by_week)]:
        # 'since' pode reduzir custo. Para casos com <1 semana, ainda funciona.
        for issue in repo.get_issues(state=state, since=since, direction="desc"):
            if issue.pull_request is not None:
                continue
            created_at = issue.created_at
            closed_at = getattr(issue, "closed_at", None)
            if state == "open":
                week = parse_week_key(created_at)
                target[week] += 1
            else:
                if closed_at is None:
                    continue
                week = parse_week_key(closed_at)
                target[week] += 1

    return opened_by_week, closed_by_week


def build_commit_aggregates(repo: Repository) -> Tuple[
    Dict[str, int],
    Dict[str, int],
    Dict[Tuple[int, int], int],
    Dict[str, PersonAgg],
]:
    commit_message_histogram: Dict[str, int] = defaultdict(int)
    coauthors_per_week: Dict[str, int] = defaultdict(int)
    heatmap_bins: Dict[Tuple[int, int], int] = defaultdict(int)
    persons: Dict[str, PersonAgg] = {}

    since = datetime.now(timezone.utc) - timedelta(weeks=104)

    # get_commits returns iterable with pagination.
    # Use per_page to manage.
    for commit in repo.get_commits(since=since):
        # Author may be None
        author = getattr(commit, "author", None)
        committer = getattr(commit, "commit", None)
        author_name = None
        author_login = None
        avatar_url = ""

        if author is not None:
            author_login = getattr(author, "login", None)
            author_name = getattr(author, "name", None) or author_login
            avatar_url = getattr(author, "avatar_url", "") or ""
        else:
            # fallback: use commit.committer name/email as username placeholder
            comm = getattr(commit, "commit", None)
            author_name = getattr(getattr(comm, "author", None), "name", None)
            author_login = author_name or "unknown"

        if not author_login:
            author_login = "unknown"

        if author_login not in persons:
            persons[author_login] = PersonAgg(
                username=author_login,
                name=author_name or author_login,
                avatar_url=avatar_url,
            )

        persons[author_login].commits += 1

        # Histogram by message
        message = getattr(commit.commit, "message", "") if getattr(commit, "commit", None) else ""
        bucket = classify_commit_message_histogram(message)
        commit_message_histogram[bucket] += 1

        # Heatmap by committer/author time (use commit.author date if possible)
        timestamp = None
        commit_obj = getattr(commit, "commit", None)
        if commit_obj is not None:
            dt = getattr(getattr(commit_obj, "author", None), "date", None)
            if dt is None:
                dt = getattr(getattr(commit_obj, "committer", None), "date", None)
            timestamp = dt
        if timestamp is None:
            continue

        dt_utc = timestamp.astimezone(timezone.utc) if isinstance(timestamp, datetime) else timestamp
        week = parse_week_key(dt_utc)
        hour = dt_utc.hour
        day_idx = dt_utc.weekday()  # Mon=0
        heatmap_bins[(day_idx, hour)] += 1

        # Co-authors per week: count Co-authored-by lines in message
        coauthors = parse_coauthors(message)
        if coauthors:
            coauthors_per_week[week] += len(coauthors)

    return commit_message_histogram, coauthors_per_week, heatmap_bins, persons


def build_pr_opened_aggregates(repo: Repository) -> Dict[str, PersonAgg]:
    persons: Dict[str, PersonAgg] = {}
    since = datetime.now(timezone.utc) - timedelta(weeks=104)

    for pr in repo.get_pulls(state="open", sort="created", direction="desc"):

        # PR pode ser antigo; filtrar por created_at
        if pr.created_at < since:
            # como desc, pode quebrar; porém nem sempre garante.
            continue

        user = pr.user
        username = normalize_username(user)
        name = getattr(user, "name", None) or username
        avatar_url = getattr(user, "avatar_url", "") or ""

        if username not in persons:
            persons[username] = PersonAgg(username=username, name=name, avatar_url=avatar_url)
        persons[username].prs_opened += 1

    return persons


def build_issue_contributors(repo: Repository, persons: Dict[str, PersonAgg]) -> Dict[str, PersonAgg]:
    since = datetime.now(timezone.utc) - timedelta(weeks=104)

    # Busca issues abertas e fechadas para somar por autor (creator).
    for state in ["open", "closed"]:
        for issue in repo.get_issues(state=state, since=since, direction="desc"):
            if issue.pull_request is not None:
                continue

            user = issue.user
            username = normalize_username(user)
            name = getattr(user, "name", None) or username
            avatar_url = getattr(user, "avatar_url", "") or ""

            if username not in persons:
                persons[username] = PersonAgg(username=username, name=name, avatar_url=avatar_url)

            if state == "open":
                persons[username].issues_opened += 1
            else:
                persons[username].issues_closed += 1

    return persons


def sort_top_10(items: List[Dict[str, Any]], key: str, top_n: int = 10) -> List[Dict[str, Any]]:
    return sorted(items, key=lambda x: x.get(key, 0), reverse=True)[:top_n]



def main() -> int:
    token = os.environ.get("GITHUB_TOKEN")
    repo_full = os.environ.get("GITHUB_REPOSITORY")

    if not token:
        print("Erro: variável de ambiente GITHUB_TOKEN não definida.", file=sys.stderr)
        return 2
    if not repo_full:
        print("Erro: variável de ambiente GITHUB_REPOSITORY não definida.", file=sys.stderr)
        return 2

    api_url = os.environ.get("GITHUB_API_URL")

    from github import Auth

    auth = Auth.Token(token)
    github = Github(auth=auth, base_url=api_url) if api_url else Github(auth=auth)

    repo = github.get_repo(repo_full)

    opened_by_week, closed_by_week = build_issue_week_aggregates(repo)
    commit_hist, coauthors_by_week, heatmap_bins, committers = build_commit_aggregates(repo)
    pr_openers = build_pr_opened_aggregates(repo)

    # Merge PR authors into committers dict
    for username, pdata in pr_openers.items():
        if username not in committers:
            committers[username] = pdata
        else:
            # keep name/avatar from committers; add prs_opened
            committers[username].prs_opened = pdata.prs_opened

    committers = build_issue_contributors(repo, committers)

    # Build sorted weeks union
    weeks = sorted(set(list(opened_by_week.keys()) + list(closed_by_week.keys())))

    issues_per_week = []
    for w in weeks:
        issues_per_week.append({"week": w, "opened": opened_by_week.get(w, 0), "closed": closed_by_week.get(w, 0)})

    # Ensure histogram buckets order
    histogram_order = ["0-20", "21-50", "51-100", "101-200", "200+"]
    commit_message_histogram = [{"range": r, "count": int(commit_hist.get(r, 0))} for r in histogram_order]

    coauthors_per_week = [{"week": w, "count": int(coauthors_by_week.get(w, 0))} for w in weeks if w in coauthors_by_week]


    # Remove trailing zeros if no commits at all: keep still weeks present? Spec allows available data.
    if not coauthors_by_week:
        coauthors_per_week = []
    else:
        coauthors_per_week = [{"week": w, "count": int(coauthors_by_week[w])} for w in sorted(coauthors_by_week.keys())]

    commit_heatmap = ensure_days_hours_heatmap(heatmap_bins)

    # rankings
    top_committers = sorted(committers.values(), key=lambda p: p.commits, reverse=True)
    top_pr_authors = sorted(committers.values(), key=lambda p: p.prs_opened, reverse=True)
    top_issue_contribs = sorted(committers.values(), key=lambda p: (p.issues_opened + p.issues_closed), reverse=True)

    top_committers_list = [p.to_top_committers() for p in top_committers]
    top_pr_authors_list = [p.to_top_pr_authors() for p in top_pr_authors]
    top_issue_contrib_list = [p.to_top_issue_contributors() for p in top_issue_contribs]

    out: Dict[str, Any] = {
        "generated_at": utc_now_iso(),
        "repository": repo_full,
        "issues_per_week": issues_per_week,
        "commit_message_histogram": commit_message_histogram,
        "coauthors_per_week": coauthors_per_week,
        "commit_heatmap": commit_heatmap,
        "top_committers": top_committers_list,
        "top_pr_authors": top_pr_authors_list,
        "top_issue_contributors": top_issue_contrib_list,
    }

    os.makedirs(os.path.dirname(os.path.abspath(os.path.join(__file__, "metrics.json"))), exist_ok=True)
    out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "metrics.json"))
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

    print(f"Gerado: {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

