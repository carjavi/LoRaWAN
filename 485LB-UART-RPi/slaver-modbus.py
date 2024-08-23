#!/usr/bin/env python
# -*- coding: utf_8 -*-
"""
Modbus: Slave Modbus RTU in Python

(C)2024 - Carlos Briceño - carjavi@hotmail.com

Para Usarse con DRAGINO 485-LB nodo LoRaWAN

pip3 install modbus_tk pyserial
pip3 install logging
pip3 install serial

"""

import sys
import time
import logging
import modbus_tk
import modbus_tk.defines as cst
import modbus_tk.modbus as modbus
import modbus_tk.modbus_rtu as modbus_rtu
import serial

# Configuración de los registros de holding con 3 valores enteros
holding_register_values = [123, 456, 789]  # Tres valores enteros predefinidos

logger = modbus_tk.utils.create_logger(name="console", record_format="%(message)s")

def update_registers(slave):
    """ Actualiza los valores de los registros holding del esclavo """
    global holding_register_values
    slave.set_values('0', 0, holding_register_values)  # Guardar valores en los registros 0, 1, 2

if __name__ == "__main__":
    # Configuración del puerto serial
    port = '/dev/ttyUSB0'  # Cambia al puerto serial UART para la conexion con el nodo LoRaWAN
    baudrate = 9600      # Configura el baud rate según tu necesidad

    # Crear el servidor Modbus RTU
    server = modbus_rtu.RtuServer(serial.Serial(port, baudrate))

    try:
        logger.info("running...")
        logger.info("enter 'quit' for closing the server")
        
        server.start()
        
        # esclavo dirección 0x01
        slave_1 = server.add_slave(1)
        # Añadir un bloque de registros holding para 3 registros
        slave_1.add_block('0', cst.HOLDING_REGISTERS, 0, 3)  # 3 registros

        while True:
            # Actualizar los valores de los registros holding
            update_registers(slave_1)

            # Esperar 10 segundos entre actualizaciones
            time.sleep(10)

            # Comando de consola para manejo del servidor
            cmd = sys.stdin.readline()
            args = cmd.split(' ')
            if cmd.find('quit') == 0:
                sys.stdout.write('bye-bye\r\n')
                break
            elif args[0] == 'add_slave':
                slave_id = int(args[1])
                server.add_slave(slave_id)
                sys.stdout.write('done: slave %d added\r\n' % (slave_id))
            elif args[0] == 'add_block':
                slave_id = int(args[1])
                name = args[2]
                block_type = int(args[3])
                starting_address = int(args[4])
                length = int(args[5])
                slave = server.get_slave(slave_id)
                slave.add_block(name, block_type, starting_address, length)
                sys.stdout.write('done: block %s added\r\n' % (name))
            elif args[0] == 'set_values':
                slave_id = int(args[1])
                name = args[2]
                address = int(args[3])
                values = [int(v) for v in args[4:]]
                slave = server.get_slave(slave_id)
                slave.set_values(name, address, values)
                values = slave.get_values(name, address, len(values))
                sys.stdout.write('done: values written: %s\r\n' % (str(values)))
            elif args[0] == 'get_values':
                slave_id = int(args[1])
                name = args[2]
                address = int(args[3])
                length = int(args[4])
                slave = server.get_slave(slave_id)
                values = slave.get_values(name, address, length)
                sys.stdout.write('done: values read: %s\r\n' % (str(values)))
            else:
                sys.stdout.write("unknown command %s\r\n" % (args[0]))
    finally:
        server.stop()
