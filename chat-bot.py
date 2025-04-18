import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import time
import google.generativeai as genai
import pyperclip  

#Chat-bot creato da Salvatore Naro
genai.configure(api_key="Your api key")#Your api key
model = genai.GenerativeModel('gemini-pro')


parole_volgari = ["coglione", "parolaccia2", "parolaccia3"]


risposte_bot = {
    "ciao": "Ciao! Come posso aiutarti?",
    "come stai?": "Sto bene, grazie! E tu?",
    "chi sei?": "Sono Chat-B",
    "chi sei": "Sono Chat-Bi",
    "chi ti ha creato": "Il mio fondatore, è Salvatore Naro ",
    "chi ti ha creato?": "Sono stato fondato da Salvatore Naro",
}
memoria_conversazione = []

def copia_testo(testo):
    pyperclip.copy(testo)

def visualizza_codice(codice):
    finestra_codice = tk.Toplevel(root)
    finestra_codice.title("Codice Generato")
    finestra_codice.geometry("500x300")
    finestra_codice.configure(bg="white")

    frame_codice = tk.Frame(finestra_codice, bg="white", padx=10, pady=10)
    frame_codice.pack(fill="both", expand=True)

    btn_copy = tk.Button(frame_codice, text="Copy", font=("Arial", 12), bg="white", fg="blue", bd=0, command=lambda: copia_testo(codice))
    btn_copy.pack(anchor="ne")

    tk.Label(frame_codice, text=codice, font=("Courier", 12), bg="white", fg="black", justify="left").pack(anchor="w")

    tk.Button(frame_codice, text="Chiudi", font=("Arial", 12), command=finestra_codice.destroy).pack(anchor="se", pady=10)

def calcola_eta(giorno, mese, anno):
    oggi = datetime.now()
    data_nascita = datetime(anno, mese, giorno)
    eta = oggi.year - data_nascita.year
    if (oggi.month, oggi.day) < (data_nascita.month, data_nascita.day):
        eta -= 1
    return eta

def scrivi_testo_lentamente(widget, testo, tag, callback=None):
    for carattere in testo:
        widget.config(state="normal")
        widget.insert("end", carattere, tag)
        widget.config(state="disabled")
        widget.update()
        time.sleep(0.02)
    if callback:
        callback()

def avvia_chat():
    try:
        nome = entry_nome.get().capitalize()
        sesso = var_sesso.get()
        giorno = int(spinner_giorno.get())
        mese = int(spinner_mese.get())
        anno = int(spinner_anno.get())

        if not nome or sesso not in ("Maschio", "Femmina"):
            messagebox.showerror("Errore", "Compila tutti i campi!")
            return

        eta = calcola_eta(giorno, mese, anno)
        schermata_iniziale.pack_forget()
        schermata_messaggio.pack(fill="both", expand=True)

        if eta < 18:
            scrivi_testo_lentamente(
                messaggio_testo,
                "Impossibile accedere perché sei minorenne.",
                "center",
                root.destroy,
            )
        else:
            benvenuto = f"Benvenuto {nome}!" if sesso == "Maschio" else f"Benvenuta {nome}!"
            scrivi_testo_lentamente(
                messaggio_testo,
                benvenuto,
                "center",
                lambda: [time.sleep(2), vai_alla_chat()],
            )
    except ValueError:
        messagebox.showerror("Errore", "Inserisci una data valida!")

def vai_alla_chat():
    schermata_messaggio.pack_forget()
    schermata_chat.pack(fill="both", expand=True)

def cerca_in_memoria(messaggio):
    parole_chiave = ["prima"]
    for parola in parole_chiave:
        if parola in messaggio:
            return True
    return False

def invia_messaggio(event=None):
    messaggio = entry_messaggio.get().strip().lower()
    entry_messaggio.delete(0, "end")

    if not messaggio:
        return

    if any(parola in messaggio for parola in parole_volgari):
        chat_area.config(state="normal")
        chat_area.insert("end", "OPERATORE: Non mandare messaggi volgari, visita la nostra politica e privacy situata nella sezione ESPLORA GPTi!\n", "violazione")
        chat_area.config(state="disabled")
        chat_area.see("end")
        return

    chat_area.config(state="normal")
    chat_area.insert("end", f"Tu: {messaggio}\n", "user")
    chat_area.config(state="disabled")
    chat_area.see("end")

    
    memoria_conversazione.append(f"Tu: {messaggio}")

    if messaggio == "chi ti ha creato?":
        risposta = "Salvatore Naro"
    elif cerca_in_memoria(messaggio):
        if len(memoria_conversazione) > 1:
            risposta = memoria_conversazione[-2]  
        else:
            risposta = "Non ci sono messaggi precedenti."
    else:
        risposta = risposte_bot.get(messaggio)
        if not risposta:
            response = model.generate_content(messaggio)
            risposta = response.text


    memoria_conversazione.append(f"Chat-B: {risposta}")

    if "```" in risposta:  
        codice = risposta.split("```")[1]  
        visualizza_codice(codice)
        scrivi_testo_lentamente(chat_area, f"Chat-B: Ho generato un codice per te. Controlla la nuova finestra!\n", "bot")
    else:
        scrivi_testo_lentamente(chat_area, f"Chat-B: {risposta}\n", "bot")

def esplora_gpt():
    schermata_chat.pack_forget()
    schermata_esplora.pack(fill="both", expand=True)

def indietro_da_esplora():
    schermata_esplora.pack_forget()
    schermata_chat.pack(fill="both", expand=True)

def espandi_sezione(titolo, descrizione):
    top = tk.Toplevel(root)
    top.title(titolo)
    top.geometry("400x300")
    top.configure(bg="black")
    tk.Label(top, text=titolo, font=("Arial", 18), wraplength=350, bg="black", fg="white").pack(pady=10)
    tk.Label(top, text=descrizione, font=("Arial", 14), wraplength=350, bg="black", fg="white").pack(pady=10)
    tk.Button(top, text="Chiudi", font=("Arial", 12), command=top.destroy).pack(pady=10)

def apri_menu():
    menu_frame.place(x=0, y=0, relwidth=0.4, relheight=1)

def chiudi_menu():
    menu_frame.place_forget()

def rimuovi_placeholder(event=None):
    if entry_messaggio.get() == "Scrivi un messaggio":
        entry_messaggio.delete(0, "end")
        entry_messaggio.config(fg="black")

def aggiungi_placeholder(event=None):
    if not entry_messaggio.get():
        entry_messaggio.insert(0, "Scrivi un messaggio")
        entry_messaggio.config(fg="grey")

root = tk.Tk()
root.title("Chat-B")
root.geometry("500x700")
root.configure(bg="black")

schermata_iniziale = tk.Frame(root, bg="black")
schermata_iniziale.pack(fill="both", expand=True)

tk.Label(schermata_iniziale, text="Nome:", font=("Arial", 14), fg="white", bg="black").pack(pady=5)
entry_nome = tk.Entry(schermata_iniziale, font=("Arial", 14))
entry_nome.pack(pady=5)

tk.Label(schermata_iniziale, text="Giorno di nascita:", font=("Arial", 14), fg="white", bg="black").pack(pady=5)
spinner_giorno = ttk.Spinbox(schermata_iniziale, from_=1, to=31, font=("Arial", 14))
spinner_giorno.pack(pady=5)

tk.Label(schermata_iniziale, text="Mese di nascita:", font=("Arial", 14), fg="white", bg="black").pack(pady=5)
spinner_mese = ttk.Spinbox(schermata_iniziale, from_=1, to=12, font=("Arial", 14))
spinner_mese.pack(pady=5)

tk.Label(schermata_iniziale, text="Anno di nascita:", font=("Arial", 14), fg="white", bg="black").pack(pady=5)
spinner_anno = ttk.Spinbox(schermata_iniziale, from_=1950, to=datetime.now().year, font=("Arial", 14))
spinner_anno.pack(pady=5)

tk.Label(schermata_iniziale, text="Sesso:", font=("Arial", 14), fg="white", bg="black").pack(pady=5)
var_sesso = tk.StringVar(value="Nessuno")
tk.Radiobutton(schermata_iniziale, text="Maschio", variable=var_sesso, value="Maschio", font=("Arial", 14), bg="black", fg="white").pack()
tk.Radiobutton(schermata_iniziale, text="Femmina", variable=var_sesso, value="Femmina", font=("Arial", 14), bg="black", fg="white").pack()

tk.Button(schermata_iniziale, text="Continua", font=("Arial", 14), command=avvia_chat).pack(pady=20)

schermata_messaggio = tk.Frame(root, bg="black")
messaggio_testo = tk.Text(schermata_messaggio, font=("Arial", 18), bg="black", fg="green", wrap="word", state="disabled", height=10)
messaggio_testo.pack(expand=True, fill="both", padx=10, pady=10)
messaggio_testo.tag_configure("center", justify="center")

schermata_chat = tk.Frame(root, bg="black")

chat_area = tk.Text(schermata_chat, font=("Arial", 14), fg="white", bg="black", state="disabled", wrap="word")
chat_area.pack(fill="both", expand=True, padx=10, pady=10)
chat_area.tag_configure("user", foreground="cyan", justify="center")
chat_area.tag_configure("bot", foreground="white", justify="center")
chat_area.tag_configure("violazione", foreground="red", justify="center")

frame_input = tk.Frame(schermata_chat, bg="black")
frame_input.pack(fill="x", padx=10, pady=10)

entry_messaggio = tk.Entry(frame_input, font=("Arial", 14), bg="white", fg="grey")
entry_messaggio.insert(0, "Scrivi un messaggio")
entry_messaggio.bind("<FocusIn>", rimuovi_placeholder)
entry_messaggio.bind("<FocusOut>", aggiungi_placeholder)
entry_messaggio.bind("<Return>", invia_messaggio)
entry_messaggio.pack(side="left", fill="x", expand=True, padx=10)

btn_invia = tk.Button(frame_input, text="↑", font=("Arial", 14), bg="white", command=invia_messaggio)
btn_invia.pack(side="right", padx=10)

menu_btn = tk.Button(schermata_chat, text="≡", font=("Arial", 14), bg="black", fg="white", bd=0, command=apri_menu)
menu_btn.place(x=10, y=10)

menu_frame = tk.Frame(root, bg="black")

tk.Button(menu_frame, text="←", font=("Arial", 14), bg="black", fg="white", bd=0, command=chiudi_menu).pack(anchor="nw", padx=10, pady=10)

tk.Button(menu_frame, 
          text="Esplora GPT", 
          font=("Arial", 14), 
          fg="white", 
          bg="black", 
          bd=0, 
          highlightthickness=0,  
          activebackground="black", 
          activeforeground="white", 
          command=esplora_gpt).pack(side="top", fill="x", padx=10, pady=2)

schermata_esplora = tk.Frame(root, bg="black")
tk.Button(schermata_esplora, text="Esplora GPT", font=("Arial", 18), fg="white", bg="black", command=lambda: None).pack(pady=10)
sections = [
    ("Politica e Privacy", "Informazioni dettagliate sulla politica e privacy."),
    ("Modelli GPT", "Scopri i modelli GPT e le loro funzionalità."),
    ("Lavora con noi", "Entra nel nostro team e cresci con noi."),
]

for titolo, descrizione in sections:
    frame = tk.Frame(schermata_esplora, bg="white", padx=5, pady=5)
    frame.pack(fill="x", padx=10, pady=5)
    tk.Label(frame, text=titolo, font=("Arial", 14), bg="white").pack(side="left", padx=5)
    tk.Button(frame, text="Leggi", font=("Arial", 12), command=lambda t=titolo, d=descrizione: espandi_sezione(t, d)).pack(side="right")

tk.Button(schermata_esplora, text="← Indietro", font=("Arial", 14), command=indietro_da_esplora).pack(pady=10)

root.mainloop()
