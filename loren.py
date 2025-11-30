import streamlit as st

# 1. Titolo
st.title("🍽️ Lorenellakitchen 🧑‍🍳")

# 2. Input numerico per il numero di persone
num_persone = st.number_input("Numero di persone", min_value=1, max_value=8)

# 3. Lista delle opzioni per il menu
possibili_menu = ["Menù alla cieca", "Menu su richiesta"]


scelta_menu = st.selectbox("Scegli il Menù", possibili_menu)

# Puoi anche mostrare all'utente la sua selezione (opzionale)
st.write(f"Hai selezionato: **{scelta_menu}**")

if scelta_menu == "Menù alla cieca":
    st.title("Menù alla cieca")
    st.subheader("Indica possibili allergie")
    lista_allergeni = [
        "Glutine (Celiachia)",
        "Lattosio/Latte",
        "Uova",
        "Frutta a guscio (Nocciole, Mandorle, Noci, ecc.)",
        "Arachidi",
        "Soia",
        "Pesce",
        "Crostacei",
        "Molluschi",
        "Senape",
        "Sesamo",
        "Sedano"
    ]
    allergie_selezionate = st.multiselect(
        "Indica tutte le allergie o intolleranze alimentari:",
        lista_allergeni,
        default=[])

    st.markdown("---")


    st.subheader("Preferenze e Gusti Alimentari")


    st.subheader("Selezione Proteine 🥩🐟")
    tipi_proteine = [
        "Solo carne bianca (es. pollo, tacchino)",
        "Solo pesce (tutti i tipi)",
        "Nessuna carne rossa (es. manzo, maiale)",
        "Vegetariano/Pesco-vegetariano",
        "Nessuna preferenza"
    ]
    preferenze_proteine = st.multiselect(
        "Hai delle restrizioni o preferenze specifiche su carni e pesce?",
        tipi_proteine,
        default=[]
    )

    st.markdown("---")


    st.subheader("Gusti e Sapori 🌶️🧀")
    gusti_chiave = [
        "Piccante/Speziato",
        "Formaggi stagionati (es. Parmigiano, Pecorino)",
        "Funghi e tartufi",
        "Cipolla, Aglio o Erbe Aromatiche Forti",
        "Dolci e dessert a base di frutta"
    ]
    preferenze_gusti = st.multiselect(
        "Indica i tuoi gusti o ingredienti preferiti:",
        gusti_chiave
    )

    st.markdown("---")

    st.subheader("Formula della cena")

    opzioni_prezzo = [
        "Antipasto + Primo → 45€",
        "Antipasto + Secondo → 50€",
        "Primo + Secondo → 55€",
        "Antipasto + Primo + Dolce → 55€",
        "Antipasto + Secondo + Dolce → 60€",
        "Primo + Secondo + Dolce → 65€"
    ]

    # 2. Utilizza st.radio per forzare l'utente a scegliere una sola opzione

    scelta_pacchetto = st.radio(
        "Seleziona il pacchetto che preferisci (prezzo a persona):",
        opzioni_prezzo,
        # Imposta un valore predefinito per chiarezza
        index= None  # Seleziona "Antipasto + Primo + Dolce → 55€" come default
    )

    try:
        # Trova l'ultima occorrenza di "€" e va indietro di 2 o 3 caratteri per prendere il numero
        prezzo_str = scelta_pacchetto.split("€")[0].split("→")[1].strip()
        prezzo_a_persona = int(prezzo_str)

        st.markdown("---")
        st.success(f"Hai scelto la formula **{scelta_pacchetto}**.")
        st.info(f"Il costo della tua cena è di circa **{prezzo_a_persona * num_persone}€**.")

    except Exception:
        # Gestione semplice degli errori
        st.warning("Inserisci la formula ideale per te")

