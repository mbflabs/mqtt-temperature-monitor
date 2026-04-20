import paho.mqtt.client as mqtt
import random
import time
import json

# Konfigurasi MQTT Broker (pakai broker gratis dari EMQX)
BROKER = "broker.emqx.io"  # MQTT broker gratis untuk testing
PORT = 1883
TOPIC = "rumah/suhu"

# Buat client MQTT
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("✅ Berhasil terhubung ke MQTT Broker!")
    else:
        print(f"❌ Gagal terhubung, kode: {rc}")

client.on_connect = on_connect
client.connect(BROKER, PORT)
client.loop_start()  # Mulai loop jaringan di background

# Kirim data suhu setiap 3 detik
try:
    suhu = 25.0
    while True:
        # Simulasi perubahan suhu
        suhu += random.uniform(-0.5, 0.5)
        suhu = round(suhu, 1)
        
        # Buat data dalam format JSON
        data = {
            "suhu": suhu,
            "ruangan": "Ruang Tamu",
            "timestamp": time.strftime("%H:%M:%S")
        }
        
        # Kirim data ke topic "rumah/suhu"
        client.publish(TOPIC, json.dumps(data))
        print(f"📤 Dikirim: {data}")
        
        time.sleep(3)
        
except KeyboardInterrupt:
    print("\n🛑 Program dihentikan")
    client.loop_stop()
    client.disconnect()
