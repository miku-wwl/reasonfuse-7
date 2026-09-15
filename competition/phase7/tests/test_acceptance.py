from competition.phase7.evaluation.acceptance import run_acceptance


def test_phase7_p0_acceptance():
    report = run_acceptance()
    assert report["pass"], report
