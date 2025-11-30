import streamlit as st
from fpdf2 import FPDF
import io
import os


# --- FUNZIONE PER CREARE IL PDF (CORRETTA) ---
def crea_pdf_ordine(dati_ordine: dict) -> bytes:
    """Crea il PDF con i dati dell'ordine e lo ritorna come bytes (in memoria)."""

    pdf = FPDF()
    pdf.add_page()

    # Intestazione
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "Riepilogo Ordine - Lorenellakitchen", 0, 1, 'C')
    pdf.ln(5)

    # Contenuto
    pdf.set_font("Arial", "", 12)

    for key, value in dati_ordine.items():
        pdf.set_font("Arial", "B", 12)
        pdf.cell(50, 8, f"{key}:", 0, 0)

        pdf.set_font("Arial", "", 12)

        # Correzione multi_cell
        pdf.multi_cell(w=0, h=8, txt=str(value), border=0, ln=1)

    # Restituisce il PDF come bytes.
    return bytes(pdf.output(dest='S'))


# --- INTERFACCIA STREAMLIT ---

# 1. Titolo
st.title("🍽️ Lorenellakitchen 🧑‍🍳")

# 2. Input numerico per il numero di persone
num_persone = st.number_input("Numero di persone", min_value=1, max_value=8)

# 3. Lista delle opzioni per il menu
possibili_menu = ["Menù alla cieca", "Menu su richiesta"]

scelta_menu = st.selectbox("Scegli il Menù", possibili_menu)

st.write(f"Hai selezionato: **{scelta_menu}**")

# Inizializza le variabili essenziali
allergie_selezionate = []
preferenze_proteine = []
preferenze_gusti = []
scelta_pacchetto = None
prezzo_a_persona = 0

if scelta_menu == "Menù alla cieca":
    st.title("Menù alla cieca")
    st.subheader("Indica possibili allergie")
    lista_allergeni = [
        "Glutine (Celiachia)", "Lattosio/Latte", "Uova", "Frutta a guscio (Nocciole, Mandorle, Noci, ecc.)",
        "Arachidi", "Soia", "Pesce", "Crostacei", "Molluschi", "Senape", "Sesamo", "Sedano"
    ]
    allergie_selezionate = st.multiselect(
        "Indica tutte le allergie o intolleranze alimentari:",
        lista_allergeni,
        default=[])

    st.markdown("---")
    st.subheader("Preferenze e Gusti Alimentari")
    st.subheader("Selezione Proteine 🥩🐟")
    tipi_proteine = [
        "Solo carne bianca (es. pollo, tacchino)", "Solo pesce (tutti i tipi)",
        "Nessuna carne rossa (es. manzo, maiale)",
        "Vegetariano/Pesco-vegetariano", "Nessuna preferenza"
    ]
    preferenze_proteine = st.multiselect(
        "Hai delle restrizioni o preferenze specifiche su carni e pesce?",
        tipi_proteine,
        default=[]
    )

    st.markdown("---")
    st.subheader("Gusti e Sapori 🌶️🧀")
    gusti_chiave = [
        "Piccante/Speziato", "Formaggi stagionati (es. Parmigiano, Pecorino)", "Funghi e tartufi",
        "Cipolla, Aglio o Erbe Aromatiche Forti", "Dolci e dessert a base di frutta"
    ]
    preferenze_gusti = st.multiselect(
        "Indica i tuoi gusti o ingredienti preferiti:",
        gusti_chiave
    )

    st.markdown("---")
    st.subheader("Formula della cena")

    opzioni_prezzo = [
        "Antipasto + Primo → 45€", "Antipasto + Secondo → 50€", "Primo + Secondo → 55€",
        "Antipasto + Primo + Dolce → 55€", "Antipasto + Secondo + Dolce → 60€", "Primo + Secondo + Dolce → 65€"
    ]

    scelta_pacchetto = st.radio(
        "Seleziona il pacchetto che preferisci (prezzo a persona):",
        opzioni_prezzo,
        index=None
    )

    # --- LOGICA DI ESTRAZIONE DEL PREZZO ---

    if scelta_pacchetto:
        try:
            # Estrazione del prezzo
            prezzo_str = scelta_pacchetto.split("€")[0].split("→")[1].strip()
            prezzo_a_persona = int(prezzo_str)

            st.markdown("---")
            st.success(f"Hai scelto la formula **{scelta_pacchetto}**.")
            st.info(f"Il costo totale stimato della tua cena è di circa **{prezzo_a_persona * num_persone}€**.")

        except Exception:
            st.warning("Seleziona una formula ideale per te.")
            prezzo_a_persona = 0

    # --- INPUT DATI DI CONTATTO (AGGIUNTA) ---
    st.markdown("---")
    st.header("👤 Dati di Contatto")

    nome_contatto = st.text_input("Inserisci il tuo Nome e Cognome:", placeholder="Mario Rossi")
    telefono_contatto = st.text_input("Inserisci il tuo Numero di Telefono:", placeholder="333 1234567")

    # Condizione per mostrare la sezione di download
    if prezzo_a_persona > 0:

        # Verifichiamo che i campi obbligatori di contatto siano riempiti prima di generare il PDF
        if nome_contatto and telefono_contatto:

            st.markdown("---")
            st.header("📥 Scarica il Riepilogo Ordine")

            # 1. Pulizia della stringa (CORREZIONE UNICODE per '→' e '€')
            scelta_pacchetto_pulita = scelta_pacchetto
            scelta_pacchetto_pulita = scelta_pacchetto_pulita.replace("→", " > ")
            scelta_pacchetto_pulita = scelta_pacchetto_pulita.replace("€", " Euro")  # Correzione Euro

            # --- RACCOLTA DATI FINALE (INCLUSI CONTATTI) ---
            riepilogo_dati = {
                "Nome Contatto": nome_contatto,  # AGGIUNTA
                "Numero di Telefono": telefono_contatto,  # AGGIUNTA
                "Numero di Persone": num_persone,
                "Menù Scelto": scelta_menu,
                "Allergie/Intolleranze": ", ".join(allergie_selezionate) if allergie_selezionate else "Nessuna",
                "Preferenze Proteine": ", ".join(preferenze_proteine) if preferenze_proteine else "Nessuna preferenza",
                "Gusti/Sapori": ", ".join(preferenze_gusti) if preferenze_gusti else "Nessun gusto specifico",
                "Formula Scelta": scelta_pacchetto_pulita,
                "Costo Totale Stimato": f"{prezzo_a_persona * num_persone} Euro"
            }

            # Genera il contenuto del PDF
            try:
                pdf_bytes = crea_pdf_ordine(riepilogo_dati)

                # Aggiunge il bottone di download
                download_clicked = st.download_button(
                    label="Scarica Riepilogo PDF ⬇️",
                    data=pdf_bytes,
                    file_name="Ordine_Lorenellakitchen.pdf",
                    mime="application/pdf"
                )

                # Aggiunge st.balloons() al successo del download
                if download_clicked:
                    st.success("Riepilogo scaricato con successo!")
                    st.balloons()

            except Exception as e:
                st.error(f"Errore durante la generazione del PDF: {e}")

        else:
            st.warning("Completa i dati di contatto (Nome e Telefono) per generare il riepilogo.")
