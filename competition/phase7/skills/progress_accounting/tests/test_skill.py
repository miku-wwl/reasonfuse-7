from competition.phase7.skills.progress_accounting.self_tests import run_self_tests


def test_progress_accounting_has_twenty_passing_cases():
    cases = run_self_tests()
    assert len(cases) >= 20
    assert all(case["passed"] for case in cases), cases
