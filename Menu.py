import PFM_PrestamoDeFi_Python.PrestamoDeFi as PrestamoDeFi  # Importamos el módulo con las funciones y conexión a Ganache

def mostrar_menu():
    print("\nMenú de Interacción con el Contrato:")
    print("1. Dar de alta un prestamista")
    print("2. Dar de alta un cliente")
    print("3. Depositar garantía")
    print("4. Solicitar un préstamo")
    print("5. Aprobar un préstamo")
    print("6. Reembolsar un préstamo")
    print("7. Liquidar garantía")
    print("8. Obtener préstamos por prestatario")
    print("9. Obtener detalles de préstamo")
    print("0. Salir")
    opcion = input("Elige una opción: ")
    return opcion


def main():
    while True:
        opcion = mostrar_menu()

        try: 
            if opcion == "1": # Dar de alta un prestamista.
                address = input("Introduce la dirección del nuevo prestamista: ")
                resultado = PrestamoDeFi.alta_prestamista(address)
                print(f"Resultado: {resultado}")

            elif opcion == "2": # Dar de alta un cliente.
                address = input("Introduce la dirección del nuevo cliente: ")
                prestamista_address = input("Introduce tu dirección de prestamista: ")
                prestamista_private_key = input("Introduce tu clave privada de prestamista: ") # Mejorar seguridad
                resultado = PrestamoDeFi.alta_cliente(address, prestamista_address, prestamista_private_key)
                print(f"Resultado: {resultado}")

            elif opcion == '3': # Depositar garantía.
                valor = input("Introduce el valor a depositar: ")
                direccion_cliente = input("Introduce la dirección del cliente: ")
                clave_privada_cliente = input("Introduce la clave privada del cliente: ") # Mejorar seguridad
                resultado = PrestamoDeFi.depositar_garantia(direccion_cliente, valor, clave_privada_cliente)
                print(f"Resultado: {resultado}")

            elif opcion == '4': # Solicitar un préstamo.
                monto = input("Introduce el monto del préstamo: ")
                plazo = input("Introduce el plazo del préstamo: ")
                direccion_cliente = input("Introduce tu dirección de cliente: ")
                clave_privada_cliente = input("Introduce tu clave privada de cliente: ") # Mejorar seguridad
                resultado = PrestamoDeFi.solicitar_prestamo(direccion_cliente, monto, plazo, clave_privada_cliente)
                print(f"Resultado: {resultado}")
                
            elif opcion == '5': # Aprobar un préstamo.
                address = input("Introduce la dirección del prestatario: ")
                prestamo_id = input("Introduce el ID del préstamo: ")
                prestamista_address = input("Introduce tu dirección de prestamista: ")
                prestamista_private_key = input("Introduce tu clave privada de prestamista: ") # Mejorar seguridad
            
            elif opcion == "6": # Reembolsar un préstamo.
                prestamo_id = input("Introduce el ID del préstamo a reembolsar: ")
                cliente_address = input("Introduce tu dirección de cliente: ")
                cliente_private_key = input("Introduce la clave privada de cliente: ") # Mejorar seguridad
                resultado = PrestamoDeFi.reembolsar_prestamo(prestamo_id, cliente_address, cliente_private_key)
                print(f"Resultado: {resultado}")
            
            elif opcion == "7": # Liquidar garantía.
                address = input("Introduce la dirección del prestatario: ")
                prestamo_id = input("Introduce el ID del préstamo: ")
                resultado = PrestamoDeFi.liquidar_garantia(address, prestamo_id)
                print(f"Resultado: {resultado}")
            
            elif opcion == "8": # Obtener préstamos por prestatario.
                address = input("Introduce la dirección del prestatario: ")
                resultado = PrestamoDeFi.obtener_prestamos_por_prestatario(address)
                print(f"Préstamos: {resultado}")
           
            elif opcion == "9": # Obtener detalles de préstamo.
                address = input("Introduce la dirección del prestatario: ")
                prestamo_id = input("Introduce el ID del préstamo: ")
                resultado = PrestamoDeFi.obtener_detalle_de_prestamo(address, prestamo_id)
                print(f"Detalle del préstamo: {resultado}")
                
            elif opcion == '0': # Salir.
                break
            else:
                print("Opción no válida. Por favor inténtalo de nuevo.")  # Mensaje del error, volver a intentarlo.

        except Exception as e:
            print(f"Ocurrió un error: {e}")  # Mensaje del error.

if __name__ == "__main__":
    main()

