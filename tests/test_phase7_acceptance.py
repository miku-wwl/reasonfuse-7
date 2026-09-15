import unittest

from competition.phase7.evaluation.acceptance import run_acceptance


class Phase7AcceptanceTests(unittest.TestCase):
    def test_p0_acceptance(self):
        report = run_acceptance()
        self.assertTrue(report["pass"], report)


if __name__ == "__main__":
    unittest.main()
