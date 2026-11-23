"""
Módulo encargado de administrar los servicios de Software FJ.

Permite registrar, consultar, buscar, filtrar, actualizar y eliminar
servicios de diferentes tipos mediante una lista interna.

Aplica polimorfismo al gestionar objetos que heredan de la clase
abstracta Servicio.
"""

# Importa la clase base abstracta Servicio para validar y filtrar tipos de servicio
from modelos.servicio import Servicio

# Importa las excepciones personalizadas para errores de validación o búsqueda
from utilidades.excepciones import (
    ErrorValidacion,
    ServicioNoEncontradoError
)

# Importa las funciones de registro para guardar eventos y errores en el log
from registros.registro_logs import (
    registrar_evento,
    registrar_error
)


# Define la clase encargada de gestionar la colección de servicios
class GestorServicios:
    """
    Administra los servicios ofrecidos por Software FJ.

    Almacena los servicios en una lista privada y permite gestionar
    diferentes clases derivadas de Servicio.
    """

    # Constructor que inicializa la lista interna vacía y registra el inicio
    def __init__(self):
        """Inicializa la lista interna de servicios."""
        self.__servicios = []

        # Registra en el log que el gestor de servicios está listo
        registrar_evento(
            "Gestor de servicios inicializado correctamente"
        )

    # Propiedad de solo lectura que devuelve cuántos servicios hay registrados
    @property
    def cantidad_servicios(self):
        """Devuelve la cantidad de servicios registrados."""
        return len(self.__servicios)

    # Registra un nuevo servicio tras comprobar herencia, validez y duplicados
    def registrar_servicio(self, servicio):
        """
        Registra un servicio en la lista interna.

        Args:
            servicio (Servicio): Objeto de una clase derivada de Servicio.

        Returns:
            Servicio: Servicio registrado.

        Raises:
            ErrorValidacion: Si el objeto no es válido o ya está registrado.
        """

        try:
            # Comprueba que el objeto herede de Servicio.
            if not isinstance(servicio, Servicio):
                raise ErrorValidacion(
                    "Solo se pueden registrar objetos derivados de Servicio."
                )

            # Ejecuta las validaciones propias del servicio.
            servicio.validar()

            # Comprueba que el identificador no esté registrado.
            if any(
                existente.id == servicio.id
                for existente in self.__servicios
            ):
                raise ErrorValidacion(
                    f"El servicio con identificador {servicio.id} "
                    "ya se encuentra registrado."
                )

            # Agrega el servicio a la lista.
            self.__servicios.append(servicio)

            # Registra el alta exitosa del servicio en el log
            registrar_evento(
                f"Servicio registrado: {servicio.nombre} | "
                f"Tipo: {type(servicio).__name__} | ID: {servicio.id}"
            )

            return servicio

        except ErrorValidacion as error:
            # Registra el error de validación y vuelve a lanzarlo
            registrar_error(
                "No fue posible registrar el servicio",
                error
            )
            raise

        except (TypeError, ValueError) as error:
            # Convierte errores de tipo o valor en ErrorValidacion
            registrar_error(
                "Error de validación durante el registro del servicio",
                error
            )

            raise ErrorValidacion(
                "El servicio contiene datos inválidos."
            ) from error

    # Busca un servicio por su identificador único
    def buscar_por_id(self, identificador):
        """
        Busca un servicio mediante su identificador único.

        Args:
            identificador (str): Identificador del servicio.

        Returns:
            Servicio: Objeto encontrado.

        Raises:
            ErrorValidacion: Si el identificador no es válido.
            ServicioNoEncontradoError: Si no existe el servicio.
        """

        # Valida que el identificador sea un texto no vacío
        if (
            not isinstance(identificador, str)
            or not identificador.strip()
        ):
            error = ErrorValidacion(
                "El identificador del servicio debe ser un texto no vacío."
            )

            registrar_error("Identificador de servicio inválido", error)
            raise error

        # Recorre los servicios registrados buscando coincidencia exacta por ID
        for servicio in self.__servicios:
            if servicio.id == identificador:
                registrar_evento(
                    f"Servicio consultado por ID: {identificador}"
                )
                return servicio

        # Si no se encuentra, registra el error y lanza ServicioNoEncontradoError
        error = ServicioNoEncontradoError(
            f"No existe un servicio con identificador {identificador}."
        )

        registrar_error("Servicio no encontrado", error)
        raise error

    # Busca servicios cuyo nombre contenga el texto indicado (sin distinguir mayúsculas)
    def buscar_por_nombre(self, nombre):
        """
        Busca servicios por su nombre.

        La búsqueda no distingue entre mayúsculas y minúsculas.

        Args:
            nombre (str): Nombre que se desea buscar.

        Returns:
            list: Servicios que coinciden con el nombre.

        Raises:
            ErrorValidacion: Si el nombre no es válido.
            ServicioNoEncontradoError: Si no hay coincidencias.
        """

        # Valida que el texto de búsqueda no esté vacío
        if not isinstance(nombre, str) or not nombre.strip():
            error = ErrorValidacion(
                "El nombre del servicio debe ser un texto no vacío."
            )

            registrar_error("Nombre de búsqueda inválido", error)
            raise error

        # Normaliza el texto de búsqueda para comparar sin distinguir mayúsculas/acentos
        nombre_busqueda = nombre.strip().casefold()

        resultados = [
            servicio
            for servicio in self.__servicios
            if nombre_busqueda in servicio.nombre.casefold()
        ]

        # Si no hubo coincidencias, lanza ServicioNoEncontradoError
        if not resultados:
            error = ServicioNoEncontradoError(
                f"No se encontraron servicios con el nombre '{nombre}'."
            )

            registrar_error("Búsqueda de servicio sin resultados", error)
            raise error

        registrar_evento(
            f"Búsqueda de servicios por nombre: {nombre}. "
            f"Coincidencias: {len(resultados)}"
        )

        return resultados

    # Retorna una copia superficial de la lista de servicios para protegerla
    def listar_servicios(self):
        """
        Devuelve una copia de todos los servicios registrados.

        Returns:
            list: Copia de la lista interna de servicios.
        """

        registrar_evento(
            f"Consulta general de servicios: {len(self.__servicios)} registros"
        )

        return self.__servicios.copy()

    # Filtra los servicios según una subclase concreta de Servicio (ej. ServicioSala)
    def filtrar_por_tipo(self, tipo_servicio):
        """
        Filtra los servicios según su clase concreta.

        Args:
            tipo_servicio (type): Clase del servicio que se desea consultar.

        Returns:
            list: Servicios que pertenecen al tipo solicitado.
        """

        # Verifica que el argumento sea una clase derivada de Servicio
        if (
            not isinstance(tipo_servicio, type)
            or not issubclass(tipo_servicio, Servicio)
        ):
            error = ErrorValidacion(
                "El tipo solicitado debe ser una clase derivada de Servicio."
            )

            registrar_error("Tipo de servicio inválido", error)
            raise error

        # Filtra los objetos que son instancia de la clase solicitada
        resultados = [
            servicio
            for servicio in self.__servicios
            if isinstance(servicio, tipo_servicio)
        ]

        registrar_evento(
            f"Filtro por tipo {tipo_servicio.__name__}: "
            f"{len(resultados)} resultados"
        )

        return resultados

    # Actualiza el estado de disponibilidad (True/False) de un servicio existente
    def cambiar_disponibilidad(self, identificador, disponible):
        """
        Modifica la disponibilidad de un servicio.

        Args:
            identificador (str): Identificador del servicio.
            disponible (bool): Nuevo estado de disponibilidad.

        Returns:
            Servicio: Servicio actualizado.
        """

        # Exige que disponible sea un valor booleano explícito
        if not isinstance(disponible, bool):
            error = ErrorValidacion(
                "La disponibilidad debe ser un valor booleano."
            )

            registrar_error("Estado de disponibilidad inválido", error)
            raise error

        # Busca el servicio y actualiza su propiedad disponible
        servicio = self.buscar_por_id(identificador)

        try:
            servicio.disponible = disponible

            registrar_evento(
                f"Disponibilidad modificada: {servicio.nombre} | "
                f"Disponible: {disponible}"
            )

            return servicio

        except (TypeError, ValueError) as error:
            registrar_error(
                "No fue posible cambiar la disponibilidad del servicio",
                error
            )

            raise ErrorValidacion(
                "No se pudo actualizar la disponibilidad."
            ) from error

    # Elimina un servicio de la lista interna a partir de su ID
    def eliminar_servicio(self, identificador):
        """
        Elimina un servicio mediante su identificador.

        Args:
            identificador (str): Identificador del servicio.

        Returns:
            Servicio: Objeto eliminado.
        """

        servicio = self.buscar_por_id(identificador)

        self.__servicios.remove(servicio)

        registrar_evento(
            f"Servicio eliminado: {servicio.nombre} | ID: {identificador}"
        )

        return servicio

    # Verifica si ya existe un servicio registrado con ese identificador
    def existe_servicio(self, identificador):
        """
        Comprueba si existe un servicio con el identificador indicado.

        Returns:
            bool: True si existe, False en caso contrario.
        """

        return any(
            servicio.id == identificador
            for servicio in self.__servicios
        )

    # Vacía todos los servicios guardados en memoria
    def limpiar_servicios(self):
        """
        Elimina todos los servicios de la lista interna.

        Se utiliza principalmente para pruebas o para reiniciar
        la información de una sesión.
        """

        cantidad = len(self.__servicios)
        self.__servicios.clear()

        registrar_evento(
            f"Lista de servicios reiniciada. "
            f"Registros eliminados: {cantidad}"
        )