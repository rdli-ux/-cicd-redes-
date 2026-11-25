def generar_configuracion():
    """Devuelve los comandos para crear una Loopback de laboratorio."""
    return [
        "interface Loopback99",
        "description LAB_CICD_PYTHON",
        "ip address 192.0.2.99 255.255.255.255",
        "no shutdown"
    ]

def generar_comandos_verificacion():
    """Comandos de solo lectura para comprobar el resultado."""
    return [
        "show ip interface brief",
        "show running-config interface Loopback99"
    ]

if __name__ == "__main__":
    print("Configuración que se propone aplicar:")
    for comando in generar_configuracion():
        print(comando)