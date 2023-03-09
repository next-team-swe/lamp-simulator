from flask import Flask, jsonify, render_template, request
import paho.mqtt.client as mqtt
import json

app = Flask(__name__)

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
    return jsonify({'lamp_id': lamp_id, 'lamp_status': lamp_status, 'brightness': brightness})

# API REST per accendere o spegnere il lampione e impostare la luminosità
@app.route('/lamp', methods=['POST'])
def set_lamp_status():
    global lamp_status, brightness
    data = request.get_json()
    if (data['lamp_id'] != lamp_id):
        return jsonify({'lamp_id': lamp_id, 'error': 'lamp_id is not the same of this lamp.'}), 400
    if('lamp_status' in data):
        lamp_status = data['lamp_status']
    if('brightness' in data):
        brightness = data['brightness']
    return jsonify({'lamp_id': lamp_id, 'lamp_status': lamp_status, 'brightness': brightness})

# Pagina web che mostra il quadrato sincronizzato con lo stato del lampione e la luminosità impostata
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

if __name__ == '__main__':
    #mqtt_client.connect(mqtt_broker_address, mqtt_broker_port)
    #mqtt_client.loop_start()
    app.run(debug=True)
