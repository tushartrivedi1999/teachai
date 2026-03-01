from app.services.course_generator import build_course_outline


def test_course_outline_has_modules():
    outline = build_course_outline("Python", "development", "beginner", ["syntax", "project"])
    assert outline["title"] == "Python"
    assert len(outline["modules"]) == 3
    assert outline["brain_map"]["center"] == "Python"


def test_course_outline_objectives_are_deduped_and_trimmed():
    outline = build_course_outline(
        "Data Science",
        "engineering",
        "intermediate",
        [" pandas ", "PANDAS", "", "modeling"],
    )
    applied_topics = outline["modules"][1]["topics"]
    assert applied_topics == ["pandas", "modeling"]
