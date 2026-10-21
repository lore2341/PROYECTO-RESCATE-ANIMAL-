"""Patrones Singleton (instancia única) y Observer (sujeto observable)."""
from .modelo import Expediente, Observador


class GestorCasos:
    """Singleton + Sujeto del Observer. Única fuente de verdad de los casos."""
    _instancia = None

    def __new__(cls):
        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
            cls._instancia._casos = {}
            cls._instancia._observadores = []
        return cls._instancia

    # --- Observer ---
    def suscribir(self, obs: Observador):
        if obs not in self._observadores:
            self._observadores.append(obs)

    def desuscribir(self, obs: Observador):
        if obs in self._observadores:
            self._observadores.remove(obs)

    def _notificar(self, evento: str, exp: Expediente):
        for obs in self._observadores:
            obs.actualizar(evento, exp)

    # --- Operaciones del negocio ---
    def registrar_caso(self, exp: Expediente):
        if exp is None:
            raise ValueError("Debe indicar un expediente válido.")
        if not exp.descripcion or not exp.descripcion.strip():
            raise ValueError("La descripción del caso no puede estar vacía.")
        if exp.id in self._casos:
            raise ValueError(f"El caso #{exp.id} ya existe.")
        self._casos[exp.id] = exp
        self._notificar("Nuevo rescate ingresado", exp)

    def asignar(self, id_caso, responsable):
        if id_caso not in self._casos:
            raise ValueError(f"El caso {id_caso} no existe.")
        if responsable is None:
            raise ValueError("Debe indicar un responsable válido.")
        exp = self._casos[id_caso]
        exp.asignar_responsable(responsable)
        self._notificar("Caso asignado", exp)

    def cambiar_estado(self, id_caso, nuevo_estado):
        if id_caso not in self._casos:
            raise ValueError(f"El caso {id_caso} no existe.")
        exp = self._casos[id_caso]
        exp.cambiar_estado(nuevo_estado)
        self._notificar("Cambio de estado", exp)

    def listar_por_estado(self, estado):
        if estado is None:
            raise ValueError("Debe indicar un estado válido.")
        return [caso for caso in self._casos.values() if caso.estado == estado]

    def listar(self):
        return list(self._casos.values())
