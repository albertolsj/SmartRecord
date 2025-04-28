import RPi.GPIO as GPIO
import time

GPIO.cleanup()


# Configura GPIO
SENSOR_GPIO = 17  # Pin where the photoelectric sensor is connected
GPIO.setmode(GPIO.BCM)
GPIO.setup(SENSOR_GPIO, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

print("ðŸ“¡ Testando sensor... Pressione Ctrl+C para parar.")

try:
    while True:
        estado = GPIO.input(SENSOR_GPIO)
        if estado:
            print("SENSOR ATIVO (detecao)")
        else:
            print("SENSOR INATIVO (sem detecao)")
        time.sleep(1)

except KeyboardInterrupt:
    print("\nEncerrando teste.")
    GPIO.cleanup()
