import os
import sys
from netmiko import ConnectHandler
from configuracion import generar_configuracion

def obtener_dispositivo():
    requeridas = [
        "NET_DEVICE_HOST",
        "NET_DEVICE_USER",
        "NET_DEVICE_PASSWORD"
    ]
    faltantes = [nombre for nombre in requeridas if not os.getenv(nombre)]
    if faltantes:
        raise ValueError(
            "Faltan variables de entorno: " + ", ".join(faltantes)
        )
    return {
        "device_type": os.getenv("NET_DEVICE_TYPE", "cisco_xe"),
        "host": os.environ["NET_DEVICE_HOST"],
        "username": os.environ["NET_DEVICE_USER"],
        "password": os.environ["NET_DEVICE_PASSWORD"],
        "port": int(os.getenv("NET_DEVICE_PORT", "22")),
        "conn_timeout": 20,
        "auth_timeout": 20,
        "banner_timeout": 20,
    }

def main():
    confirmar = input(
        "¿Confirmas que es tu Sandbox IOS XE privado de laboratorio?\n"
        "Escribe SI para continuar: "
    )
    if confirmar != "SI":
        print("Despliegue cancelado.")
        return

    dispositivo = obtener_dispositivo()
    print("Conectando al dispositivo...")
    with ConnectHandler(**dispositivo) as conexion:
        print("\n--- IDENTIFICACIÓN DEL EQUIPO ---")
        print(conexion.send_command("show version", read_timeout=30)[:1500])

        print("\n--- APLICANDO CONFIGURACIÓN ---")
        resultado = conexion.send_config_set(generar_configuracion())
        print(resultado)

        print("\n--- VERIFICACIÓN ---")
        verificacion = conexion.send_command(
            "show running-config interface Loopback99"
        )
        print(verificacion)

        if "192.0.2.99" not in verificacion:
            raise RuntimeError(
                "No se encontró la dirección IP esperada. "
                "Revisa el resultado con el docente."
            )

        print("\nDESPLIEGUE COMPLETADO Y VERIFICADO.")

if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print(f"ERROR: {error}")
        sys.exit(1)