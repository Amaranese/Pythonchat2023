import socket
import threading

# Configuración del servidor
host = '127.0.0.1'  # Puedes cambiarlo a tu dirección IP pública si deseas que otros se conecten a tu chat
port = 55555

# Inicialización del socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

# Listas para almacenar los clientes y sus nombres
clientes = []
nombres = []


# Función para enviar mensajes a todos los clientes conectados
def broadcast(mensaje):
    for cliente in clientes:
        cliente.send(mensaje)


# Función para manejar las conexiones de los clientes
def manejar_cliente(cliente):
    while True:
        try:
            # Recibir y retransmitir mensajes
            mensaje = cliente.recv(1024)
            broadcast(mensaje)
        except:
            # Eliminar y cerrar la conexión del cliente si ocurre algún error
            index = clientes.index(cliente)
            clientes.remove(cliente)
            cliente.close()
            nombre = nombres[index]
            broadcast(f'{nombre} se ha desconectado'.encode('utf-8'))
            nombres.remove(nombre)
            break


# Función principal para aceptar conexiones y manejar clientes
def iniciar_chat():
    while True:
        # Aceptar conexiones entrantes
        cliente, direccion = server.accept()
        print(f'Conectado a {str(direccion)}')

        # Solicitar y almacenar el nombre del cliente
        cliente.send('NOMBRE'.encode('utf-8'))
        nombre = cliente.recv(1024).decode('utf-8')
        nombres.append(nombre)
        clientes.append(cliente)

        # Notificar a todos los clientes sobre el nuevo participante
        print(f'Nombre del cliente: {nombre}')
        broadcast(f'{nombre} se ha unido al chat'.encode('utf-8'))
        cliente.send('Conexión establecida'.encode('utf-8'))

        # Iniciar un hilo para manejar al cliente
        cliente_thread = threading.Thread(target=manejar_cliente, args=(cliente,))
        cliente_thread.start()


# Iniciar el servidor de chat
print('Esperando conexiones...')
iniciar_chat()

