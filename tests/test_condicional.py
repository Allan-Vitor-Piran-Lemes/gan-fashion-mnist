"""Testes das redes definidas nos notebooks, sem executar treinamento longo."""
import json
from pathlib import Path
import unittest
import torch

RAIZ = Path(__file__).resolve().parents[1]

def arquitetura(nome):
    nb = json.loads((RAIZ / 'notebooks' / nome).read_text())
    return next(c['source'] for c in nb['cells'] if c['cell_type'] == 'code' and 'class GeradorCondicional' in c['source'])

class CondicionalTest(unittest.TestCase):
    def test_definicoes_consistentes(self):
        self.assertEqual(arquitetura('02_treinar_gan_condicional.ipynb'),
                         arquitetura('03_evolucao_e_geracao_condicional.ipynb'))

    def test_condicao_e_gradientes(self):
        torch.set_num_threads(2)
        torch.manual_seed(42)
        contexto = {'torch': torch, 'nn': torch.nn}
        exec(arquitetura('02_treinar_gan_condicional.ipynb'), contexto)
        g = contexto['GeradorCondicional']().eval()
        d = contexto['DiscriminadorCondicional']().eval()
        ruido = torch.randn(2,100,1,1).repeat(2,1,1,1)
        classes = torch.tensor([0,0,1,1])
        imagens = g(ruido, classes)
        self.assertEqual(tuple(imagens.shape), (4,1,28,28))
        self.assertFalse(torch.allclose(imagens[:2], imagens[2:]))
        self.assertFalse(torch.allclose(d(imagens[:2],classes[:2]), d(imagens[:2],classes[2:])))
        d(imagens,classes).sum().backward()
        self.assertGreater(g.classe.weight.grad.abs().sum().item(),0)
        self.assertGreater(d.classe.weight.grad.abs().sum().item(),0)

if __name__ == '__main__':
    unittest.main()
