# Importa isfinite para verificar que los valores numéricos sean finitos
from math import isfinite

# Importa la clase base Servicio de la que hereda ServicioAsesoria
from modelos.servicio import Servicio


# Define la clase ServicioAsesoria heredando de Servicio
class ServicioAsesoria(Servicio):
    """
    Representa el servicio de asesorías especializadas
    ofrecido por la empresa Software FJ.

    Hereda de Servicio e incorpora características como
    la especialidad, el profesional y la modalidad.
    """

    # Constructor que inicializa los datos generales y específicos de la asesoría
    def __init__(
        self,
        nombre,
        descripcion,
        precio_base,
        especialidad,
        profesional,
        modalidad,
        disponible=True
    ):
        """
        Inicializa un servicio de asesoría.

        Args:
            nombre (str): Nombre de la asesoría.
            descripcion (str): Descripción del servicio.
            precio_base (float): Precio por hora de asesoría.
            especialidad (str): Área de conocimiento.
            profesional (str): Profesional encargado.
            modalidad (str): Modalidad virtual o presencial.
            disponible (bool): Estado de disponibilidad.
        """

        # Llama al constructor de Servicio para inicializar atributos comunes y validar
        super().__init__(
            nombre,
            descripcion,
            precio_base,
            disponible
        )

        # Asigna los atributos propios de la asesoría usando sus setters
        self.especialidad = especialidad
        self.profesional = profesional
        self.modalidad = modalidad

        # Ejecuta la validación completa del servicio de asesoría
        self.validar()

    # Propiedad getter para consultar la especialidad
    @property
    def especialidad(self):
        return self.__especialidad

    # Setter que valida y guarda la especialidad
    @especialidad.setter
    def especialidad(self, valor):
        # Exige que la especialidad sea texto no vacío
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError(
                "La especialidad no puede estar vacía."
            )

        # Guarda el valor limpio de espacios sobrantes
        self.__especialidad = valor.strip()

    # Propiedad getter para consultar el profesional encargado
    @property
    def profesional(self):
        return self.__profesional

    # Setter que valida y guarda el nombre del profesional
    @profesional.setter
    def profesional(self, valor):
        # Exige que el nombre del profesional sea texto no vacío
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError(
                "El nombre del profesional no puede estar vacío."
            )

        # Guarda el nombre limpio de espacios extremos
        self.__profesional = valor.strip()

    # Propiedad getter para consultar la modalidad
    @property
    def modalidad(self):
        return self.__modalidad

    # Setter que valida que la modalidad sea virtual o presencial
    @modalidad.setter
    def modalidad(self, valor):
        if not isinstance(valor, str):
            raise ValueError(
                "La modalidad debe ser un texto."
            )

        # Normaliza el texto quitando espacios y pasando a minúsculas
        valor = valor.strip().lower()

        # Define las únicas modalidades aceptadas
        modalidades_validas = ("virtual", "presencial")

        if valor not in modalidades_validas:
            raise ValueError(
                "La modalidad debe ser virtual o presencial."
            )

        # Guarda la modalidad válida
        self.__modalidad = valor

    # Valida tanto los atributos heredados como los propios de la asesoría
    def validar(self):
        """
        Valida los atributos generales y específicos
        del servicio de asesoría.
        """

        # Valida los atributos generales de Servicio
        super().validar()

        # Reaplica validaciones de los atributos específicos
        self.especialidad = self.__especialidad
        self.profesional = self.__profesional
        self.modalidad = self.__modalidad

        return True

    # Valida disponibilidad y duración de la asesoría antes de reservar o cobrar
    def validar_parametros(self, cantidad=1):
        """
        Valida la duración de la asesoría y la disponibilidad.

        Args:
            cantidad (float): Duración de la asesoría en horas.
        """

        # Impide usar el servicio si no está disponible
        if not self.disponible:
            raise ValueError(
                "El servicio de asesoría no está disponible."
            )

        # Verifica que la duración sea numérica y no booleana
        if (
            isinstance(cantidad, bool)
            or not isinstance(cantidad, (int, float))
        ):
            raise ValueError(
                "La duración debe ser un valor numérico."
            )

        # Verifica que la duración sea finita y mayor que cero
        if not isfinite(cantidad) or cantidad <= 0:
            raise ValueError(
                "La duración debe ser mayor que cero."
            )

        return True

    # Calcula el costo total aplicando duración, descuento e impuesto
    def calcular_costo(
        self,
        cantidad=1,
        descuento=0,
        impuesto=0.19
    ):
        """
        Calcula el costo de la asesoría según su duración.

        Args:
            cantidad (float): Duración en horas.
            descuento (float): Descuento expresado entre 0 y 1.
            impuesto (float): Impuesto expresado entre 0 y 1.

        Returns:
            float: Costo total de la asesoría.
        """

        # Primero valida disponibilidad y duración en horas
        self.validar_parametros(cantidad)

        # Revisa que tanto el descuento como el impuesto estén entre 0 y 1
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

        return round(
            subtotal_con_descuento + valor_impuesto,
            2
        )

    # Devuelve una ficha descriptiva completa de la asesoría
    def describir(self):
        """
        Genera una descripción detallada del servicio
        de asesoría.
        """

        return (
            f"Nombre: {self.nombre}\n"
            f"Descripción: {self.descripcion}\n"
            f"Especialidad: {self.especialidad}\n"
            f"Profesional: {self.profesional}\n"
            f"Modalidad: {self.modalidad.capitalize()}\n"
            f"Precio por hora: ${self.precio_base:,.2f}\n"
            f"Disponible: {'Sí' if self.disponible else 'No'}"
        )