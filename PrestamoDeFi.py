import json
from web3 import Web3

from web3.exceptions import Web3Exception

try:
    # Conexión a Ganache
    ganache_url = "http://127.0.0.1:7545"
    w3 = Web3(Web3.HTTPProvider(ganache_url)) 

    if not w3.is_connected():
        print("No se pudo conectar a Ganache. Asegúrate de que Ganache esté en funcionamiento.")
        exit()
except Exception as e:
    print(f"Error al intentar conectar con Ganache: {e}")
    exit()

print("Conectado a Ganache")

# Direccion del contrato inteligente desplegado
contract_address = "0xA6fc9216b778CdEF75faE0484A3960E70Fd5839c"

# Direccion del socio principal
socio_principal_address = "0x3810af75EfDBc51521a7681fE42B9e1Afa5DC8c3"

# Clave privada del socio principal (necesaria para firmar transacciones)
socio_principal_private_key = "0x890080f87db7f650b8e593d9c80d720cc2c023ebcaaad53c16f99ad6f1b60e08"

contract_abi = json.loads('[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"prestatario","type":"address"},{"indexed":false,"internalType":"uint256","name":"monto","type":"uint256"}],"name":"GarantiaLiquidada","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"prestatario","type":"address"},{"indexed":false,"internalType":"uint256","name":"monto","type":"uint256"}],"name":"PrestamoAprobado","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"prestatario","type":"address"},{"indexed":false,"internalType":"uint256","name":"monto","type":"uint256"}],"name":"PrestamoReembolsado","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"prestatario","type":"address"},{"indexed":false,"internalType":"uint256","name":"monto","type":"uint256"},{"indexed":false,"internalType":"uint256","name":"plazo","type":"uint256"}],"name":"SolicitudPrestamo","type":"event"},{"inputs":[{"internalType":"address","name":"nuevoCliente","type":"address"}],"name":"altaCliente","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"nuevoPrestamista","type":"address"}],"name":"altaPrestamista","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"prestatario_","type":"address"},{"internalType":"uint256","name":"id_","type":"uint256"}],"name":"aprobarPrestamo","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"clientes","outputs":[{"internalType":"bool","name":"activado","type":"bool"},{"internalType":"uint256","name":"saldoGarantia","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"depositarGarantia","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"empleadosPrestamista","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"prestatario_","type":"address"},{"internalType":"uint256","name":"id_","type":"uint256"}],"name":"liquidarGarantia","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"prestatario_","type":"address"},{"internalType":"uint256","name":"id_","type":"uint256"}],"name":"obtenerDetalleDePrestamo","outputs":[{"components":[{"internalType":"uint256","name":"id","type":"uint256"},{"internalType":"address","name":"prestatario","type":"address"},{"internalType":"uint256","name":"monto","type":"uint256"},{"internalType":"uint256","name":"plazo","type":"uint256"},{"internalType":"uint256","name":"tiempoSolicitud","type":"uint256"},{"internalType":"uint256","name":"tiempoLimite","type":"uint256"},{"internalType":"bool","name":"aprobado","type":"bool"},{"internalType":"bool","name":"reembolsado","type":"bool"},{"internalType":"bool","name":"liquidado","type":"bool"}],"internalType":"struct PrestamoDeFi.Prestamo","name":"","type":"tuple"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"prestatario_","type":"address"}],"name":"obtenerPrestamosPorPrestatario","outputs":[{"internalType":"uint256[]","name":"","type":"uint256[]"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"id_","type":"uint256"}],"name":"reembolsarPrestamo","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"socioPrincipal","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"monto_","type":"uint256"},{"internalType":"uint256","name":"plazo_","type":"uint256"}],"name":"solicitarPrestamo","outputs":[{"internalType":"uint256","name":"id","type":"uint256"}],"stateMutability":"nonpayable","type":"function"}]')

contract = w3.eth.contract(address=contract_address, abi=contract_abi)

# Función para mostrar mensajes de éxito o fracaso
def mostrar_mensaje_operacion(resultado, exitoso=True):
    if exitoso:
        print("Operación completada exitosamente.")
    else:
        print("La operación ha fallado. Motivo:", resultado)

# Funcion para enviar transaccion:
def enviar_transaccion(w3, txn_dict, private_key):
    try:
        signed_txn = w3.eth.account.sign_transaction(txn_dict, private_key=private_key)
        
        txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        
        txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
        
        mostrar_mensaje_operacion("Transacción exitosa")
        return txn_receipt

    except Exception as e:

        # Lanzar la excepción para ser capturada por la función que llama
        raise Exception(f"Error al enviar la transacción: {e}")

# Funciones de interacción con el contrato

# Función para dar de alta a un prestamista por el socio principal
def alta_prestamista(nuevo_prestamista_address):
    try:
        # Construye la transacción con los detalles necesarios, incluyendo la dirección del nuevo prestamista.
        txn_dict = contract.functions.altaPrestamista(nuevo_prestamista_address).buildTransaction({
            'nonce': w3.eth.getTransactionCount(socio_principal_address),
            'gas': 1000000,
            'gasPrice': w3.toWei('30', 'gwei')
        })

        # Envía la transacción a la blockchain para su ejecución.
        txn_receipt = enviar_transaccion(w3, txn_dict, socio_principal_private_key)

        return txn_receipt

    except Exception as e:
        
        print(f"Error en alta_prestamista: {e}")  # Manejar errores

# Función para dar de alta a un cliente-prestatario.
def alta_cliente(nuevo_cliente_address, prestamista_address, prestamista_private_key):
    try:
        # Construye la transacción con los detalles necesarios, incluyendo la dirección del nuevo cliente.
        txn_dict = contract.functions.altaCliente(nuevo_cliente_address).buildTransaction({
            'nonce': w3.eth.getTransactionCount(prestamista_address),
            'gas': 1000000,
            'gasPrice': w3.toWei('30', 'gwei')
        })

        # Envía la transacción a la blockchain para su ejecución.
        txn_receipt = enviar_transaccion(w3, txn_dict, prestamista_private_key)

        return txn_receipt

    except Exception as e:
        
        print(f"Error en alta_cliente: {e}")  # Manejar errores

# Función depositar garantía del cliente-prestatario.
def depositar_garantia(direccion_cliente, valor, clave_privada_cliente):
    try:
        # Construye la transacción con el monto de la garantía.
        txn_dict = contract.functions.depositarGarantia().buildTransaction({
            'nonce': w3.eth.getTransactionCount(direccion_cliente),
            'gas': 1000000,
            'gasPrice': w3.toWei('30', 'gwei'),
            'value': valor
        })

        # Envía la transacción desde la cuenta del cliente.
        txn_receipt = enviar_transaccion(w3, txn_dict, clave_privada_cliente)

        return txn_receipt

    except Exception as e:
        
        print(f"Error en depositar_garantia: {e}")  # Manejar errores

# Función para que el cliente-prestatario pueda solicitar el préstamo.
def solicitar_prestamo(direccion_cliente, monto, plazo, clave_privada_cliente):
    try:
        # Verifica si el cliente tiene suficiente garantía.

        # Si cumple, envía la solicitud de préstamo.
        txn_dict = contract.functions.solicitarPrestamo(monto, plazo).buildTransaction({
            'nonce': w3.eth.getTransactionCount(direccion_cliente),
            'gas': 1000000,
            'gasPrice': w3.toWei('30', 'gwei')
        })

        # Envía la transacción y espera confirmación.
        txn_receipt = enviar_transaccion(w3, txn_dict, clave_privada_cliente)

        # Retorna el ID del préstamo solicitado.
        return txn_receipt

    except Exception as e:
        
        print(f"Error en solicitar_prestamo: {e}")  # Manejar errores

# Función para aprobar el préstamo.
def aprobar_prestamo(prestatario_address, prestamo_id, prestamista_address, prestamista_private_key):
    try:
        # Comprueba la validez del préstamo y del cliente-prestatario.

        # Si es válido, procede a aprobar el préstamo.
        txn_dict = contract.functions.aprobarPrestamo(prestatario_address, prestamo_id).buildTransaction({
            'nonce': w3.eth.getTransactionCount(prestamista_address),
            'gas': 1000000,
            'gasPrice': w3.toWei('30', 'gwei')
        })

        # Envía la transacción y espera confirmación.
        txn_receipt = enviar_transaccion(w3, txn_dict, prestamista_private_key)

        return txn_receipt

    except Exception as e:
        
        print(f"Error en aprobar_prestamo: {e}")  # Manejar errores

# Función para reembolsar el préstamo.
def reembolsar_prestamo(prestamo_id, cliente_address, cliente_private_key):
    try:
        # Verifica la validez del préstamo y si el cliente es el prestatario.

        # Envía la transacción para reembolsar el préstamo.
        txn_dict = contract.functions.reembolsarPrestamo(prestamo_id).buildTransaction({
            'nonce': w3.eth.getTransactionCount(cliente_address),
            'gas': 1000000,
            'gasPrice': w3.toWei('30', 'gwei')
        })

        # Espera la confirmación y retorna el resultado.
        txn_receipt = enviar_transaccion(w3, txn_dict, cliente_private_key)

        return txn_receipt

    except Exception as e:
        
        print(f"Error en reembolsar_prestamo: {e}")  # Manejar errores

# Función para liquidar la garantía.
def liquidar_garantia(prestamo_id, prestamista_address, prestamista_private_key):
    try:
        # Verifica si el préstamo está aprobado y no reembolsado y si ha vencido el plazo.

        # Envía la transacción para liquidar la garantía.
        txn_dict = contract.functions.liquidarGarantia(prestamo_id).buildTransaction({
            'nonce': w3.eth.getTransactionCount(prestamista_address),
            'gas': 1000000,
            'gasPrice': w3.toWei('30', 'gwei')
        })

        # Espera la confirmación y retorna el resultado.
        txn_receipt = enviar_transaccion(w3, txn_dict, prestamista_private_key)

        return txn_receipt

    except Exception as e:
        
        print(f"Error en liquidar_garantia: {e}")  # Manejar errores

# Función para obtener los prestamos por el cliente-prestatario.
def obtener_prestamos_prestatario(prestatario_address):
    try:
        # Realiza una llamada al contrato para obtener la lista de IDs de los préstamos del prestatario.
        prestamos = contract.functions.obtenerPrestamosPrestatario(prestatario_address).call()
        return prestamos

    except Exception as e:
        
        print(f"Error en obtener_prestamos_prestatario: {e}")  # Manejar errores

# Función para obtener detalle del préstamo.
def obtener_detalles_prestamo(prestatario_address, prestamo_id):
    try:
        # Realiza una llamada al contrato para obtener los detalles del préstamo.
        detalles = contract.functions.obtenerDetallesPrestamo(prestatario_address, prestamo_id).call()
        return detalles

    except Exception as e:
        
        print(f"Error en obtener_detalles_prestamo: {e}")  # Manejar errores
        





