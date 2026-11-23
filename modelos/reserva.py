# Importa isfinite para comprobar que los números no sean infinitos ni NaN
from math import isfinite

# Importa la clase base Entidad y los modelos Cliente y Servicio
from modelos.entidad import Entidad
from modelos.cliente import Cliente
from modelos.servicio import Servicio
# Importa ServicioEquipo para revisar si la reserva corresponde al alquiler de equipos
from servicios.servicio_equipo import ServicioEquipo


# Define la clase Reserva heredando de Entidad
class Reserva(Entidad):
    """
    Representa una reserva realizada por un cliente
    para utilizar alguno de los servicios de Software FJ.
    """

    # Tupla con los únicos estados permitidos para una reserva
    ESTADOS_VALIDOS = (
        "pendiente",
        "confirmada",
        "cancelada",
        "completada"
    )

    # Constructor que inicializa una reserva con cliente, servicio, duración y unidades
    def __init__(self, cliente, servicio, duracion, unidades=1):
        """
        Inicializa una reserva.

        Args:
            cliente (Cliente): Cliente que realiza la reserva.
            servicio (Servicio): Servicio solicitado.
            duracion (float): Duración en horas.
            unidades (int): Cantidad de equipos solicitados.
        """

        # Llama al constructor de Entidad para asignar el ID único de la reserva
        super().__init__()

        # Asigna los valores usando los setters para que se validen desde el inicio
        self.cliente = cliente
        self.servicio = servicio
        self.duracion = duracion
        self.unidades = unidades

        # Inicializa el estado en pendiente y el costo total en cero
        self.__estado = "pendiente"
        self.__costo_total = 0.0

        # Ejecuta la validación general de la reserva
        self.validar()

    # --------------------------------------------------
    # PROPIEDADES Y ENCAPSULACIÓN
    # --------------------------------------------------

    @property
    def cliente(self):
        # Retorna el cliente asociado a la reserva
        return self.__cliente

    @cliente.setter
    def cliente(self, valor):
        # Comprueba que el valor sea una instancia válida de Cliente
        if not isinstance(valor, Cliente):
            raise ValueError(
                "La reserva debe estar asociada a un cliente válido."
            )

        # Guarda el cliente en el atributo privado
        self.__cliente = valor

    @property
    def servicio(self):
        # Retorna el servicio asociado a la reserva
        return self.__servicio

    @servicio.setter
    def servicio(self, valor):
        # Comprueba que el valor sea una instancia válida de Servicio
        if not isinstance(valor, Servicio):
            raise ValueError(
                "La reserva debe estar asociada a un servicio válido."
            )

        # Guarda el servicio en el atributo privado
        self.__servicio = valor

    @property
    def duracion(self):
        # Retorna la duración de la reserva en horas
        return self.__duracion

    @duracion.setter
    def duracion(self, valor):
        # Rechaza valores booleanos o que no sean int/float
        if (
            isinstance(valor, bool)
            or not isinstance(valor, (int, float))
        ):
            raise ValueError(
                "La duración debe ser un valor numérico."
            )

        # Comprueba que la duración sea finita y mayor que cero
        if not isfinite(valor) or valor <= 0:
            raise ValueError(
                "La duración debe ser mayor que cero y finita."
            )

        # Guarda la duración convertida a flotante
        self.__duracion = float(valor)

    @property
    def unidades(self):
        # Retorna la cantidad de unidades reservadas
        return self.__unidades

    @unidades.setter
    def unidades(self, valor):
        # Rechaza booleanos y valores que no sean números enteros
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise ValueError(
                "Las unidades deben ser un número entero."
            )

        # Exige que se solicite al menos una unidad
        if valor <= 0:
            raise ValueError(
                "Debe solicitar al menos una unidad."
            )

        # Guarda la cantidad de unidades
        self.__unidades = valor

    @property
    def estado(self):
        # Retorna el estado actual de la reserva (solo lectura directa)
        return self.__estado

    @property
    def costo_total(self):
        # Retorna el costo total calculado de la reserva (solo lectura directa)
        return self.__costo_total

    # --------------------------------------------------
    # VALIDACIONES
    # --------------------------------------------------

    def validar(self):
        """
        Valida los datos generales de la reserva.
        """

        # Verifica nuevamente que cliente y servicio sean objetos válidos
        if not isinstance(self.__cliente, Cliente):
            raise ValueError("El cliente de la reserva no es válido.")

        if not isinstance(self.__servicio, Servicio):
            raise ValueError("El servicio de la reserva no es válido.")

        # Reaplica validaciones de cada propiedad
        self.cliente = self.__cliente
        self.servicio = self.__servicio
        self.duracion = self.__duracion
        self.unidades = self.__unidades

        # Evita pedir más de 1 unidad si el servicio no es alquiler de equipos
        if (
            not isinstance(self.servicio, ServicioEquipo)
            and self.unidades != 1
        ):
            raise ValueError(
                "Solo se pueden solicitar varias unidades "
                "en el servicio de alquiler de equipos."
            )

        # Retorna True si toda la validación fue exitosa
        return True

    # --------------------------------------------------
    # CÁLCULO DE COSTOS
    # --------------------------------------------------

    def calcular_total(self, descuento=0, impuesto=0.19):
        """
        Calcula el costo total de la reserva según el servicio.

        Args:
            descuento (float): Descuento expresado entre 0 y 1.
            impuesto (float): Impuesto expresado entre 0 y 1.

        Returns:
            float: Costo total de la reserva.
        """

        # Valida que el descuento sea un número finito entre 0 y 1
        if (
            isinstance(descuento, bool)
            or not isinstance(descuento, (int, float))
            or not isfinite(descuento)
            or not 0 <= descuento <= 1
        ):
            raise ValueError(
                "El descuento debe estar entre 0 y 1."
            )

        # Valida que el impuesto sea un número finito entre 0 y 1
        if (
            isinstance(impuesto, bool)
            or not isinstance(impuesto, (int, float))
            or not isfinite(impuesto)
            or not 0 <= impuesto <= 1
        ):
            raise ValueError(
                "El impuesto debe estar entre 0 y 1."
            )

        # Si el servicio es alquiler de equipos, incluye las unidades en el cálculo
        if isinstance(self.servicio, ServicioEquipo):
            return self.servicio.calcular_costo(
                cantidad=self.duracion,
                descuento=descuento,
                impuesto=impuesto,
                unidades=self.unidades
            )

        # Para otros servicios, calcula el costo según la duración
        return self.servicio.calcular_costo(
            cantidad=self.duracion,
            descuento=descuento,
            impuesto=impuesto
        )

    # --------------------------------------------------
    # CONFIRMACIÓN Y PROCESAMIENTO
    # --------------------------------------------------

    def procesar(self, descuento=0, impuesto=0.19):
        """
        Procesa una reserva pendiente, calcula su costo
        y cambia su estado a confirmada.
        """

        # Solo permite procesar reservas que estén en estado pendiente
        if self.estado != "pendiente":
            raise ValueError(
                "Solo se pueden procesar reservas pendientes."
            )

        # Valida la disponibilidad y los parámetros del servicio según su tipo
        self.servicio.validar_parametros(self.duracion) if (
            not isinstance(self.servicio, ServicioEquipo)
        ) else self.servicio.validar_parametros(
            self.duracion, self.unidades
        )

        # Calcula el costo total y verifica que sea un valor válido y positivo
        costo = self.calcular_total(descuento, impuesto)

        if not isfinite(costo) or costo <= 0:
            raise ValueError(
                "El costo calculado de la reserva no es válido."
            )

        # Guarda el costo final y cambia el estado de la reserva a confirmada
        self.__costo_total = costo
        self.__estado = "confirmada"

        return self.__costo_total

    def confirmar(self, descuento=0, impuesto=0.19):
        """
        Confirma una reserva mediante su procesamiento.
        """

        # Delega la confirmación al método procesar
        return self.procesar(descuento, impuesto)

    # --------------------------------------------------
    # CANCELACIÓN Y FINALIZACIÓN
    # --------------------------------------------------

    def cancelar(self):
        """
        Cancela una reserva pendiente o confirmada.
        """

        # Impide cancelar reservas ya canceladas o completadas
        if self.estado not in ("pendiente", "confirmada"):
            raise ValueError(
                "No se puede cancelar una reserva "
                "que ya está cancelada o completada."
            )

        # Cambia el estado de la reserva a cancelada
        self.__estado = "cancelada"

        return True

    def completar(self):
        """
        Marca como completada una reserva confirmada.
        """

        # Solo permite completar reservas previamente confirmadas
        if self.estado != "confirmada":
            raise ValueError(
                "Solo se pueden completar reservas confirmadas."
            )

        # Cambia el estado de la reserva a completada
        self.__estado = "completada"

        return True

    # --------------------------------------------------
    # REPRESENTACIÓN DEL OBJETO
    # --------------------------------------------------

    def __str__(self):
        """
        Devuelve una representación legible de la reserva.
        """

        # Retorna un texto formateado con el resumen de la reserva
        return (
            f"Reserva: {self.id}\n"
            f"Cliente: {self.cliente.nombre}\n"
            f"Servicio: {self.servicio.nombre}\n"
            f"Duración: {self.duracion} horas\n"
            f"Unidades: {self.unidades}\n"
            f"Estado: {self.estado.capitalize()}\n"
            f"Costo total: ${self.costo_total:,.2f}"
        )