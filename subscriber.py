import paho.mqtt.client as mqtt
import json

# Konfigurasi (sama dengan publisher)
BROKER = "broker.emqx.io"
PORT = 1883
TOPIC = "rumah/suhu"

# Callback saat terhubung ke broker
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("✅ Terhubung ke MQTT Broker!")
        # Subscribe ke topic setelah terhubung
        client.subscribe(TOPIC)
        print(f"📡 Subscribe ke topic: {TOPIC}")
    else:
        print(f"❌ Gagal terhubung, kode: {rc}")

# Callback saat menerima pesan
def on_message(client, userdata, msg):
    try:
        # Parse data JSON
        data = json.loads(msg.payload.decode())
        print(f"📥 [Topic: {msg.topic}] Suhu: {data['suhu']}°C | Ruangan: {data['ruangan']} | Jam: {data['timestamp']}")
    except Exception as e:
        print(f"📥 [Topic: {msg.topic}] Pesan: {msg.payload.decode()}")

# Buat client
client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

# Koneksi ke broker
client.connect(BROKER, PORT)

# Loop forever (program akan terus berjalan)
print("🔄 Menunggu pesan... (Ctrl+C untuk berhenti)")
client.loop_forever()
