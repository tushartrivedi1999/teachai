from collections.abc import Iterable

MAX_OBJECTIVES = 8


def _normalize_objectives(objectives: Iterable[str], title: str, field: str) -> list[str]:
    cleaned = []
    seen = set()
    for objective in objectives:
        value = objective.strip()
        if not value:
            continue
        key = value.casefold()
        if key in seen:
            continue
        seen.add(key)
        cleaned.append(value)
        if len(cleaned) >= MAX_OBJECTIVES:
            break

    if cleaned:
        return cleaned

    return [
        f"Understand fundamentals of {field}",
        f"Build practical project in {title}",
        "Assess knowledge with quizzes and mock interviews",
    ]


def build_course_outline(title: str, field: str, level: str, objectives: Iterable[str]) -> dict:
    normalized_objectives = _normalize_objectives(objectives, title=title, field=field)

    modules = [
        {
            "name": "Foundations",
            "topics": [
                f"Introduction to {title}",
                f"Core concepts in {field}",
                "Learning roadmap and milestones",
            ],
            "practical": "Set up your workspace and complete a baseline mini-task",
            "assessment": "Module quiz (proctored)",
        },
        {
            "name": "Applied Learning",
            "topics": normalized_objectives,
            "practical": "Guided project implementation with AI mentor feedback",
            "assessment": "Code/design review + scenario-based questions",
        },
        {
            "name": "Career and Research Readiness",
            "topics": [
                "Interview preparation",
                "Portfolio and certificate readiness",
                "Research methods and publication guidance",
            ],
            "practical": "Final capstone project and presentation",
            "assessment": "Final viva + benchmark test",
        },
    ]

    return {
        "title": title,
        "field": field,
        "level": level,
        "modules": modules,
        "brain_map": {
            "center": title,
            "nodes": [m["name"] for m in modules],
        },
        "weekly_plan": [
            {"week": i + 1, "goal": mod["name"]}
            for i, mod in enumerate(modules)
        ],
    }
