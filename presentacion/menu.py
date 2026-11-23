# Importa la clase Cliente para crear objetos de clientes en el menú
from modelos.cliente import Cliente
# Importa los tres tipos de servicios heredados para registrarlos según la elección del usuario
from servicios.servicio_sala import ServicioSala
from servicios.servicio_equipo import ServicioEquipo
from servicios.servicio_asesoria import ServicioAsesoria

# Importa los controladores encargados de administrar clientes, servicios y reservas en memoria
from controladores.gestor_clientes import GestorClientes
from controladores.gestor_servicios import GestorServicios
from controladores.gestor_reservas import GestorReservas

# Importa las funciones para guardar eventos normales y errores en el archivo de logs
from registros.registro_logs import registrar_evento, registrar_error


def leer_texto(mensaje):
    """Solicita un texto obligatorio y evita que quede vacío."""
    # Repite hasta que el usuario escriba un texto válido
    while True:
        # Lee lo que escribe el usuario y quita espacios sobrantes en los extremos
        valor = input(mensaje).strip()

        # Si el texto no está vacío, lo devuelve
        if valor:
            return valor

        # Avisa que el dato es obligatorio si quedó vacío
        print("El campo no puede estar vacío.")


def leer_entero(mensaje, minimo=1):
    """Solicita un número entero dentro del rango permitido."""
    # Repite hasta obtener un número entero válido
    while True:
        try:
            # Convierte el texto ingresado a número entero
            valor = int(input(mensaje))

            # Verifica que no sea menor que el valor mínimo permitido
            if valor < minimo:
                print(f"El valor debe ser igual o superior a {minimo}.")
                continue

            # Devuelve el entero válido
            return valor

        except ValueError:
            # Si escribió letras o símbolos no válidos, muestra mensaje y vuelve a pedirlo
            print("Ingresa un número entero válido.")


def leer_decimal(mensaje, minimo=0):
    """Solicita un número decimal válido igual o mayor al mínimo."""
    # Repite hasta obtener un número decimal válido
    while True:
        try:
            # Cambia coma por punto y convierte el texto a número flotante
            valor = float(input(mensaje).replace(",", "."))

            # Revisa que el número cumpla con el mínimo exigido
            if valor < minimo:
                print(f"El valor debe ser igual o superior a {minimo}.")
                continue

            # Devuelve el decimal válido
            return valor

        except ValueError:
            # Si no se puede convertir a decimal, avisa al usuario
            print("Ingresa un número válido.")


def leer_opcion(mensaje, opciones):
    """Solicita una opción que esté dentro de la lista de opciones válidas."""
    # Repite hasta que el usuario elija una opción permitida
    while True:
        # Lee la opción y elimina espacios al inicio o final
        opcion = input(mensaje).strip()

        # Comprueba si la opción está en la lista válida
        if opcion in opciones:
            return opcion

        # Informa si la opción no es válida
        print("Opción no válida.")


class MenuSoftwareFJ:
    """Interfaz de consola para administrar Software FJ."""

    def __init__(self):
        # Inicializa el gestor de clientes
        self.gestor_clientes = GestorClientes()
        # Inicializa el gestor de servicios
        self.gestor_servicios = GestorServicios()

        # Inicializa el gestor de reservas pasándole los gestores de clientes y servicios
        self.gestor_reservas = GestorReservas(
            self.gestor_clientes,
            self.gestor_servicios
        )

    def mostrar_menu_principal(self):
        # Imprime en consola las opciones principales del sistema
        print("\n========================================")
        print("       SOFTWARE FJ")
        print(" Sistema Integral de Gestión")
        print("========================================")
        print("1. Gestión de clientes")
        print("2. Gestión de servicios")
        print("3. Gestión de reservas")
        print("4. Consultar resumen del sistema")
        print("0. Salir")
        print("========================================")

    def ejecutar(self):
        # Registra en el log que el sistema arrancó
        registrar_evento("Inicio de Software FJ")

        # Bucle principal que mantiene vivo el menú hasta elegir salir
        while True:
            try:
                # Muestra el menú principal y lee la opción del usuario
                self.mostrar_menu_principal()
                opcion = input("Selecciona una opción: ").strip()

                # Abre el submenú de clientes
                if opcion == "1":
                    self.menu_clientes()

                # Abre el submenú de servicios
                elif opcion == "2":
                    self.menu_servicios()

                # Abre el submenú de reservas
                elif opcion == "3":
                    self.menu_reservas()

                # Muestra el resumen de cantidades registradas
                elif opcion == "4":
                    self.mostrar_resumen()

                # Cierra el programa de forma limpia y registra el cierre en el log
                elif opcion == "0":
                    print("\nGracias por utilizar Software FJ.")
                    registrar_evento("Cierre de Software FJ")
                    break

                # Si escribió otro número o texto, avisa sin detener el sistema
                else:
                    print("Selecciona una opción válida.")

            except KeyboardInterrupt:
                # Captura Ctrl+C para cerrar sin error feo y registra la interrupción
                print("\nOperación interrumpida por el usuario.")
                registrar_evento("Interrupción manual del sistema")
                break

            except Exception as error:
                # Registra cualquier error inesperado en logs pero mantiene el sistema activo
                registrar_error("Error no controlado en el menú principal", error)
                print(f"Se produjo un error: {error}")
                print("El sistema continuará funcionando.")

    # ==========================================
    # GESTIÓN DE CLIENTES
    # ==========================================

    def menu_clientes(self):
        # Bucle del submenú para administrar clientes
        while True:
            print("\n----------- CLIENTES -----------")
            print("1. Registrar cliente")
            print("2. Buscar cliente por documento")
            print("3. Listar clientes")
            print("4. Eliminar cliente")
            print("0. Volver")

            opcion = input("Selecciona una opción: ").strip()

            try:
                if opcion == "1":
                    # Llama al método para crear y guardar un cliente
                    self.registrar_cliente()

                elif opcion == "2":
                    # Llama al método para buscar un cliente por documento
                    self.buscar_cliente()

                elif opcion == "3":
                    # Llama al método para mostrar todos los clientes
                    self.listar_clientes()

                elif opcion == "4":
                    # Llama al método para eliminar un cliente
                    self.eliminar_cliente()

                elif opcion == "0":
                    # Sale del submenú de clientes y vuelve al menú principal
                    break

                else:
                    print("Opción no válida.")

            except Exception as error:
                # Registra el error de clientes y muestra un mensaje controlado
                registrar_error("Error en el módulo de clientes", error)
                print(f"No se pudo completar la operación: {error}")

    def registrar_cliente(self):
        # Pide los datos básicos del cliente y lo registra en el gestor
        print("\nREGISTRO DE CLIENTE")

        nombre = leer_texto("Nombre completo: ")
        documento = leer_texto("Documento: ")
        correo = leer_texto("Correo electrónico: ")
        telefono = leer_texto("Teléfono: ")

        # Crea el objeto Cliente con los datos ingresados
        cliente = Cliente(nombre, documento, correo, telefono)

        # Guarda el cliente a través del gestor
        self.gestor_clientes.registrar_cliente(cliente)

        print("Cliente registrado correctamente.")

    def buscar_cliente(self):
        # Busca un cliente por documento y muestra sus datos en pantalla
        documento = leer_texto("Documento del cliente: ")

        cliente = self.gestor_clientes.buscar_por_documento(documento)

        print("\nCLIENTE ENCONTRADO")
        print(f"Nombre: {cliente.nombre}")
        print(f"Documento: {cliente.documento}")
        print(f"Correo: {cliente.correo}")
        print(f"Teléfono: {cliente.telefono}")
        print(f"ID: {cliente.id}")

    def listar_clientes(self):
        # Obtiene la lista de clientes registrados
        clientes = self.gestor_clientes.listar_clientes()

        # Si la lista está vacía, informa y termina el método
        if not clientes:
            print("No hay clientes registrados.")
            return

        print("\nLISTADO DE CLIENTES")

        # Recorre cada cliente y muestra sus datos principales
        for cliente in clientes:
            print(
                f"Nombre: {cliente.nombre} | "
                f"Documento: {cliente.documento} | "
                f"ID: {cliente.id}"
            )

    def eliminar_cliente(self):
        # Busca el cliente a eliminar, pide confirmación y lo borra si acepta
        documento = leer_texto("Documento del cliente que deseas eliminar: ")

        cliente = self.gestor_clientes.buscar_por_documento(documento)

        confirmacion = leer_opcion(
            f"¿Eliminar a {cliente.nombre}? (s/n): ",
            ["s", "n"]
        )

        if confirmacion == "s":
            self.gestor_clientes.eliminar_cliente(documento)
            print("Cliente eliminado correctamente.")
        else:
            print("Operación cancelada.")

    # ==========================================
    # GESTIÓN DE SERVICIOS
    # ==========================================

    def menu_servicios(self):
        # Bucle del submenú para administrar servicios
        while True:
            print("\n----------- SERVICIOS -----------")
            print("1. Registrar servicio")
            print("2. Listar servicios")
            print("3. Consultar servicio por ID")
            print("4. Cambiar disponibilidad")
            print("5. Eliminar servicio")
            print("0. Volver")

            opcion = input("Selecciona una opción: ").strip()

            try:
                if opcion == "1":
                    self.registrar_servicio()

                elif opcion == "2":
                    self.listar_servicios()

                elif opcion == "3":
                    self.buscar_servicio()

                elif opcion == "4":
                    self.cambiar_disponibilidad()

                elif opcion == "5":
                    self.eliminar_servicio()

                elif opcion == "0":
                    break

                else:
                    print("Opción no válida.")

            except Exception as error:
                # Registra el error en el módulo de servicios sin detener el menú
                registrar_error("Error en el módulo de servicios", error)
                print(f"No se pudo completar la operación: {error}")

    def registrar_servicio(self):
        # Permite elegir entre sala, equipo o asesoría y crea el objeto correspondiente
        print("\nTIPOS DE SERVICIO")
        print("1. Servicio de sala")
        print("2. Alquiler de equipo")
        print("3. Asesoría especializada")

        tipo = leer_opcion("Selecciona el tipo: ", ["1", "2", "3"])

        nombre = leer_texto("Nombre del servicio: ")
        descripcion = leer_texto("Descripción: ")
        precio = leer_decimal("Precio base: ", 0)

        if tipo == "1":
            # Datos propios de una reserva de sala
            capacidad = leer_entero("Capacidad de personas: ")
            equipamiento = leer_texto("Equipamiento disponible: ")

            servicio = ServicioSala(
                nombre,
                descripcion,
                precio,
                capacidad,
                equipamiento
            )

        elif tipo == "2":
            # Datos propios del alquiler de equipo
            tipo_equipo = leer_texto("Tipo de equipo: ")
            unidades = leer_entero("Unidades disponibles: ")
            estado = leer_texto("Estado del equipo: ")

            servicio = ServicioEquipo(
                nombre,
                descripcion,
                precio,
                tipo_equipo,
                unidades,
                estado
            )

        else:
            # Datos propios de una asesoría especializada
            especialidad = leer_texto("Especialidad: ")
            profesional = leer_texto("Profesional responsable: ")
            modalidad = leer_texto("Modalidad: ")

            servicio = ServicioAsesoria(
                nombre,
                descripcion,
                precio,
                especialidad,
                profesional,
                modalidad
            )

        # Registra el servicio creado en el gestor
        self.gestor_servicios.registrar_servicio(servicio)

        print("\nServicio registrado correctamente.")
        print(f"Identificador: {servicio.id}")

    def listar_servicios(self):
        # Obtiene todos los servicios registrados y muestra sus datos
        servicios = self.gestor_servicios.listar_servicios()

        if not servicios:
            print("No hay servicios registrados.")
            return

        print("\nLISTADO DE SERVICIOS")

        for servicio in servicios:
            print("----------------------------------------")
            print(f"Nombre: {servicio.nombre}")
            print(f"Descripción: {servicio.descripcion}")
            print(f"Precio base: {servicio.precio_base}")
            print(f"Disponible: {servicio.disponible}")
            print(f"Tipo: {servicio.__class__.__name__}")
            print(f"ID: {servicio.id}")

    def buscar_servicio(self):
        # Busca un servicio por su ID y muestra su descripción y estado
        identificador = leer_texto("ID del servicio: ")

        servicio = self.gestor_servicios.buscar_por_id(identificador)

        print("\nSERVICIO ENCONTRADO")
        print(servicio.describir())
        print(f"Precio base: {servicio.precio_base}")
        print(f"Disponible: {servicio.disponible}")
        print(f"ID: {servicio.id}")

    def cambiar_disponibilidad(self):
        # Invierte el estado de disponibilidad actual (disponible / no disponible)
        identificador = leer_texto("ID del servicio: ")

        servicio = self.gestor_servicios.buscar_por_id(identificador)

        nueva_disponibilidad = not servicio.disponible

        self.gestor_servicios.cambiar_disponibilidad(
            identificador,
            nueva_disponibilidad
        )

        print(
            "Servicio ahora disponible."
            if nueva_disponibilidad
            else "Servicio ahora no disponible."
        )

    def eliminar_servicio(self):
        # Pide confirmación antes de eliminar un servicio por ID
        identificador = leer_texto("ID del servicio que deseas eliminar: ")

        servicio = self.gestor_servicios.buscar_por_id(identificador)

        confirmacion = leer_opcion(
            f"¿Eliminar {servicio.nombre}? (s/n): ",
            ["s", "n"]
        )

        if confirmacion == "s":
            self.gestor_servicios.eliminar_servicio(identificador)
            print("Servicio eliminado correctamente.")
        else:
            print("Operación cancelada.")

    # ==========================================
    # GESTIÓN DE RESERVAS
    # ==========================================

    def menu_reservas(self):
        # Bucle del submenú para crear, consultar y cambiar el estado de reservas
        while True:
            print("\n----------- RESERVAS -----------")
            print("1. Crear reserva")
            print("2. Listar reservas")
            print("3. Buscar reserva por ID")
            print("4. Confirmar reserva")
            print("5. Cancelar reserva")
            print("6. Completar reserva")
            print("0. Volver")

            opcion = input("Selecciona una opción: ").strip()

            try:
                if opcion == "1":
                    self.crear_reserva()

                elif opcion == "2":
                    self.listar_reservas()

                elif opcion == "3":
                    self.buscar_reserva()

                elif opcion == "4":
                    self.confirmar_reserva()

                elif opcion == "5":
                    self.cancelar_reserva()

                elif opcion == "6":
                    self.completar_reserva()

                elif opcion == "0":
                    break

                else:
                    print("Opción no válida.")

            except Exception as error:
                # Registra cualquier error de reservas y sigue con el menú
                registrar_error("Error en el módulo de reservas", error)
                print(f"No se pudo completar la operación: {error}")

    def crear_reserva(self):
        # Solicita datos de cliente, servicio y duración para crear una reserva
        print("\nCREAR RESERVA")

        documento = leer_texto("Documento del cliente: ")
        identificador = leer_texto("ID del servicio: ")
        duracion = leer_decimal("Duración o cantidad de horas: ")

        servicio = self.gestor_servicios.buscar_por_id(identificador)

        unidades = 1

        # Si el servicio es alquiler de equipo, pide cuántas unidades reservar
        if isinstance(servicio, ServicioEquipo):
            unidades = leer_entero("Cantidad de unidades de equipo: ")

        reserva = self.gestor_reservas.crear_reserva(
            documento,
            identificador,
            duracion,
            unidades
        )

        print("\nReserva creada correctamente.")
        print(f"Identificador de reserva: {reserva.id}")
        print(f"Estado: {reserva.estado}")

    def listar_reservas(self):
        # Lista todas las reservas registradas con su cliente, servicio, estado y costo
        reservas = self.gestor_reservas.listar_reservas()

        if not reservas:
            print("No hay reservas registradas.")
            return

        print("\nLISTADO DE RESERVAS")

        for reserva in reservas:
            print("----------------------------------------")
            print(f"ID: {reserva.id}")
            print(f"Cliente: {reserva.cliente.nombre}")
            print(f"Servicio: {reserva.servicio.nombre}")
            print(f"Duración: {reserva.duracion}")
            print(f"Estado: {reserva.estado}")
            print(f"Costo: {reserva.costo_total}")

    def buscar_reserva(self):
        # Busca una reserva por su ID y muestra sus detalles
        identificador = leer_texto("ID de la reserva: ")

        reserva = self.gestor_reservas.buscar_por_id(identificador)

        print("\nRESERVA ENCONTRADA")
        print(f"ID: {reserva.id}")
        print(f"Cliente: {reserva.cliente.nombre}")
        print(f"Servicio: {reserva.servicio.nombre}")
        print(f"Duración: {reserva.duracion}")
        print(f"Estado: {reserva.estado}")
        print(f"Costo: {reserva.costo_total}")

    def confirmar_reserva(self):
        # Confirma una reserva por ID y muestra el costo total calculado
        identificador = leer_texto("ID de la reserva: ")

        reserva = self.gestor_reservas.confirmar_reserva(identificador)

        print("Reserva confirmada correctamente.")
        print(f"Costo total: {reserva.costo_total}")

    def cancelar_reserva(self):
        # Cancela una reserva existente según su ID
        identificador = leer_texto("ID de la reserva: ")

        self.gestor_reservas.cancelar_reserva(identificador)

        print("Reserva cancelada correctamente.")

    def completar_reserva(self):
        # Marca una reserva como completada según su ID
        identificador = leer_texto("ID de la reserva: ")

        self.gestor_reservas.completar_reserva(identificador)

        print("Reserva completada correctamente.")

    # ==========================================
    # RESUMEN GENERAL
    # ==========================================

    def mostrar_resumen(self):
        # Muestra el total actual de clientes, servicios y reservas en el sistema
        print("\n========== RESUMEN DEL SISTEMA ==========")
        print(f"Clientes: {self.gestor_clientes.cantidad_clientes}")
        print(f"Servicios: {self.gestor_servicios.cantidad_servicios}")
        print(f"Reservas: {self.gestor_reservas.cantidad_reservas}")
        print("=========================================")


def ejecutar_menu():
    """Punto de entrada de la interfaz de consola."""
    # Crea la instancia del menú y arranca su ejecución
    sistema = MenuSoftwareFJ()
    sistema.ejecutar()