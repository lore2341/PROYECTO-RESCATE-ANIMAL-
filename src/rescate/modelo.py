"""Modelo (M de MVC): entidades del dominio."""
from abc import ABC, abstractmethod
from datetime import date
from enum import Enum


class EstadoCaso(Enum):
    RESCATADO = "Rescatado"
    EN_TRATAMIENTO = "En Tratamiento"
    EN_ADOPCION = "En Adopción"
    ADOPTADO = "Adoptado"


# Transiciones permitidas: evita saltos inválidos (ej. Rescatado -> Adoptado)
TRANSICIONES = {
    EstadoCaso.RESCATADO: [EstadoCaso.EN_TRATAMIENTO],
    EstadoCaso.EN_TRATAMIENTO: [EstadoCaso.EN_ADOPCION],
    EstadoCaso.EN_ADOPCION: [EstadoCaso.ADOPTADO],
    EstadoCaso.ADOPTADO: [],
}


class Observador(ABC):
    """Interfaz Observer (ISP): solo exige el método que necesita."""

    @abstractmethod
    def actualizar(self, evento: str, expediente: "Expediente") -> None: ...


class Persona:
    def __init__(self, nombre: str, contacto: str):
        self.nombre = nombre
        self.contacto = contacto


class Reportante(Persona):
    """Ciudadano que reporta un animal."""


class Voluntario(Persona, Observador):
    """Voluntario: también es observador de nuevos rescates."""

    def __init__(self, nombre, contacto):
        super().__init__(nombre, contacto)
        self.bandeja = []

    def actualizar(self, evento, expediente):
        self.bandeja.append(f"[{self.nombre}] {evento}: {expediente.resumen()}")
        print(self.bandeja[-1])


class Veterinario(Voluntario):
    """Veterinario: voluntario con especialidad médica."""

    def __init__(self, nombre, contacto, registro: str):
        super().__init__(nombre, contacto)
        self.registro = registro


class Administrador(Persona):
    """Administra el refugio y gestiona usuarios y casos."""


class Expediente(ABC):
    """Producto abstracto del Factory Method."""
    _contador = 0

    def __init__(self, descripcion: str, ubicacion: str, reportante: Reportante):
        Expediente._contador += 1
        self.id = Expediente._contador
        self.descripcion = descripcion
        self.ubicacion = ubicacion
        self.reportante = reportante
        self.fecha_ingreso = date.today()
        self.estado = EstadoCaso.RESCATADO
        self.responsable = None
        self.historial = [(self.fecha_ingreso, self.estado)]

    @property
    @abstractmethod
    def especie(self) -> str: ...

    @abstractmethod
    def requisitos_especiales(self) -> str: ...

    def asignar_responsable(self, responsable: Voluntario):
        self.responsable = responsable

    def cambiar_estado(self, nuevo: EstadoCaso):
        if nuevo not in TRANSICIONES[self.estado]:
            raise ValueError(f"Transición inválida: {self.estado.value} -> {nuevo.value}")
        self.estado = nuevo
        self.historial.append((date.today(), nuevo))

    def resumen(self) -> str:
        return f"#{self.id} {self.especie} - {self.ubicacion} ({self.estado.value})"


class ExpedientePerro(Expediente):
    especie = "Perro"
    def requisitos_especiales(self): return "Vacunas y desparasitación"


class ExpedienteGato(Expediente):
    especie = "Gato"
    def requisitos_especiales(self): return "Vacunas y esterilización"


class ExpedienteFaunaSilvestre(Expediente):
    especie = "Fauna Silvestre"
    def requisitos_especiales(self): return "Aviso a autoridad ambiental; no apto para adopción"

    def cambiar_estado(self, nuevo):
        # Regla propia: la fauna silvestre se libera, no se adopta
        if nuevo in (EstadoCaso.EN_ADOPCION, EstadoCaso.ADOPTADO):
            raise ValueError("La fauna silvestre no puede ir a adopción")
        super().cambiar_estado(nuevo)
