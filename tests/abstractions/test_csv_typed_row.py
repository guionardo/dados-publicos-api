import unittest

from src.domain.motivo import MotivoRow


class TestCSVTypedRow(unittest.TestCase):

    def test_0(self):
        motivo = MotivoRow().from_row('"00";"SEM MOTIVO"')
        self.assertIsNotNone(motivo)
        self.assertEqual(0, motivo.cod)
        self.assertEqual('SEM MOTIVO', motivo.motivo)
