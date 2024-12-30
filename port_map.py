from pybricks.hubs import PrimeHub
from pybricks.parameters import Port
from pybricks.pupdevices import ColorSensor, Motor, ForceSensor, UltrasonicSensor
from pybricks.tools import wait
from pybricks.parameters import Button

hub = PrimeHub()


def map_ports() -> dict[Port, (ColorSensor | Motor | ForceSensor | UltrasonicSensor)]:
    available_device_types = (ColorSensor, Motor, ForceSensor, UltrasonicSensor)

    ports = (Port.A, Port.B, Port.C, Port.D, Port.E, Port.F)
    port_devices = {
        Port.A: None,
        Port.B: None,
        Port.C: None,
        Port.D: None,
        Port.E: None,
        Port.F: None,
    }

    for port in ports:
        for device_type in available_device_types:
            try:
                port_devices[port] = device_type(port)
                break
            except OSError:
                ...

    return port_devices


def get_device_name(
    device: ColorSensor | Motor | ForceSensor | UltrasonicSensor,
) -> str:
    device_type = type(device)
    return str(device_type).replace("<class '", "").replace("'>", "")


def generate_code_difinition(device, port) -> str:
    device_name: str = get_device_name(device)
    print(f"{device_name.lower()} = {device_name}({port})")


def print_hardware_difinitions(port_devices: dict) -> None:
    for port, device in port_devices.items():
        device_name: str = get_device_name(device)
        print(f"{device_name.lower()} = {device_name}({port})")


def signal_color_sensor(sensor: ColorSensor) -> None:
    sensor.lights.off()
    wait(150)
    sensor.lights.on(100)
    wait(150)


def signal_motor(motor: Motor) -> None:
    motor.run_time(100, 100, wait=False)


def indicate_port_on_matrix(port: Port) -> None:
    port_pixels = {
        Port.A: (0, 0),
        Port.B: (0, 4),
        Port.C: (2, 0),
        Port.D: (2, 4),
        Port.E: (4, 0),
        Port.F: (4, 4),
    }
    hub.display.off()
    x, y = port_pixels[port]
    hub.display.pixel(x, y)


def signal_devices(port_devices: dict) -> None:
    indicator = 0  # TODO: rename

    while True:
        if Button.RIGHT in hub.buttons.pressed():
            indocator = (indicator + 1) % 6
        if Button.LEFT in hub.buttons.pressed():
            indocator = (indicator - 1) % 6

        port, device = port_devices.items()[indicator]
        indicate_port_on_matrix(port=port)
        device_name: str = get_device_name(device)
        if device_name == "ColorSensor":
            signal_color_sensor(device)
        elif device_name == "Motor":
            signal_motor(device)
        else:
            wait(100)


device_ports = map_ports()
print_hardware_difinitions(device_ports)
signal_devices(device_ports)
print("done")
# <class 'ColorSensor'> = <class 'ColorSensor'>(Port.C)
# <class 'Motor'> = <class 'Motor'>(Port.F)
# <class 'Motor'> = <class 'Motor'>(Port.A)
# <class 'ColorSensor'> = <class 'ColorSensor'>(Port.D)
# <class 'Motor'> = <class 'Motor'>(Port.B)
# <class 'Motor'> = <class 'Motor'>(Port.E)
