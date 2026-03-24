from flask import Flask, render_template
from flask_mail import Mail, Message

app = Flask(__name__)

# Configuración de Flask-Mail (igual que en tu app principal)
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'tu_correo@gmail.com'
app.config['MAIL_PASSWORD'] = 'tu_contraseña_de_app'
app.config['MAIL_DEFAULT_SENDER'] = 'tu_correo@gmail.com'
app.config['MAIL_ASCII_ATTACHMENTS'] = False

mail = Mail(app)

with app.app_context():
    # Correo de prueba usando el template de notificación de login
    msg = Message(
        subject="Prueba de notificación de inicio de sesión",
        recipients=["destinatario@gmail.com"]  # pon aquí tu correo real
    )
    msg.html = render_template("emails/login_notification.html", nombre="Cristian Muñoz")
    mail.send(msg)
    print("✅ Correo de prueba de login enviado correctamente")
