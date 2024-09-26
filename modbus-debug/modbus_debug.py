"""
Modbus: Slave Modbus RTU in Python

(C)2024 - Carlos Briceño - carjavi@hotmail.com

Para Usarse con DRAGINO 485-LB nodo LoRaWAN

Nota: Puerto UART para el 485LB = ttyS0

"""
import sys
import time
import threading
import logging
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus as modbus
import modbus_tk.modbus_rtu as modbus_rtu
import serial


# Configuración inicial de los registros de holding
holding_register_values = [0, 0, 0, 0, 0, 0, 0, 0]  

def close_serial_port(serial_port):
    """Cierra el puerto serial si está abierto"""
    if serial_port.is_open:
        serial_port.close()
        print(f"Puerto serial {serial_port.port} estaba abieto, se cerro para continuar.")

def initialize_sensor():
    sensor_port = serial.Serial("/dev/ttyUSB0", 115200)
    return sensor_port


def update_registers_loop(slave, sensor_port):
    """Bucle infinito para actualizar los valores de los registros holding con los datos del sensor"""
    global holding_register_values
    while True:
        #distance, confidence = read_sensor(myPing)
        holding_register_values[0] = 100 
        holding_register_values[1] = 200
        holding_register_values[2] = 300
        holding_register_values[3] = 400 
        holding_register_values[4] = 500 
        holding_register_values[5] = 600 
        holding_register_values[6] = 700 
        holding_register_values[7] = 800 
        slave.set_values('0', 0, holding_register_values)  # Guardar valores en los registros 
        #print("ready...")
        time.sleep(1)  # Intervalo de actualización (1 segundo)

if __name__ == "__main__":
    # Configuración del puerto serial para el servidor Modbus RTU
    modbus_port = serial.Serial('/dev/ttyS0', 9600)
    close_serial_port(modbus_port)  # Cierra el puerto si está abierto antes de iniciar el servidor

    # Crear el servidor Modbus RTU
    server = modbus_rtu.RtuServer(modbus_port)

    sensor_port = initialize_sensor()

    try:
        print("running... enter 'quit' for closing the server")
        
        server.start()
        
        # esclavo dirección 0x01
        slave_1 = server.add_slave(1)
        # Añadir un bloque de registros holding 
        slave_1.add_block('0', cst.HOLDING_REGISTERS, 0, 8)  

        # Iniciar el Demonio para la actualización de los registros
        sensor_thread = threading.Thread(target=update_registers_loop, args=(slave_1, sensor_port))
        sensor_thread.daemon = True  # El demonio se cerrará cuando el programa principal termine
        sensor_thread.start()

        while True:
            
            # Comando de consola para manejo del servidor
            cmd = sys.stdin.readline()
            args = cmd.split(' ')
            if cmd.find('quit') == 0:
                sys.stdout.write('bye-bye\r\n')
                break
    finally:
        server.stop()
        #close_serial_port(modbus_port)  # Cerrar el puerto ttyS0 al finalizar el servidor

