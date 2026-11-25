from configuracion import generar_configuracion, generar_comandos_verificacion

def test_configuracion_crea_loopback_99():
    comandos = generar_configuracion()
    assert "interface Loopback100" in comandos
    assert "description LAB_CICD_PYTHON" in comandos
    assert "ip address 192.0.2.99 255.255.255.255" in comandos
    assert "no shutdown" in comandos

def test_verificacion_es_solo_lectura():
    comandos = generar_comandos_verificacion()
    assert "show ip interface brief" in comandos
    assert "show running-config interface Loopback99" in comandos
    assert all(comando.strip().lower().startswith("show") for comando in comandos)