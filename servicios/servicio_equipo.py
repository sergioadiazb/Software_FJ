# Importa isfinite para verificar que los valores numéricos sean finitos
from math import isfinite

# Importa la clase base Servicio de la que hereda ServicioEquipo
from modelos.servicio import Servicio


# Define la clase ServicioEquipo heredando de Servicio
class ServicioEquipo(Servicio):
    """
    Representa el servicio de alquiler de equipos tecnológicos
    de Software FJ.
    """

    # Constructor que inicializa los datos generales y específicos del alquiler de equipos
    def __init__(
        self,
        nombre,
        descripcion,
        precio_base,
        tipo_equipo,
        unidades_disponibles,
        estado,
        disponible=True
    ):
        """
        Inicializa un servicio de alquiler de equipos.

        Args:
            nombre (str): Nombre del equipo.
            descripcion (str): Descripción del equipo.
            precio_base (float): Precio de alquiler por hora y unidad.
            tipo_equipo (str): Categoría del equipo.
            unidades_disponibles (int): Cantidad disponible para alquiler.
            estado (str): Estado de conservación del equipo.
            disponible (bool): Disponibilidad del servicio.
        """

        # Llama al constructor de Servicio para inicializar atributos comunes y validar
        super().__init__(
            nombre,
            descripcion,
            precio_base,
            disponible
        )

        # Asigna los atributos propios del equipo usando sus setters
        self.tipo_equipo = tipo_equipo
        self.unidades_disponibles = unidades_disponibles
        self.estado = estado

        # Ejecuta la validación completa del servicio de equipo
        self.validar()

    # Propiedad getter para consultar el tipo de equipo
    @property
    def tipo_equipo(self):
        return self.__tipo_equipo

    # Setter que valida y guarda el tipo de equipo
    @tipo_equipo.setter
    def tipo_equipo(self, valor):
        # Exige que el tipo de equipo sea texto no vacío
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El tipo de equipo no puede estar vacío.")

        # Guarda el texto limpio de espacios sobrantes
        self.__tipo_equipo = valor.strip()

    # Propiedad getter para consultar las unidades disponibles
    @property
    def unidades_disponibles(self):
        return self.__unidades_disponibles

    # Setter que valida que las unidades disponibles sean un entero no negativo
    @unidades_disponibles.setter
    def unidades_disponibles(self, valor):
        # Rechaza booleanos y valores que no sean enteros
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise ValueError(
                "Las unidades disponibles deben ser un número entero."
            )

        # Impide cantidades negativas de equipos
        if valor < 0:
            raise ValueError(
                "Las unidades disponibles no pueden ser negativas."
            )

        # Guarda la cantidad de unidades disponibles
        self.__unidades_disponibles = valor

    # Propiedad getter para consultar el estado de conservación
    @property
    def estado(self):
        return self.__estado

    # Setter que valida que el estado sea nuevo, bueno o regular
    @estado.setter
    def estado(self, valor):
        if not isinstance(valor, str):
            raise ValueError("El estado debe ser un texto.")

        # Normaliza el texto quitando espacios y pasando a minúsculas
        valor = valor.strip().lower()

        # Define los únicos estados válidos para el equipo
        estados_validos = ("nuevo", "bueno", "regular")

        if valor not in estados_validos:
            raise ValueError(
                "El estado debe ser nuevo, bueno o regular."
            )

        # Guarda el estado validado
        self.__estado = valor

    # Valida tanto los atributos generales como los específicos del equipo
    def validar(self):
        """
        Valida los atributos generales y específicos del equipo.
        """

        # Valida los atributos heredados de Servicio
        super().validar()

        # Reaplica validaciones de los atributos propios del equipo
        self.tipo_equipo = self.__tipo_equipo
        self.unidades_disponibles = self.__unidades_disponibles
        self.estado = self.__estado

        return True

    # Valida disponibilidad, duración en horas y cantidad de unidades solicitadas
    def validar_parametros(self, cantidad=1, unidades=1):
        """
        Valida la duración del alquiler y la cantidad de equipos
        solicitados.

        Args:
            cantidad (float): Duración del alquiler en horas.
            unidades (int): Cantidad de equipos solicitados.
        """

        # Impide alquilar si el servicio está marcado como no disponible
        if not self.disponible:
            raise ValueError("El servicio de alquiler no está disponible.")

        # Comprueba que la duración sea un número válido y no booleano
        if (
            isinstance(cantidad, bool)
            or not isinstance(cantidad, (int, float))
        ):
            raise ValueError("La duración debe ser un valor numérico.")

        # Exige que la duración sea finita y mayor que cero
        if not isfinite(cantidad) or cantidad <= 0:
            raise ValueError("La duración debe ser mayor que cero.")

        # Comprueba que las unidades solicitadas sean un número entero válido
        if isinstance(unidades, bool) or not isinstance(unidades, int):
            raise ValueError("La cantidad de equipos debe ser un entero.")

        # Exige pedir al menos una unidad
        if unidades <= 0:
            raise ValueError("Debe solicitar al menos un equipo.")

        # Verifica que existan suficientes unidades disponibles
        if unidades > self.unidades_disponibles:
            raise ValueError(
                "No hay suficientes unidades disponibles para el alquiler."
            )

        return True

    # Calcula el costo total según horas, unidades, descuento e impuesto
    def calcular_costo(
        self,
        cantidad=1,
        descuento=0,
        impuesto=0.19,
        unidades=1
    ):
        """
        Calcula el costo del alquiler según las horas y unidades solicitadas.

        Args:
            cantidad (float): Duración del alquiler en horas.
            descuento (float): Descuento expresado entre 0 y 1.
            impuesto (float): Impuesto expresado entre 0 y 1.
            unidades (int): Cantidad de equipos solicitados.

        Returns:
            float: Costo total del alquiler.
        """

        # Valida disponibilidad, duración y unidades antes de calcular
        self.validar_parametros(cantidad, unidades)

        # Revisa que descuento e impuesto estén en el rango válido de 0 a 1
        for nombre, porcentaje in (
            ("Descuento", descuento),
            ("Impuesto", impuesto)
        ):
            if (
                isinstance(porcentaje, bool)
                or not isinstance(porcentaje, (int, float))
                or not isfinite(porcentaje)
                or not 0 <= porcentaje <= 1
            ):
                raise ValueError(
                    f"El {nombre.lower()} debe estar entre 0 y 1."
                )

        # Calcula el subtotal por horas y unidades, aplica descuento e impuesto
        subtotal = self.precio_base * cantidad * unidades
        valor_descuento = subtotal * descuento
        subtotal_con_descuento = subtotal - valor_descuento
        valor_impuesto = subtotal_con_descuento * impuesto

        return round(subtotal_con_descuento + valor_impuesto, 2)

    # Devuelve una ficha descriptiva completa del equipo
    def describir(self):
        """
        Genera una descripción detallada del equipo disponible.
        """

        return (
            f"Nombre: {self.nombre}\n"
            f"Descripción: {self.descripcion}\n"
            f"Tipo de equipo: {self.tipo_equipo}\n"
            f"Precio por hora y unidad: ${self.precio_base:,.2f}\n"
            f"Unidades disponibles: {self.unidades_disponibles}\n"
            f"Estado: {self.estado.capitalize()}\n"
            f"Disponible: {'Sí' if self.disponible else 'No'}"
        )