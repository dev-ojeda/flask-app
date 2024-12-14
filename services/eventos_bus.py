from model.empleado import Empleado


class EventEmitter:
    def __init__(self):
        self.listeners = {}

    def on(self, event_name, listener):
        """Registra un listener para un evento"""
        if event_name == "ListarEmpleado":
            return
        else:
            if event_name not in self.listeners:
                self.listeners[event_name] = []
            self.listeners[event_name].append(listener)

    def emit(self, event_name, data):
        """Emite un evento a todos los listeners registrados"""
        if event_name == "ListarEmpleado":
            return
        else:
            if event_name in self.listeners:
                for listener in self.listeners[event_name]:
                    listener(data)


# Servicio que crea pedidos
class EmpleadoService:
    def __init__(self, event_bus, event_name, name_funcion):
        self.event_bus = event_bus
        self.event_name = event_name
        self.name_funcion = name_funcion
        self.event_bus.on(self.event_name, self.name_funcion)

    def eliminar_empleado(self, empleados):
        print(f"Empleado eliminado: {empleados}")
        # Emitir el evento EliminarEmpleado
        self.event_bus.emit("EliminarEmpleado", empleados)

    def listar_empleado(self) -> list[dict]:
        objEmpleado = Empleado()
        return objEmpleado.cargar_empleados_to_dict()
