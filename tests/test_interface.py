"""Verificação funcional: python3 -m unittest discover -s tests."""
import unittest
from unittest.mock import patch
from pathlib import Path
import numpy as np
from streamlit.testing.v1 import AppTest


class InterfaceTest(unittest.TestCase):
    def test_modelo_ausente(self):
        original = Path.exists
        def existe(caminho):
            return False if caminho.name == 'gerador.pt' else original(caminho)
        with patch.object(Path, 'exists', existe):
            app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / 'app.py'), default_timeout=60).run()
            self.assertFalse(app.exception)
            self.assertTrue(any('Modelo local ausente' in x.value for x in app.warning))

    def test_comparacao_e_geracao(self):
        app = AppTest.from_file(str(Path(__file__).resolve().parents[1] / 'app.py'), default_timeout=60).run()
        self.assertFalse(app.exception)
        app.radio[0].set_value('Local').run()
        self.assertFalse(app.exception)
        app.button[0].click().run()
        self.assertFalse(app.exception)
        primeira = app.session_state['imagens'].copy()
        self.assertEqual(primeira.shape, (16, 28, 28))
        self.assertTrue(np.isfinite(primeira).all())
        self.assertTrue(((primeira >= 0) & (primeira <= 1)).all())
        app.button[0].click().run()
        np.testing.assert_array_equal(primeira, app.session_state['imagens'])
        app.number_input[0].set_value(456).run()
        app.button[0].click().run()
        self.assertFalse(app.exception)
        self.assertFalse(np.array_equal(primeira, app.session_state['imagens']))


if __name__ == '__main__':
    unittest.main()
