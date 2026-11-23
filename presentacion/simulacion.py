# Importa la clase Cliente y la clase base abstracta Servicio
from modelos.cliente import Cliente
from modelos.servicio import Servicio

# Importa los controladores que administran clientes, servicios y reservas
from controladores.gestor_clientes import GestorClientes
from controladores.gestor_servicios import GestorServicios
from controladores.gestor_reservas import GestorReservas

# Importa las funciones para registrar eventos y errores en el archivo de logs
from registros.registro_logs import registrar_evento, registrar_error


class ServicioDemostracion(Servicio):
    """Servicio concreto utilizado para probar la integración del sistema."""

    def calcular_costo(self, cantidad=1, descuento=0, impuesto=0.19):
        # Verifica que la cantidad o duración sea mayor que cero
        if cantidad <= 0:
            raise ValueError("La duración debe ser mayor que cero.")

        # Calcula el subtotal multiplicando precio base por cantidad y aplicando descuento
        subtotal = self.precio_base * cantidad
        subtotal -= subtotal * (descuento / 100)

        # Devuelve el total redondeado a dos decimales sumando el impuesto
        return round(subtotal * (1 + impuesto), 2)

    def describir(self):
        # Devuelve una descripción breve con nombre y detalle del servicio
        return f"{self.nombre}: {self.descripcion}"

    def validar_parametros(self, cantidad=1, **kwargs):
        # Comprueba que la duración sea un número positivo válido
        if not isinstance(cantidad, (int, float)) or cantidad <= 0:
            raise ValueError("La duración debe ser un número positivo.")

        return True


def ejecutar_operacion(numero, descripcion, funcion):
    """Ejecuta una operación y controla sus posibles errores."""

    # Muestra en consola qué operación de prueba se está corriendo
    print(f"\nOPERACIÓN {numero}: {descripcion}")

    try:
        # Ejecuta la función de prueba recibida
        funcion()

    except Exception as error:
        # Si ocurre un error, lo guarda en el log y lo informa sin detener la simulación
        registrar_error(
            f"Operación {numero} fallida: {descripcion}",
            error
        )
        print(f"ERROR CONTROLADO: {error}")

    else:
        # Si todo salió bien sin errores, registra el éxito en el log
        registrar_evento(
            f"Operación {numero} ejecutada correctamente: {descripcion}"
        )
        print("Resultado: CORRECTO")

    finally:
        # Siempre se ejecuta al terminar la operación, haya dado error o no
        print(f"Operación {numero} finalizada.")


def ejecutar_simulacion():
    """Ejecuta operaciones para comprobar el funcionamiento integral."""

    # Registra el inicio de toda la simulación en el log
    registrar_evento("Inicio de la simulación integral de Software FJ")

    # Crea las instancias de los gestores en memoria (sin base de datos)
    gestor_clientes = GestorClientes()
    gestor_servicios = GestorServicios()

    gestor_reservas = GestorReservas(
        gestor_clientes,
        gestor_servicios
    )

    # Diccionario temporal para guardar objetos creados durante las pruebas
    datos = {}

    # 1. Registrar un cliente válido.
    def registrar_cliente():
        cliente = Cliente(
            "Sergio Diaz",
            "1098765432",
            "sergio@email.com",
            "3001234567"
        )

        gestor_clientes.registrar_cliente(cliente)
        datos["cliente"] = cliente

        print("Cliente registrado correctamente.")

    ejecutar_operacion(
        1,
        "Registrar un cliente válido",
        registrar_cliente
    )

    # 2. Buscar el cliente registrado.
    def buscar_cliente():
        cliente = gestor_clientes.buscar_por_documento("1098765432")

        print(f"Cliente encontrado: {cliente.nombre}")

    ejecutar_operacion(
        2,
        "Buscar un cliente por documento",
        buscar_cliente
    )

    # 3. Intentar registrar un documento duplicado.
    def registrar_duplicado():
        cliente = Cliente(
            "Cliente Duplicado",
            "1098765432",
            "duplicado@email.com",
            "3112223344"
        )

        gestor_clientes.registrar_cliente(cliente)

    ejecutar_operacion(
        3,
        "Impedir el registro de un documento duplicado",
        registrar_duplicado
    )

    # 4. Registrar un servicio disponible.
    def registrar_servicio():
        servicio = ServicioDemostracion(
            "Servicio de sala",
            "Alquiler de sala para reuniones",
            100000,
            True
        )

        gestor_servicios.registrar_servicio(servicio)
        datos["servicio"] = servicio

        print("Servicio registrado correctamente.")

    ejecutar_operacion(
        4,
        "Registrar un servicio disponible",
        registrar_servicio
    )

    # 5. Registrar un servicio no disponible.
    def registrar_servicio_no_disponible():
        servicio = ServicioDemostracion(
            "Sala en mantenimiento",
            "Sala temporalmente fuera de servicio",
            80000,
            False
        )

        gestor_servicios.registrar_servicio(servicio)
        datos["servicio_no_disponible"] = servicio

        print("Servicio no disponible registrado.")

    ejecutar_operacion(
        5,
        "Registrar un servicio no disponible",
        registrar_servicio_no_disponible
    )

    # 6. Crear una reserva válida.
    def crear_reserva():
        reserva = gestor_reservas.crear_reserva(
            "1098765432",
            datos["servicio"].id,
            2
        )

        datos["reserva"] = reserva

        print("Reserva creada correctamente.")

    ejecutar_operacion(
        6,
        "Crear una reserva válida",
        crear_reserva
    )

    # 7. Intentar reservar con un cliente inexistente.
    def reserva_cliente_inexistente():
        gestor_reservas.crear_reserva(
            "9999999999",
            datos["servicio"].id,
            1
        )

    ejecutar_operacion(
        7,
        "Controlar una reserva con cliente inexistente",
        reserva_cliente_inexistente
    )

    # 8. Confirmar la reserva.
    def confirmar_reserva():
        gestor_reservas.confirmar_reserva(
            datos["reserva"].id
        )

        print("Reserva confirmada correctamente.")

    ejecutar_operacion(
        8,
        "Confirmar una reserva pendiente",
        confirmar_reserva
    )

    # 9. Intentar confirmar nuevamente.
    def confirmar_dos_veces():
        gestor_reservas.confirmar_reserva(
            datos["reserva"].id
        )

    ejecutar_operacion(
        9,
        "Impedir la confirmación repetida de una reserva",
        confirmar_dos_veces
    )

    # 10. Completar la reserva confirmada.
    def completar_reserva():
        gestor_reservas.completar_reserva(
            datos["reserva"].id
        )

        print("Reserva completada correctamente.")

    ejecutar_operacion(
        10,
        "Completar una reserva confirmada",
        completar_reserva
    )

    # 11. Intentar reservar un servicio no disponible.
    def reservar_servicio_no_disponible():
        gestor_reservas.crear_reserva(
            "1098765432",
            datos["servicio_no_disponible"].id,
            1
        )

    ejecutar_operacion(
        11,
        "Impedir reservas de servicios no disponibles",
        reservar_servicio_no_disponible
    )

    # 12. Intentar crear una reserva con duración inválida.
    def reserva_duracion_invalida():
        gestor_reservas.crear_reserva(
            "1098765432",
            datos["servicio"].id,
            0
        )

    ejecutar_operacion(
        12,
        "Controlar una duración de reserva inválida",
        reserva_duracion_invalida
    )

    # 13. Consultar las reservas existentes.
    def listar_reservas():
        reservas = gestor_reservas.listar_reservas()

        print(f"Total de reservas registradas: {len(reservas)}")

    ejecutar_operacion(
        13,
        "Consultar las reservas registradas",
        listar_reservas
    )

    # Registra el fin de la simulación en el archivo de logs
    registrar_evento("Finalización de la simulación integral de Software FJ")

    # Imprime el resumen final de cuántos elementos quedaron creados
    print("\n======================================")
    print("SIMULACIÓN FINALIZADA")
    print("======================================")
    print(f"Clientes registrados: {gestor_clientes.cantidad_clientes}")
    print(f"Servicios registrados: {gestor_servicios.cantidad_servicios}")
    print(f"Reservas registradas: {gestor_reservas.cantidad_reservas}")


# Ejecuta la simulación si este archivo se corre directamente
if __name__ == "__main__":
    ejecutar_simulacion()
    