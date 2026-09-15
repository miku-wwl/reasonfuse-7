from competition.phase7.skills.approval_control.self_tests import run_self_tests


def test_approval_control_has_twenty_passing_cases():
    cases = run_self_tests()
    assert len(cases) >= 20
    assert all(case["passed"] for case in cases), cases
