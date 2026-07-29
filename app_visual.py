from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.core.clipboard import Clipboard
import webbrowser
import os
import re

ARCHIVO_CONFIG = "datos_usuario.txt"

def guardar_dato(nombre, valor):
    with open(ARCHIVO_CONFIG, "a") as f:
        f.write(f"{nombre}={valor}\n")

def leer_dato(nombre):
    if not os.path.exists(ARCHIVO_CONFIG):
        return None
    with open(ARCHIVO_CONFIG) as f:
        for linea in f:
            if linea.startswith(nombre):
                return linea.strip().split("=", 1)[1]
    return None

class PantallaApp(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.padding = 20
        self.spacing = 12
        self.contador_ciclos = 0
        self.es_pro = leer_dato("pro") == "SI"

        self.usuario = leer_dato("usuario")
        self.correo = leer_dato("correo")
        self.metodo = leer_dato("metodo")
        self.destino = leer_dato("destino")

        if not self.usuario:
            self.mostrar_registro()
        elif not self.destino:
            self.mostrar_elegir_metodo()
        else:
            self.mostrar_principal()

    def mostrar_registro(self):
        self.clear_widgets()
        self.add_widget(Label(text="🔒 REGISTRO", font_size=18, bold=True))
        self.add_widget(Label(text="Solo seguridad y evitar abusos", font_size=13, color=(0.6,0.6,0.6,1)))
        self.entrada_usuario = TextInput(hint_text="Nombre de usuario", multiline=False)
        self.add_widget(self.entrada_usuario)
        self.entrada_correo = TextInput(hint_text="Correo electrónico", multiline=False)
        self.add_widget(self.entrada_correo)
        self.entrada_clave = TextInput(hint_text="Contraseña", multiline=False, password=True)
        self.add_widget(self.entrada_clave)
        self.btn_registrar = Button(text="✅ CONTINUAR", font_size=16, background_color=(0.2,0.7,0.3,1))
        self.btn_registrar.bind(on_press=self.guardar_registro)
        self.add_widget(self.btn_registrar)

    def guardar_registro(self, instancia):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", self.entrada_correo.text.strip()):
            self.add_widget(Label(text="❌ Correo inválido", color=(1,0.2,0.2,1)))
            return
        self.usuario = self.entrada_usuario.text.strip()
        self.correo = self.entrada_correo.text.strip()
        guardar_dato("usuario", self.usuario)
        guardar_dato("correo", self.correo)
        self.mostrar_elegir_metodo()

    def mostrar_elegir_metodo(self):
        self.clear_widgets()
        self.add_widget(Label(text="💳 ¿Dónde querés recibir?", font_size=18, bold=True))
        self.add_widget(Label(text="Primero recibís en cripto, luego pasás a donde quieras", font_size=13, color=(0.6,0.6,0.6,1)))
        self.metodo_spinner = Spinner(
            text="Selecciona método",
            values=[
                "Binance", "FaucetPay", "PayPal (vía exchange)",
                "Payoneer (vía exchange)", "BNA+ / Naranja X (vía P2P)",
                "Cuenta bancaria (vía P2P)"
            ],
            size_hint=(1, None),
            height=44
        )
        self.add_widget(self.metodo_spinner)
        self.entrada_destino = TextInput(hint_text="Dirección / Usuario / Alias", multiline=False)
        self.add_widget(self.entrada_destino)
        self.btn_siguiente = Button(text="✅ GUARDAR", font_size=16, background_color=(0.2,0.7,0.3,1))
        self.btn_siguiente.bind(on_press=self.guardar_metodo)
        self.add_widget(self.btn_siguiente)

    def guardar_metodo(self, instancia):
        self.metodo = self.metodo_spinner.text
        self.destino = self.entrada_destino.text.strip()
        guardar_dato("metodo", self.metodo)
        guardar_dato("destino", self.destino)
        self.mostrar_principal()

    def activar_pro(self, instancia):
        guardar_dato("pro", "SI")
        self.es_pro = True
        self.mostrar_principal()

    def mostrar_principal(self):
        self.clear_widgets()
        self.contador_ciclos += 1
        if self.es_pro:
            self.add_widget(Label(text="⭐ VERSIÓN PRO ACTIVA", font_size=16, bold=True, color=(1,0.8,0,1)))
            self.add_widget(Label(text="✅ SIN ANUNCIOS - ELEGÍ TU RECOMPENSA", font_size=14, color=(0.2,0.8,0.2,1)))
        else:
            self.add_widget(Label(text="📱 VERSIÓN GRATUITA", font_size=16, bold=True))
            self.btn_actualizar = Button(text="💎 ACTUALIZAR A PRO", font_size=15, background_color=(0.8,0.6,0.1,1))
            self.btn_actualizar.bind(on_press=self.activar_pro)
            self.add_widget(self.btn_actualizar)
        self.add_widget(Label(text=f"👤 Bienvenido {self.usuario}", font_size=18, bold=True))
        self.add_widget(Label(text=f"📧 {self.correo[:10]}...", font_size=12))
        self.add_widget(Label(text=f"💳 Recibís en: {self.metodo}", font_size=14))
        self.add_widget(Label(text=f"🔑 Dato guardado: {self.destino[:15]}...", font_size=12))
        self.btn_copiar = Button(text="📋 COPIAR DIRECCIÓN", font_size=15, background_color=(0.3,0.5,0.8,1))
        self.btn_copiar.bind(on_press=lambda x: Clipboard.copy(self.destino))
        self.add_widget(self.btn_copiar)
        self.btn_faucet = Button(text="🔗 FaucetPay - RECLAMAR", font_size=15, background_color=(0.2,0.6,0.4,1))
        self.btn_faucet.bind(on_press=lambda x: webbrowser.open(f"https://faucetpay.io/claim?address={self.destino}"))
        self.add_widget(self.btn_faucet)
        self.btn_free = Button(text="🔗 FreeBitco.in - RECLAMAR", font_size=15, background_color=(0.2,0.6,0.4,1))
        self.btn_free.bind(on_press=lambda x: webbrowser.open("https://freebitco.in/"))
        self.add_widget(self.btn_free)
        if not self.es_pro:
            self.add_widget(Label(text="✨ GRATIS: Elegí ver anuncio para ganar más", font_size=15, bold=True, color=(1,0.8,0,1)))
            self.btn_duplicar = Button(text="📺 1 anuncio + 1 captcha → DUPLICAR", font_size=15, background_color=(0.9,0.6,0.1,1))
            self.add_widget(self.btn_duplicar)
            self.btn_triplicar = Button(text="📺 1 anuncio + 2 captchas → TRIPLICAR", font_size=15, background_color=(1,0.4,0.1,1))
            self.add_widget(self.btn_triplicar)
            self.btn_normal = Button(text="⏭️ SALTAR - COBRAR NORMAL", font_size=15, background_color=(0.4,0.4,0.4,1))
            self.add_widget(self.btn_normal)
            if self.contador_ciclos % 4 == 0:
                self.add_widget(Label(text="\n🔔 Anuncio para apoyar la app", font_size=14, color=(0.7,0.7,1,1)))
        else:
            self.add_widget(Label(text="✨ PRO: SIN ANUNCIOS", font_size=15, bold=True, color=(1,0.8,0,1)))
            self.btn_doble = Button(text="✅ 1 captcha → DOBLE GANANCIA", font_size=15, background_color=(0.2,0.7,0.3,1))
            self.add_widget(self.btn_doble)
            self.btn_triple = Button(text="✅ 2 captchas → TRIPLICAR", font_size=15, background_color=(0.3,0.8,0.4,1))
            self.add_widget(self.btn_triple)
            self.btn_normal_pro = Button(text="⏭️ COBRAR NORMAL", font_size=15, background_color=(0.4,0.4,0.4,1))
            self.add_widget(self.btn_normal_pro)
        self.add_widget(Label(text="💡 Luego pasás a PayPal / BNA+ / Naranja X / Payoneer", font_size=12, color=(0.9,0.7,0.2,1)))

class AppAutomatizador(App):
    def build(self):
        return PantallaApp()

if __name__ == "__main__":
    AppAutomatizador().run()
