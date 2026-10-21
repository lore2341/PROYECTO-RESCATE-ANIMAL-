"""Patrón Factory Method: crea el expediente según la especie."""
from abc import ABC, abstractmethod
from .modelo import (Expediente, ExpedientePerro, ExpedienteGato,
                     ExpedienteFaunaSilvestre)


class CreadorExpediente(ABC):
    @abstractmethod
    def crear_expediente(self, descripcion, ubicacion, reportante) -> Expediente: ...

    def registrar(self, descripcion, ubicacion, reportante) -> Expediente:
        """Método plantilla: usa el factory method sin conocer la clase concreta."""
        exp = self.crear_expediente(descripcion, ubicacion, reportante)
        print(f"Expediente creado: {exp.resumen()} | {exp.requisitos_especiales()}")
        return exp


class CreadorPerro(CreadorExpediente):
    def crear_expediente(self, d, u, r): return ExpedientePerro(d, u, r)


class CreadorGato(CreadorExpediente):
    def crear_expediente(self, d, u, r): return ExpedienteGato(d, u, r)


class CreadorFaunaSilvestre(CreadorExpediente):
    def crear_expediente(self, d, u, r): return ExpedienteFaunaSilvestre(d, u, r)


CREADORES = {"perro": CreadorPerro, "gato": CreadorGato, "fauna": CreadorFaunaSilvestre}
