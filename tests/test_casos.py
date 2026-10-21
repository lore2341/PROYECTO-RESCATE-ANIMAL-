import unittest

from rescate.fabrica import CREADORES
from rescate.gestor import GestorCasos
from rescate.modelo import EstadoCaso, Reportante, Veterinario, Voluntario


class TestCasos(unittest.TestCase):
    def setUp(self):
        self.gestor = GestorCasos()
        self.gestor._casos.clear()
        self.gestor._observadores.clear()
        self.reportante = Reportante("Carlos", "0991111111")
        self.voluntario = Voluntario("Ana", "ana@refugio.ec")
        self.veterinario = Veterinario("Dr. Pepe", "pepe@refugio.ec", "VET-001")

    def test_transiciones_validas(self):
        exp = CREADORES["perro"]().crear_expediente("Perro herido", "Portoviejo", self.reportante)
        self.gestor.registrar_caso(exp)
        self.gestor.cambiar_estado(exp.id, EstadoCaso.EN_TRATAMIENTO)
        self.assertEqual(exp.estado, EstadoCaso.EN_TRATAMIENTO)
        self.gestor.cambiar_estado(exp.id, EstadoCaso.EN_ADOPCION)
        self.assertEqual(exp.estado, EstadoCaso.EN_ADOPCION)
        self.gestor.cambiar_estado(exp.id, EstadoCaso.ADOPTADO)
        self.assertEqual(exp.estado, EstadoCaso.ADOPTADO)

    def test_transicion_invalida(self):
        exp = CREADORES["perro"]().crear_expediente("Perro herido", "Portoviejo", self.reportante)
        self.gestor.registrar_caso(exp)
        with self.assertRaises(ValueError):
            self.gestor.cambiar_estado(exp.id, EstadoCaso.ADOPTADO)

    def test_fauna_silvestre_no_puede_adoptarse(self):
        exp = CREADORES["fauna"]().crear_expediente("Mono en patio", "Manta", self.reportante)
        self.gestor.registrar_caso(exp)
        self.gestor.cambiar_estado(exp.id, EstadoCaso.EN_TRATAMIENTO)
        with self.assertRaises(ValueError):
            self.gestor.cambiar_estado(exp.id, EstadoCaso.EN_ADOPCION)
        with self.assertRaises(ValueError):
            self.gestor.cambiar_estado(exp.id, EstadoCaso.ADOPTADO)

    def test_factory_crea_clase_correcta(self):
        perro = CREADORES["perro"]().crear_expediente("Perro", "Portoviejo", self.reportante)
        gato = CREADORES["gato"]().crear_expediente("Gato", "Manta", self.reportante)
        fauna = CREADORES["fauna"]().crear_expediente("Mono", "Bahia", self.reportante)
        self.assertEqual(perro.especie, "Perro")
        self.assertEqual(gato.especie, "Gato")
        self.assertEqual(fauna.especie, "Fauna Silvestre")

    def test_observer_notifica(self):
        self.gestor.suscribir(self.voluntario)
        self.gestor.suscribir(self.veterinario)
        exp = CREADORES["perro"]().crear_expediente("Perro herido", "Portoviejo", self.reportante)
        self.gestor.registrar_caso(exp)
        self.assertTrue(self.voluntario.bandeja)
        self.assertTrue(self.veterinario.bandeja)

    def test_singleton_una_instancia(self):
        gestor_1 = GestorCasos()
        gestor_2 = GestorCasos()
        self.assertIs(gestor_1, gestor_2)


if __name__ == "__main__":
    unittest.main()
