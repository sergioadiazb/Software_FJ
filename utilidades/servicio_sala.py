# Importa isfinite para verificar que los valores numéricos sean finitos
from math import isfinite

# Importa la clase base Servicio de la que hereda ServicioSala
from modelos.servicio import Servicio


# Define la clase ServicioSala heredando de Servicio
class ServicioSala(Servicio):
    """
    Representa el servicio de alquiler de salas de Software FJ.

    Hereda de Servicio e incorpora características específicas
    como la capacidad y el equipamiento disponible.
    """

    # Constructor que inicializa los datos generales y específicos de la sala
    def __init__(
        self,
        nombre,
        descripcion,
        precio_base,
        capacidad,
        equipamiento,
        disponible=True
    ):
        """
        Inicializa una sala con sus características particulares.

        Args:
            nombre (str): Nombre de la sala.
            descripcion (str): Descripción de la sala.
            precio_base (float): Precio por hora de alquiler.
            capacidad (int): Número máximo de personas.
            equipamiento (list): Elementos disponibles en la sala.
            disponible (bool): Estado de disponibilidad.
        """

        # Llama al constructor de Servicio para inicializar atributos comunes y validar
        super().__init__(
            nombre,
            descripcion,
            precio_base,
            disponible
        )

        # Asigna los atributos propios de la sala usando sus setters
        self.capacidad = capacidad
        self.equipamiento = equipamiento

        # Ejecuta la validación completa de la sala
        self.validar()

    # Propiedad getter para consultar la capacidad máxima de personas
    @property
    def capacidad(self):
        return self.__capacidad

    # Setter que valida que la capacidad sea un entero mayor que cero
    @capacidad.setter
    def capacidad(self, valor):
        # Rechaza booleanos y valores que no sean números enteros
        if isinstance(valor, bool) or not isinstance(valor, int):
            raise ValueError("La capacidad debe ser un número entero.")

        # Exige que la capacidad sea positiva
        if valor <= 0:
            raise ValueError("La capacidad debe ser mayor que cero.")

        # Guarda la capacidad de la sala
        self.__capacidad = valor

    # Propiedad getter para consultar el equipamiento de la sala
    @property
    def equipamiento(self):
        return self.__equipamiento

    # Setter que valida el equipamiento y lo guarda como tupla de textos limpios
    @equipamiento.setter
    def equipamiento(self, valor):
        # Exige que el equipamiento venga en una lista o tupla
        if not isinstance(valor, (list, tuple)):
            raise ValueError("El equipamiento debe ser una lista o tupla.")

        # Comprueba que cada elemento sea una cadena de texto no vacía
        if not all(
            isinstance(elemento, str) and elemento.strip()
            for elemento in valor
        ):
            raise ValueError("Todos los elementos del equipamiento deben ser textos válidos.")

        # Convierte a tupla eliminando espacios sobrantes en cada elemento
        self.__equipamiento = tuple(
            elemento.strip() for elemento in valor
        )

    # Valida tanto los atributos generales como los específicos de la sala
    def validar(self):
        """
        Valida los atributos generales y específicos de la sala.
        """

        # Valida los atributos heredados de Servicio
        super().validar()

        # Reaplica validaciones de capacidad y equipamiento
        self.capacidad = self.__capacidad
        self.equipamiento = self.__equipamiento

        return True

    # Valida disponibilidad de la sala y duración en horas
    def validar_parametros(self, cantidad=1):
        """
        Comprueba que las horas de alquiler sean válidas
        y que la sala se encuentre disponible.
        """

        # Impide alquilar si la sala no está disponible
        if not self.disponible:
            raise ValueError("La sala no se encuentra disponible.")

        # Verifica que la duración sea numérica y no booleana
        if isinstance(cantidad, bool) or not isinstance(cantidad, (int, float)):
            raise ValueError("La duración debe ser un valor numérico.")

        # Verifica que la duración sea finita y mayor que cero
        if not isfinite(cantidad) or cantidad <= 0:
            raise ValueError("La duración debe ser mayor que cero.")

        return True

    # Calcula el costo total del alquiler según horas, descuento e impuesto
    def calcular_costo(self, cantidad=1, descuento=0, impuesto=0.19):
        """
        Calcula el costo del alquiler según las horas contratadas.

        Args:
            cantidad (float): Cantidad de horas de alquiler.
            descuento (float): Descuento expresado entre 0 y 1.
            impuesto (float): Impuesto expresado entre 0 y 1.

        Returns:
            float: Costo total del alquiler.
        """

        # Valida disponibilidad y duración antes de calcular el costo
        self.validar_parametros(cantidad)

        # Comprueba que descuento e impuesto estén entre 0 y 1
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

        # Calcula subtotal, resta el descuento y suma el impuesto redondeado a 2 decimales
        subtotal = self.precio_base * cantidad
        valor_descuento = subtotal * descuento
        subtotal_con_descuento = subtotal - valor_descuento
        valor_impuesto = subtotal_con_descuento * impuesto

        return round(subtotal_con_descuento + valor_impuesto, 2)

    # Devuelve una descripción detallada de la sala
    def describir(self):
        """
        Genera una descripción detallada de la sala.
        """

        # Une los elementos del equipamiento separados por coma
        elementos = ", ".join(self.equipamiento)

        return (
            f"Nombre: {self.nombre}\n"
            f"Descripción: {self.descripcion}\n"
            f"Capacidad: {self.capacidad} personas\n"
            f"Precio por hora: ${self.precio_base:,.2f}\n"
            f"Equipamiento: {elementos or 'Sin equipamiento adicional'}\n"
            f"Disponible: {'Sí' if self.disponible else 'No'}"
        )