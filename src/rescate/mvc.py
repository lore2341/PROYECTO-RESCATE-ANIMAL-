"""MVC: Vista (consola) y Controlador. El Modelo está en modelo.py y gestor.py."""
from .fabrica import CREADORES
from .gestor import GestorCasos
from .modelo import EstadoCaso, Veterinario, Voluntario


class VistaConsola:
    def mostrar(self, mensaje: str):
        print(mensaje)

    def mostrar_casos(self, casos):
        print("\n--- Casos del refugio ---")
        for c in casos:
            resp = c.responsable.nombre if c.responsable else "sin asignar"
            print(f"{c.resumen()} | Responsable: {resp}")


class ControladorCasos:
    def __init__(self, vista: VistaConsola):
        self.vista = vista
        self.gestor = GestorCasos()

    def reportar(self, especie, descripcion, ubicacion, reportante):
        if not especie or not isinstance(especie, str):
            raise ValueError("La especie es obligatoria.")
        especie_normalizada = especie.lower()
        if especie_normalizada not in CREADORES:
            raise ValueError(f"La especie '{especie}' no es válida.")
        if not descripcion or not descripcion.strip():
            raise ValueError("La descripción del rescate no puede estar vacía.")
        if not ubicacion or not ubicacion.strip():
            raise ValueError("La ubicación del rescate no puede estar vacía.")
        if reportante is None:
            raise ValueError("Debe indicar el reportante del caso.")

        creador = CREADORES[especie_normalizada]()
        exp = creador.registrar(descripcion, ubicacion, reportante)
        self.gestor.registrar_caso(exp)
        return exp

    def asignar(self, id_caso, responsable):
        if not isinstance(responsable, (Voluntario, Veterinario)):
            raise ValueError("El responsable debe ser un Voluntario o Veterinario.")
        self.gestor.asignar(id_caso, responsable)

    def avanzar(self, id_caso, estado: EstadoCaso):
        try:
            self.gestor.cambiar_estado(id_caso, estado)
        except ValueError as e:
            self.vista.mostrar(f"ERROR: {e}")

    def ver_todo(self):
        self.vista.mostrar_casos(self.gestor.listar())

    def ver_por_estado(self, estado: EstadoCaso):
        self.vista.mostrar_casos(self.gestor.listar_por_estado(estado))
