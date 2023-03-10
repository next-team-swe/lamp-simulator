from flask import Flask, jsonify, render_template, request
from supabase import create_client, Client
import paho.mqtt.client as mqtt
import json

url: str = "https://banraxrzqacvpzsonavh.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJhbnJheHJ6cWFjdnB6c29uYXZoIiwicm9sZSI6ImFub24iLCJpYXQiOjE2NzczMzkzNTksImV4cCI6MTk5MjkxNTM1OX0.gRfvdnzSN_jBTmi2iY1GPOK10flQIp_tUgyeRD3K90I"
supabase: Client = create_client(url, key)

app = Flask(__name__)

lights = (supabase.table("light").select("*").execute()).data
lights_ip = {}
for light in lights:
    lights_ip[light["ip_address"]] = light

last_changed = lights_ip[list(lights_ip.keys())[0]]

# Identificativo del lampione
lamp_id = 123

# Stato del lampione (True = acceso, False = spento)
lamp_status = False

# Luminosità del lampione (0 = spento, 1-10 = luminosità impostata)
brightness = 0

""" # Configurazione del client MQTT
mqtt_broker_address = 'localhost'
mqtt_broker_port = 1883
mqtt_topic = 'manage_lamps'

mqtt_client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    # Connessione al broker MQTT
    print('Connected to MQTT broker')
    # Sottoscrizione al topic relativo allo stato del lampione
    client.subscribe(mqtt_topic)

def on_message(client, userdata, message):
    # Ricezione di un messaggio sul topic relativo allo stato del lampione
    global lamp_status, brightness
    payload = message.payload.decode('utf-8')
    data = json.loads(payload)
    if (data.get('lamp_id') == lamp_id):
        lamp_status = data.get('lamp_status', lamp_status)
        brightness = data.get('brightness', brightness)
        print(f"LAMP {lamp_id}: status [{lamp_status}] and brightness [{brightness}] updated.")
    else:
        print(f"LAMP {lamp_id}: message with lamp_id [{data.get('lamp_id')}] not for me. Ignored.")


# Configurazione dei callback MQTT
mqtt_client.on_connect = on_connect
mqtt_client.on_message = on_message
 """
# API REST per ottenere lo stato del lampione e la luminosità impostata
@app.route('/lamp', methods=['GET'])
def get_lamp_status():
    return jsonify({'lamp_id': last_changed["id"], 'lamp_status': last_changed["state"], 'brightness': last_changed["brightness"], 'lamp_ip': last_changed["ip_address"]})

# API REST per accendere o spegnere il lampione e impostare la luminosità
@app.route('/lamp', methods=['POST'])
def set_lamp_status():
    global lamp_status, brightness, last_changed
    data = request.get_json()
    """ if (data['lamp_id'] != lamp_id):
        return jsonify({'lamp_id': lamp_id, 'error': 'lamp_id is not the same of this lamp.'}), 400 """
    if('lamp_ip' not in data):
        return jsonify({'error': 'The ip address of the lamp is not defined'}), 400
    if('lamp_status' in data):
        lights_ip[data['lamp_ip']]["state"] = data['lamp_status']
        last_changed = lights_ip[data['lamp_ip']]
    if('brightness' in data):
        lights_ip[data['lamp_ip']]["brightness"] = data['brightness']
        last_changed = lights_ip[data['lamp_ip']]
    return jsonify({'lamp_id': lamp_id, 'lamp_status': lamp_status, 'brightness': brightness})

# Pagina web che mostra il quadrato sincronizzato con lo stato del lampione e la luminosità impostata
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    #mqtt_client.connect(mqtt_broker_address, mqtt_broker_port)
    #mqtt_client.loop_start()
    app.run(debug=True)
