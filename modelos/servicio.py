# Importa abstractmethod para declarar métodos que deben implementar las clases hijas
from abc import abstractmethod
# Importa isfinite para asegurar que los valores numéricos sean finitos
from math import isfinite

# Importa la clase base abstracta Entidad
from modelos.entidad import Entidad


# Define la clase abstracta Servicio heredando de Entidad
class Servicio(Entidad):
    """
    Clase abstracta que representa los servicios ofrecidos
    por la empresa Software FJ.
    """

    # Constructor que inicializa los atributos comunes de cualquier servicio
    def __init__(self, nombre, descripcion, precio_base, disponible=True):
        """
        Inicializa los atributos generales de un servicio.

        Args:
            nombre (str): Nombre del servicio.
            descripcion (str): Descripción del servicio.
            precio_base (float): Precio inicial del servicio.
            disponible (bool): Estado de disponibilidad.
        """
        # Llama al constructor de Entidad para asignar el identificador único
        super().__init__()

        # Asigna los atributos usando los setters para validar los datos desde el inicio
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio_base = precio_base
        self.disponible = disponible

    # Propiedad getter para consultar el nombre del servicio
    @property
    def nombre(self):
        return self.__nombre

    # Setter que valida y guarda el nombre del servicio
    @nombre.setter
    def nombre(self, valor):
        # Exige que el nombre sea texto no vacío
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("El nombre del servicio no puede estar vacío.")

        # Guarda el nombre sin espacios sobrantes a los lados
        self.__nombre = valor.strip()

    # Propiedad getter para consultar la descripción del servicio
    @property
    def descripcion(self):
        return self.__descripcion

    # Setter que valida y guarda la descripción del servicio
    @descripcion.setter
    def descripcion(self, valor):
        # Exige que la descripción sea una cadena de texto no vacía
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("La descripción del servicio no puede estar vacía.")

        # Guarda la descripción limpia de espacios extremos
        self.__descripcion = valor.strip()

    # Propiedad getter para consultar el precio base
    @property
    def precio_base(self):
        return self.__precio_base

    # Setter que valida que el precio base sea un número positivo finito
    @precio_base.setter
    def precio_base(self, valor):
        # Rechaza booleanos y valores que no sean numéricos
        if isinstance(valor, bool) or not isinstance(valor, (int, float)):
            raise ValueError("El precio base debe ser un valor numérico.")

        # Comprueba que el precio sea finito y mayor que cero
        if not isfinite(valor) or valor <= 0:
            raise ValueError("El precio base debe ser mayor que cero y finito.")

        # Guarda el precio convertido a número flotante
        self.__precio_base = float(valor)

    # Propiedad getter para consultar si el servicio está disponible
    @property
    def disponible(self):
        return self.__disponible

    # Setter que valida que la disponibilidad sea booleana (True o False)
    @disponible.setter
    def disponible(self, valor):
        if not isinstance(valor, bool):
            raise ValueError("La disponibilidad debe ser verdadera o falsa.")

        # Guarda el estado de disponibilidad
        self.__disponible = valor

    # Valida todos los atributos generales del servicio
    def validar(self):
        """
        Valida los atributos generales del servicio.
        """
        # Reasigna cada propiedad para disparar sus validaciones
        self.nombre = self.__nombre
        self.descripcion = self.__descripcion
        self.precio_base = self.__precio_base
        self.disponible = self.__disponible

        return True

    # Método abstracto que cada servicio especializado definirá a su manera
    @abstractmethod
    def calcular_costo(self, cantidad=1, descuento=0, impuesto=0.19):
        """
        Calcula el costo del servicio según sus características.
        Cada servicio especializado implementará su propio cálculo.
        """
        pass

    # Método abstracto para devolver la descripción detallada de cada servicio
    @abstractmethod
    def describir(self):
        """
        Devuelve una descripción detallada del servicio.
        """
        pass

    # Método abstracto para validar parámetros específicos de cada tipo de servicio
    @abstractmethod
    def validar_parametros(self, cantidad=1):
        """
        Valida los parámetros particulares de cada servicio.
        """
        pass

    # Representación legible en texto del servicio
    def __str__(self):
        return (
            f"Servicio: {self.nombre}\n"
            f"Descripción: {self.descripcion}\n"
            f"Precio base: ${self.precio_base:,.2f}\n"
            f"Disponible: {'Sí' if self.disponible else 'No'}"
        )