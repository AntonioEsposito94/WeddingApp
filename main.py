import os
import zipfile
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from flask import Flask, render_template, request, redirect, url_for
#from flask_sslify import SSLify  # Importa il modulo per forzare l'HTTPS

app = Flask(__name__)
#sslify = SSLify(app)  # Forza l'uso di HTTPS
# Inserisci i tuoi dati di email
SMTP_HOST = 'smtp.gmail.com'
SMTP_PORT = 587
EMAIL_ADDRESS = 'espositoant1994@gmail.com'
EMAIL_PASSWORD = 'zzqkjeipcokmctpv'

@app.route('/')
def index():
    # Inserisci gli obiettivi del gioco qui
    objectives = [
        "Obiettivo 1",
        "Obiettivo 2",
        "Obiettivo 3",
        # Aggiungi altri obiettivi qui
    ]
    return render_template('index.html', objectives=objectives)

def create_zip(file_paths, zip_filename):
    with zipfile.ZipFile(zip_filename, 'w') as zip_file:
        for file_path in file_paths:
            zip_file.write(file_path, os.path.basename(file_path))

@app.route('/upload', methods=['POST'])
def upload():
    print('Richiesta di upload ricevuta...')
    target = os.path.join(os.getcwd(), 'uploads')
    print('Percorso della cartella uploads:', target)
    if not os.path.isdir(target):
        os.mkdir(target)

    name = request.form['name']
    table_name = request.form['tableName']
    print('Nome e nome tavolo ricevuti:', name, table_name)
    print('Foto ricevute:', request.files)

    file_paths = []
    for objective in request.files:
        photo = request.files[objective]
        if photo.filename != '':
            photo_filename = os.path.join(target, f"{objective}.jpg")
            photo.save(photo_filename)
            file_paths.append(photo_filename)

    print('Foto scattate e salvate nella cartella:', file_paths)

    if file_paths:
        zip_filename = f"{name}_{table_name}.zip"
        create_zip(file_paths, zip_filename)

        # Invia l'archivio ZIP alla tua email
        send_email(name, table_name, zip_filename)

        # Elimina i file temporanei
        for file_path in file_paths:
            os.remove(file_path)
        os.remove(zip_filename)

        return "Foto caricate e inviate correttamente via email!"
    return "Errore durante il caricamento delle foto."

def send_email(name, table_name, zip_filename):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS
    msg['Subject'] = f"Matrimonio Game: {name} - {table_name}"

    body = f"Gentile {name},\nGrazie per aver partecipato al gioco da matrimonio. " \
           f"Di seguito troverai i tuoi obiettivi fotografici:\n\n" \
           f"Buona caccia fotografica!\n\nCordiali saluti,\nOrganizzatori del matrimonio"
    msg.attach(MIMEText(body, 'plain'))

    with open(zip_filename, 'rb') as f:
        part = MIMEApplication(f.read(), Name=os.path.basename(zip_filename))
        part['Content-Disposition'] = f'attachment; filename="{os.path.basename(zip_filename)}"'
        msg.attach(part)

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, EMAIL_ADDRESS, msg.as_string())

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
