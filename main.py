import flet as ft
from alert import AlertManager
from autonoleggio import Autonoleggio

FILE_AUTO = "automobili.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = "center"
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DALL'AUTONOLEGGIO DEL LAB03 ---
    autonoleggio = Autonoleggio("Polito Rent", "Alessandro Visconti")
    try:
        autonoleggio.carica_file_automobili(FILE_AUTO) # Carica il file
    except Exception as e:
        alert.show_alert(f"❌ {e}") # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile dell'autonoleggio
    txt_titolo = ft.Text(value=autonoleggio.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {autonoleggio.responsabile}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=autonoleggio.responsabile, label="Responsabile")

    # ListView per mostrare la lista di auto aggiornata
    lista_auto = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere una nuova automobile (marca, modello, anno, contatore posti)
    # TODO

    marca = ft.TextField(label="Marca")
    modello = ft.TextField(label="Modello")
    anno = ft.TextField(label="Anno")
    contatore = ft.TextField(width=100, disabled=True, value="0", border_color="green",
                          text_align=ft.TextAlign.CENTER)


    # --- FUNZIONI APP ---
    def aggiorna_lista_auto():
        lista_auto.controls.clear()
        for auto in autonoleggio.automobili_ordinate_per_marca():
            stato = "✅" if auto.disponibile else "⛔"
            lista_auto.controls.append(ft.Text(f"{stato} {auto}"))
        page.update()

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"
        page.update()

    def conferma_responsabile(e):
        autonoleggio.responsabile = input_responsabile.value
        txt_responsabile.value = f"Responsabile: {autonoleggio.responsabile}"
        page.update()

    # Handlers per la gestione dei bottoni utili all'inserimento di una nuova auto
    # TODO
    def handleAdd(e):
        try:
            currentVal = int(contatore.value)
        except Exception:
            currentVal = 0
        currentVal += 1
        contatore.value = str(currentVal)
        contatore.update()

    def handleRemove(e):
        try:
            currentVal = int(contatore.value)
        except Exception:
            currentVal = 0
        if currentVal > 0:
            currentVal -= 1
        contatore.value = str(currentVal)
        contatore.update()


    def btNPresserHandler(e):
        if marca.value.strip() == '' or modello.value.strip() == '' or anno.value.strip() == '' or contatore.value.strip() == '':
            alert.show_alert('❌ I Campi non possono essere vuoti')
            return

        try:
            anno_int = int(anno.value)
        except ValueError:
            alert.show_alert("❌ Nel campo 'Anno' ci deve essere un valore numerico intero")
            return

        try:
            posti = int(contatore.value)
        except ValueError:
            alert.show_alert('❌ Valore non valido per il numero di posti')
            return

        if posti <= 0:
            alert.show_alert('❌ Il numero di posti deve essere maggiore di zero')
            return

        try:
            autonoleggio.aggiungi_automobile(marca.value.strip(),modello.value.strip(), anno_int, posti)
        except Exception as exc:
            alert.show_alert(f"❌ Errore durante l'aggiunta: {exc}")
            return

        marca.value = ""
        modello.value = ""
        anno.value = ""
        contatore.value = "0"

        marca.update()
        modello.update()
        anno.update()
        contatore.update()

        aggiorna_lista_auto()
        alert.show_alert('✅ Automobile aggiunta correttamente!')

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.ElevatedButton("Conferma", on_click=conferma_responsabile)

    # Bottoni per la gestione dell'inserimento di una nuova auto
    # TODO
    btnPress = ft.ElevatedButton(text='Aggiungi Automobile',on_click=btNPresserHandler)     #bottone aggiungi automobile

    btnMinus = ft.IconButton(icon=ft.Icons.REMOVE, icon_color="red",        #bottone per diminuire il numero dei posti
                             icon_size=24, on_click=handleRemove)

    btnAdd = ft.IconButton(icon=ft.Icons.ADD,
                           icon_color="green",
                           icon_size=24, on_click=handleAdd)            #bottone per aumentare il numero dei posti

    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        # TODO
        ft.Divider(),
        ft.Text(value='Aggiungi nuova Automobile',
                              size=20),
        ft.Row([marca, modello, anno, btnMinus, contatore, btnAdd], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([btnPress], alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 4
        ft.Divider(),
        ft.Text("Automobili", size=20),
        lista_auto,
    )
    aggiorna_lista_auto()

ft.app(target=main)
