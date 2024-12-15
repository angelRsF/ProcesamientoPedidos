# Crear una cola compartida
import queue
import random
import threading
import time

cola = queue.Queue(maxsize=5)#crear cola con tamaño máximo de 5
#crear instancia de Condition para coordinar los hilos
condition=threading.Condition()

#declaro variable compartida
pedidos=0

# Función del cliente
def cliente(id_cliente):
    global pedidos #se declara la variable compartida porque se va a operar con ella
    while True:
        with condition:
            if pedidos>=15:#condición para que salir de la función si los pedidos son 15
                return
            while cola.full():
                condition.wait()#se hace esperar hasta que la cola se vacíe
            pedidos+=1
            cola.put(pedidos) #colocar el pedido en la cola
            print(f"Cliente {id_cliente}: Generó Pedido - {pedidos}")
            condition.notify_all()#se notifica a los demás hilos
        time.sleep(random.uniform(1, 2))  #simular tiempo de generación de pedido

# Función del empleado
def empleado(id_empleado):
    while True:
        with condition:
            while cola.empty():
                if pedidos>=15:#condición para salir de la función cuando se hayan alcanzado los 15 pedidos
                    return
                condition.wait()#esperar si la cola está vacía
            numero = cola.get()#obtener un pedido de la cola
            print(f"Empleado {id_empleado}: Procesó Pedido - {numero}")
            condition.notify_all()#notifica a los demás hilos
        time.sleep(random.uniform(2,3))#simular tiempo de procesamiento
        cola.task_done()#Marcar la tarea como completada

# Crear hilos para clientes y empleados
clientes=[]
for i in range(3):
    t=threading.Thread(target= cliente, args=(i+1,))
    clientes.append(t)
    t.start()

empleados=[]
for i in range(2):
    t=threading.Thread(target=empleado, args=(i+1,))
    empleados.append(t)
    t.start()

# Esperar a que los clientes terminen
for c in clientes:
    c.join()
# Esperar a que los empleados terminen
for e in empleados:
    e.join()

print("Todos los pedidos han sido procesados.")
