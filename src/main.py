from rescate.gestor import GestorCasos
from rescate.modelo import EstadoCaso, Reportante, Veterinario, Voluntario
from rescate.mvc import ControladorCasos, VistaConsola

ctrl = ControladorCasos(VistaConsola())
assert GestorCasos() is ctrl.gestor  # Singleton: misma instancia

ana = Voluntario("Ana", "ana@refugio.ec")
dr = Veterinario("Dr. Pepe", "Pepe@refugio.ec", "VET-123")
ctrl.gestor.suscribir(ana)
ctrl.gestor.suscribir(dr)

ciudadano = Reportante("Carlos", "0990000000")
print("== 1. Reportar rescates ==")
c1 = ctrl.reportar("perro", "Perro herido en la vía", "Portoviejo, centro", ciudadano)
c2 = ctrl.reportar("fauna", "Mono ardilla en patio", "Manta, Tarqui", ciudadano)

print("\n== 2. Asignar responsable ==")
ctrl.asignar(c1.id, dr)

print("\n== 3. Cambios de estado ==")
ctrl.avanzar(c1.id, EstadoCaso.EN_TRATAMIENTO)
ctrl.avanzar(c1.id, EstadoCaso.ADOPTADO)       # inválido
ctrl.avanzar(c2.id, EstadoCaso.EN_TRATAMIENTO)
ctrl.avanzar(c2.id, EstadoCaso.EN_ADOPCION)    # inválido para fauna

ctrl.ver_todo()
