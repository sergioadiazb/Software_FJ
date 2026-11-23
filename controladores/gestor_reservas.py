"""
Módulo encargado de administrar las reservas de Software FJ.

Integra los gestores de clientes y servicios para crear y administrar
reservas. Mantiene las reservas en una lista interna y registra
los eventos y errores de las operaciones realizadas.
"""

# Importa el modelo Reserva y ServicioEquipo para validar alquiler de equipos
from modelos.reserva import Reserva
from servicios.servicio_equipo import ServicioEquipo

# Importa las excepciones personalizadas del sistema para controlar errores
from utilidades.excepciones import (
    ErrorValidacion,
    ClienteNoEncontradoError,
    ServicioNoEncontradoError,
    ServicioNoDisponibleError,
    ReservaNoEncontradaError,
    OperacionNoPermitidaError,
    CapacidadInsuficienteError
)

# Importa las funciones encargadas de registrar eventos y errores
from registros.registro_logs import (
    registrar_evento,
    registrar_error
)


# Define la clase encargada de gestionar el ciclo de vida de las reservas
class GestorReservas:
    """
    Administra las reservas y coordina los gestores de clientes
    y servicios.
    """

    # Constructor que recibe los gestores de clientes y servicios e inicializa la lista
    def __init__(self, gestor_clientes, gestor_servicios):
        """
        Inicializa el gestor de reservas.

        Args:
            gestor_clientes: Gestor encargado de administrar clientes.
            gestor_servicios: Gestor encargado de administrar servicios.
        """

        # Exige que ambos gestores existan para poder operar
        if gestor_clientes is None or gestor_servicios is None:
            raise ErrorValidacion(
                "Se requieren los gestores de clientes y servicios."
            )

        # Guarda referencias privadas a los gestores y crea la lista interna de reservas
        self.__gestor_clientes = gestor_clientes
        self.__gestor_servicios = gestor_servicios
        self.__reservas = []

        # Registra en el log que el gestor se inicializó correctamente
        registrar_evento(
            "Gestor de reservas inicializado correctamente"
        )

    # Propiedad de solo lectura que retorna cuántas reservas hay registradas
    @property
    def cantidad_reservas(self):
        """Devuelve la cantidad de reservas registradas."""
        return len(self.__reservas)

    # Crea una reserva en estado pendiente validando cliente, servicio y disponibilidad
    def crear_reserva(
        self,
        documento_cliente,
        identificador_servicio,
        duracion,
        unidades=1
    ):
        """
        Crea una reserva utilizando un cliente y un servicio existentes.

        La reserva se crea inicialmente en estado pendiente.
        Su confirmación y cálculo definitivo se realizan por separado.

        Args:
            documento_cliente (str): Documento del cliente.
            identificador_servicio (str): ID del servicio.
            duracion (float): Duración solicitada.
            unidades (int): Unidades de equipo solicitadas.

        Returns:
            Reserva: Reserva creada y registrada.
        """

        try:
            # Recupera el cliente y el servicio desde sus gestores.
            cliente = self.__gestor_clientes.buscar_por_documento(
                documento_cliente
            )

            servicio = self.__gestor_servicios.buscar_por_id(
                identificador_servicio
            )

            # Comprueba que el servicio esté disponible.
            if not servicio.disponible:
                raise ServicioNoDisponibleError(
                    f"El servicio '{servicio.nombre}' no está disponible."
                )

            # Comprueba las unidades solicitadas cuando se alquilan equipos.
            if isinstance(servicio, ServicioEquipo):
                if unidades > servicio.unidades_disponibles:
                    raise CapacidadInsuficienteError(
                        f"Se solicitaron {unidades} unidades, "
                        f"pero solo hay {servicio.unidades_disponibles} "
                        "disponibles."
                    )

            # Construye la reserva con los objetos existentes.
            reserva = Reserva(
                cliente,
                servicio,
                duracion,
                unidades
            )

            # Valida la relación entre cliente, servicio y duración.
            reserva.validar()

            # Incorpora la reserva a la lista interna.
            self.__reservas.append(reserva)

            # Registra la creación exitosa de la reserva en el log
            registrar_evento(
                f"Reserva creada: {reserva.id} | "
                f"Cliente: {cliente.documento} | "
                f"Servicio: {servicio.nombre}"
            )

            return reserva

        except (
            ClienteNoEncontradoError,
            ServicioNoEncontradoError,
            ServicioNoDisponibleError,
            CapacidadInsuficienteError,
            ErrorValidacion
        ) as error:
            # Registra el error de dominio y vuelve a lanzarlo
            registrar_error(
                "No fue posible crear la reserva",
                error
            )
            raise

        except (TypeError, ValueError) as error:
            # Convierte errores de tipo o valor en ErrorValidacion
            registrar_error(
                "Datos inválidos durante la creación de una reserva",
                error
            )

            raise ErrorValidacion(
                "No se pudo crear la reserva debido a datos inválidos."
            ) from error

    # Busca una reserva existente por su identificador único
    def buscar_por_id(self, identificador):
        """
        Busca una reserva mediante su identificador único.

        Args:
            identificador (str): Identificador de la reserva.

        Returns:
            Reserva: Reserva encontrada.

        Raises:
            ErrorValidacion: Si el identificador es inválido.
            ReservaNoEncontradaError: Si no existe la reserva.
        """

        # Valida que el identificador sea una cadena de texto no vacía
        if (
            not isinstance(identificador, str)
            or not identificador.strip()
        ):
            error = ErrorValidacion(
                "El identificador de la reserva debe ser un texto no vacío."
            )

            registrar_error("Identificador de reserva inválido", error)
            raise error

        # Busca la reserva coincidente en la lista interna
        for reserva in self.__reservas:
            if reserva.id == identificador:
                registrar_evento(
                    f"Reserva consultada: {identificador}"
                )
                return reserva

        # Si no existe, registra el error y lanza ReservaNoEncontradaError
        error = ReservaNoEncontradaError(
            f"No existe una reserva con identificador {identificador}."
        )

        registrar_error("Reserva no encontrada", error)
        raise error

    # Retorna una copia superficial de la lista de reservas
    def listar_reservas(self):
        """
        Devuelve una copia de todas las reservas registradas.
        """

        registrar_evento(
            f"Consulta general de reservas: {len(self.__reservas)} registros"
        )

        return self.__reservas.copy()

    # Obtiene todas las reservas asociadas al documento de un cliente
    def buscar_por_cliente(self, documento_cliente):
        """
        Obtiene todas las reservas asociadas a un cliente.

        Args:
            documento_cliente (str): Documento del cliente.

        Returns:
            list: Reservas pertenecientes al cliente.
        """

        # Verifica primero que el cliente exista.
        self.__gestor_clientes.buscar_por_documento(documento_cliente)

        # Filtra las reservas que pertenecen al cliente indicado
        resultados = [
            reserva
            for reserva in self.__reservas
            if reserva.cliente.documento == documento_cliente
        ]

        registrar_evento(
            f"Consulta de reservas del cliente {documento_cliente}: "
            f"{len(resultados)} resultados"
        )

        return resultados

    # Filtra las reservas según su estado (pendiente, confirmada, cancelada, completada)
    def filtrar_por_estado(self, estado):
        """
        Filtra las reservas según su estado actual.

        Estados permitidos:
        pendiente, confirmada, cancelada y completada.
        """

        estados_validos = Reserva.ESTADOS_VALIDOS

        # Valida que el estado solicitado esté dentro de los permitidos
        if not isinstance(estado, str) or estado not in estados_validos:
            error = ErrorValidacion(
                f"Estado inválido. Estados permitidos: {estados_validos}."
            )

            registrar_error("Filtro de reservas con estado inválido", error)
            raise error

        # Recolecta las reservas con el estado solicitado
        resultados = [
            reserva
            for reserva in self.__reservas
            if reserva.estado == estado
        ]

        registrar_evento(
            f"Reservas filtradas por estado '{estado}': "
            f"{len(resultados)} resultados"
        )

        return resultados

    # Confirma una reserva pendiente, calcula su costo total y cambia su estado
    def confirmar_reserva(self, identificador, descuento=0, impuesto=0.19):
        """
        Confirma una reserva pendiente y calcula su costo.

        Args:
            identificador (str): Identificador de la reserva.
            descuento (float): Descuento aplicado, entre 0 y 1.
            impuesto (float): Impuesto aplicado, entre 0 y 1.

        Returns:
            float: Costo total de la reserva.
        """

        # Busca la reserva y verifica que esté en estado pendiente
        reserva = self.buscar_por_id(identificador)

        if reserva.estado != "pendiente":
            error = OperacionNoPermitidaError(
                "Solo se pueden confirmar reservas pendientes."
            )

            registrar_error("Confirmación de reserva no permitida", error)
            raise error

        # Verifica que el servicio siga disponible al momento de confirmar
        if not reserva.servicio.disponible:
            error = ServicioNoDisponibleError(
                f"El servicio '{reserva.servicio.nombre}' "
                "no está disponible para confirmar la reserva."
            )

            registrar_error("Servicio no disponible al confirmar", error)
            raise error

        # Si es alquiler de equipos, valida que aún haya unidades suficientes
        if isinstance(reserva.servicio, ServicioEquipo):
            if reserva.unidades > reserva.servicio.unidades_disponibles:
                error = CapacidadInsuficienteError(
                    "No hay suficientes unidades de equipo disponibles."
                )

                registrar_error("Unidades insuficientes al confirmar", error)
                raise error

        try:
            # Ejecuta la confirmación y calcula el costo total
            costo = reserva.confirmar(
                descuento=descuento,
                impuesto=impuesto
            )

            registrar_evento(
                f"Reserva confirmada: {identificador} | "
                f"Costo total: {costo}"
            )

            return costo

        except (TypeError, ValueError) as error:
            registrar_error(
                f"Error al confirmar la reserva {identificador}",
                error
            )

            raise OperacionNoPermitidaError(
                "No fue posible confirmar la reserva. "
                "Verifique sus parámetros y estado."
            ) from error

    # Cancela una reserva pendiente o confirmada
    def cancelar_reserva(self, identificador):
        """
        Cancela una reserva pendiente o confirmada.
        """

        reserva = self.buscar_por_id(identificador)

        try:
            # Cambia el estado de la reserva a cancelada si su estado actual lo permite
            reserva.cancelar()

            registrar_evento(
                f"Reserva cancelada: {identificador}"
            )

            return reserva

        except (TypeError, ValueError) as error:
            registrar_error(
                f"No fue posible cancelar la reserva {identificador}",
                error
            )

            raise OperacionNoPermitidaError(
                "La reserva no puede cancelarse en su estado actual."
            ) from error

    # Marca como completada una reserva que ya estaba confirmada
    def completar_reserva(self, identificador):
        """
        Marca como completada una reserva confirmada.
        """

        reserva = self.buscar_por_id(identificador)

        try:
            # Cambia el estado de la reserva a completada
            reserva.completar()

            registrar_evento(
                f"Reserva completada: {identificador}"
            )

            return reserva

        except (TypeError, ValueError) as error:
            registrar_error(
                f"No fue posible completar la reserva {identificador}",
                error
            )

            raise OperacionNoPermitidaError(
                "Solo se pueden completar reservas confirmadas."
            ) from error

    # Indica si existe una reserva registrada con el ID indicado
    def existe_reserva(self, identificador):
        """
        Comprueba si existe una reserva con el identificador indicado.
        """

        return any(
            reserva.id == identificador
            for reserva in self.__reservas
        )

    # Vacía todas las reservas almacenadas en memoria
    def limpiar_reservas(self):
        """
        Elimina todas las reservas de la lista interna.

        Se utiliza para pruebas y reinicio de sesiones.
        """

        cantidad = len(self.__reservas)
        self.__reservas.clear()

        registrar_evento(
            f"Lista de reservas reiniciada. "
            f"Registros eliminados: {cantidad}"
        )