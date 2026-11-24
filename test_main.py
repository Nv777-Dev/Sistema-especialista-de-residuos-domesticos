import unittest
from main import BASE, inferir, normalizar, proximo_estado


class TestInferencia(unittest.TestCase):
    def test_categorias(self):
        casos = [
            ('PAPEL', 'Reciclável'),
            ('  borra de café  ', 'Orgânico'),
            ('fralda', 'Rejeito'),
            ('pilha', 'Descarte especial'),
            ('objeto desconhecido', 'Não identificado'),
            ('', 'Não identificado'),
            ('garrafa   PET', 'Reciclável'),
        ]
        for entrada, esperado in casos:
            with self.subTest(entrada=entrada):
                self.assertEqual(inferir(entrada)[0], esperado)

    def test_regras_e_orientacoes(self):
        self.assertEqual(inferir('pilha')[2], 'R1')
        self.assertEqual(inferir('papel')[2], 'R2')
        self.assertEqual(inferir('borra de café')[2], 'R3')
        self.assertEqual(inferir('fralda')[2], 'R4')
        self.assertEqual(inferir('item inexistente')[2], 'R5')
        self.assertTrue(len(inferir('papel')[1]) > 0)

    def test_normalizacao(self):
        self.assertEqual(normalizar('  Lâmpada   Fluorescente  '), 'lampada fluorescente')
        self.assertEqual(normalizar('Óleo de Cozinha'), 'oleo de cozinha')
        self.assertEqual(normalizar('   '), '')

    def test_base_conhecimento_21_itens(self):
        total = sum(len(itens) for itens in BASE.values())
        self.assertEqual(total, 21)


class TestMaquinaDeEstados(unittest.TestCase):
    def test_transicoes_menu(self):
        self.assertEqual(proximo_estado('MENU', '1'), 'CLASSIFICAR')
        self.assertEqual(proximo_estado('MENU', '2'), 'HISTORICO')
        self.assertEqual(proximo_estado('MENU', '3'), 'FIM')
        self.assertEqual(proximo_estado('MENU', '9'), 'MENU')

    def test_retorno_ao_menu(self):
        self.assertEqual(proximo_estado('CLASSIFICAR', 'concluida'), 'MENU')
        self.assertEqual(proximo_estado('HISTORICO', 'concluida'), 'MENU')


if __name__ == '__main__':
    unittest.main()
