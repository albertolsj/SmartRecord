import time
import psutil
import os
from gpiozero import Button
from opcua import Server
from sdnotify import SystemdNotifier

# WATCHDOG notifier start
notifier = SystemdNotifier()

# GPIO Configuration
SENSOR_GPIO = 17  # Pin where the photoelectric sensor is connected
sensor = Button(SENSOR_GPIO, pull_up=False)  # pull_down usado (como no seu original)

# OPC UA Server Configuration
server = Server()
server.set_endpoint("opc.tcp://0.0.0.0:4840/")  # Server listens on all interfaces
server.set_server_name("RaspberryPi OPC UA Server")

# Create Namespace
uri = "http://raspberrypi.opcua"
idx = server.register_namespace(uri)

# Create OPC UA nodes for monitoring
obj = server.nodes.objects

sensor_node = obj.add_variable(idx, "Signal", 0)
sensor_node.set_writable()

sensor_counter_node = obj.add_variable(idx, "Counter", 0)
sensor_counter_node.set_writable()

cpu_temp_node = obj.add_variable(idx, "Temperature", 0.0)
cpu_usage_node = obj.add_variable(idx, "CPU", 0.0)
ram_usage_node = obj.add_variable(idx, "RAM", 0.0)
disk_usage_node = obj.add_variable(idx, "Disk", 0.0)

# Start OPC UA Server
server.start()
print("✅ OPC UA Server started!")
notifier.notify("READY=1")  # Notify watchdog systemd that server is ready

def get_cpu_temp():
    """Reads the Raspberry Pi CPU temperature"""
    try:
        temp = os.popen("vcgencmd measure_temp").readline()
        return float(temp.replace("temp=", "").replace("'C\n", ""))
    except Exception:
        return 0.0

# Initialize sensor activation counter and state tracking
sensor_activation_count = 0
previous_sensor_state = 0

try:
    while True:
        # Read Raspberry Pi system data
        sensor_value = 1 if sensor.is_pressed else 0
        cpu_temp = get_cpu_temp()
        cpu_usage = psutil.cpu_percent()
        ram_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent

        # Detect rising edge for activation (LOW → HIGH)
        if sensor_value == 1 and previous_sensor_state == 0:
            sensor_activation_count += 1
            sensor_counter_node.set_value(sensor_activation_count)

        previous_sensor_state = sensor_value

        # Update OPC UA server values
        sensor_node.set_value(sensor_value)
        cpu_temp_node.set_value(cpu_temp)
        cpu_usage_node.set_value(cpu_usage)
        ram_usage_node.set_value(ram_usage)
        disk_usage_node.set_value(disk_usage)

        # Send watchdog "still alive" signal
        notifier.notify("WATCHDOG=1")

        # Print status to console
        print(f"Sensor: {'ACTIVE' if sensor_value else 'INACTIVE'} | "
              f"Activations: {sensor_activation_count} | "
              f"CPU Temp: {cpu_temp:.1f}°C | CPU: {cpu_usage}% | "
              f"RAM: {ram_usage}% | Disk: {disk_usage}%")

        time.sleep(1)  # Update every 1 second

except KeyboardInterrupt:
    print("\nShutting down OPC UA Server...")
    server.stop()
