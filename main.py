#!/usr/bin/env python3
"""Project AI Manager."""

import json, sys
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Task:
    id: int
    title: str
    description: str
    estimate_hours: float
    priority: str = "medium"
    dependencies: list = field(default_factory=list)
    risks: list = field(default_factory=list)

@dataclass
class ProjectPlan:
    name: str
    tasks: list = field(default_factory=list)
    total_hours: float = 0.0
    estimated_weeks: float = 0.0
    risks: list = field(default_factory=list)

class ProjectManager:
    def plan(self, description: str) -> ProjectPlan:
        plan = ProjectPlan(name=description[:50])
        tasks = self._break_down(description)
        plan.tasks = tasks
        plan.total_hours = sum(t.estimate_hours for t in tasks)
        plan.estimated_weeks = round(plan.total_hours / 40, 1)
        plan.risks = self._identify_risks(tasks)
        return plan

    def _break_down(self, desc: str) -> list:
        lower = desc.lower()
        tasks = []
        tid = 1

        base_tasks = [
            Task(tid, "Project Setup", "Initialize repo, CI/CD, dev environment", 4, "high"),
            Task(tid + 1, "Database Design", "Schema design and migrations", 8, "high"),
        ]
        tid += 2

        if "auth" in lower or "login" in lower:
            base_tasks.append(Task(tid, "Authentication System", "User registration, login, JWT tokens", 16, "high"))
            tid += 1

        if "api" in lower or "backend" in lower:
            base_tasks.append(Task(tid, "API Development", "REST endpoints, validation, error handling", 24, "high"))
            tid += 1

        if "ui" in lower or "frontend" in lower or "app" in lower:
            base_tasks.append(Task(tid, "Frontend Development", "React components, routing, state management", 32, "medium"))
            tid += 1

        if "payment" in lower or "billing" in lower:
            base_tasks.append(Task(tid, "Payment Integration", "Stripe/payment gateway integration", 16, "high",
                                   risks=["Payment provider downtime"]))
            tid += 1

        base_tasks.extend([
            Task(tid, "Testing", "Unit tests, integration tests, E2E tests", 16, "medium"),
            Task(tid + 1, "Deployment", "Production deployment and monitoring", 8, "medium"),
        ])

        return base_tasks

    def _identify_risks(self, tasks: list) -> list:
        risks = []
        total = sum(t.estimate_hours for t in tasks)
        if total > 200:
            risks.append({"risk": "Large project scope", "mitigation": "Consider phased delivery"})
        high_deps = [t for t in tasks if len(t.dependencies) > 2]
        if high_deps:
            risks.append({"risk": "High dependency chain", "mitigation": "Parallelize independent tasks"})
        return risks

    def export_gantt(self, plan: ProjectPlan) -> list:
        current_hour = 0
        schedule = []
        for task in plan.tasks:
            schedule.append({
                "task": task.title,
                "start": current_hour,
                "end": current_hour + task.estimate_hours,
                "hours": task.estimate_hours,
            })
            current_hour += task.estimate_hours * 0.7
        return schedule

def main():
    if len(sys.argv) < 3:
        print("Usage: python main.py plan 'project description'")
        sys.exit(1)
    pm = ProjectManager()
    desc = " ".join(sys.argv[2:])
    plan = pm.plan(desc)
    print(f"Project: {plan.name}")
    print(f"Total: {plan.total_hours}h ({plan.estimated_weeks} weeks)")
    print(f"\nTasks ({len(plan.tasks)}):")
    for t in plan.tasks:
        print(f"  [{t.priority}] {t.title} - {t.estimate_hours}h")

if __name__ == "__main__":
    main()
