from pybricks.hubs import PrimeHub
from pybricks.parameters import Port
from pybricks.pupdevices import ColorSensor, Motor, ForceSensor, UltrasonicSensor
from pybricks.tools import wait
from pybricks.parameters import Button

PORTS = (Port.A, Port.B, Port.C, Port.D, Port.E, Port.F)
PORT_PIXELS = {
    Port.A: (0, 0),
    Port.B: (0, 4),
    Port.C: (2, 0),
    Port.D: (2, 4),
    Port.E: (4, 0),
    Port.F: (4, 4),
}

hub = PrimeHub()


def map_ports() -> list[ColorSensor | Motor | ForceSensor | UltrasonicSensor]:
    available_device_types = (ColorSensor, Motor, ForceSensor, UltrasonicSensor)

    devices = []
    for port_index in range(6):
        port = PORTS[port_index]
        devices.append(None)
        for device_type in available_device_types:
            try:
                devices[port_index] = device_type(port)
                break
            except OSError:
                ...

    return devices


def get_device_name(
    device: ColorSensor | Motor | ForceSensor | UltrasonicSensor,
) -> str:
    device_type = type(device)
    return str(device_type).replace("<class '", "").replace("'>", "")


def generate_code_difinition(
    device: ColorSensor | Motor | ForceSensor | UltrasonicSensor, port: Port
) -> str:
    device_name: str = get_device_name(device)
    print(f"{device_name.lower()} = {device_name}({port})")


def print_hardware_difinitions(
    devices: list[ColorSensor | Motor | ForceSensor | UltrasonicSensor],
) -> None:
    for port_index in range(6):
        port = PORTS[port_index]
        device = devices[port_index]
        if device:
            device_name: str = get_device_name(device)
            print(f"{device_name.lower()} = {device_name}({port})")


def indicate_device(
    device: ColorSensor | Motor | ForceSensor | UltrasonicSensor,
) -> None:
    if device:
        if type(device) == ColorSensor:
            device.lights.on(100)
        elif type(device) == Motor:
            device.dc(100)


def indicate_port_on_matrix(port: Port) -> None:
    hub.display.off()
    x, y = PORT_PIXELS[port]
    hub.display.pixel(x, y)


def stop_device(device: ColorSensor | Motor | ForceSensor | UltrasonicSensor) -> None:
    if device:
        if type(device) == ColorSensor:
            device.lights.off()
        elif type(device) == Motor:
            device.stop()


def signal_devices(
    devices: list[ColorSensor | Motor | ForceSensor | UltrasonicSensor],
) -> None:
    indicator = 0

    while True:
        running_device = devices[indicator]
        indicate_port_on_matrix(port=PORTS[indicator])
        indicate_device(running_device)

        if Button.RIGHT in hub.buttons.pressed():
            stop_device(running_device)
            indicator = (indicator + 1) % 6
            wait(200)
        if Button.LEFT in hub.buttons.pressed():
            stop_device(running_device)
            indicator = (indicator - 1) % 6
            wait(200)

        wait(20)


def main() -> None:
    devices = map_ports()
    print_hardware_difinitions(devices)
    for device in devices:
        if type(device) == ColorSensor:
            device.lights.off()
    signal_devices(devices)


main()
