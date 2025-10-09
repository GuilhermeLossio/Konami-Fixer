from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from pdfrw import PdfReader, PdfWriter, PageMerge

def fill_konami_decklist(input_pdf_path, output_pdf_path, data):
    temp_pdf_path = "temp_filled_data.pdf"
    c = canvas.Canvas(temp_pdf_path, pagesize=letter)
    c.setFont("Helvetica", 12)

    # -----------------------------
    # Informações Pessoais
    # -----------------------------
    c.drawString(102, 720, data.get("first_middle_name", ""))  # First & Middle Name
    c.drawString(102, 695, data.get("last_name", ""))          # Last Name
    c.drawString(400, 695, data.get("country_of_residency", ""))  # Country of Residency
    ##c.drawString(520, 735, data.get("last_name_initial", ""))  # Last Name Initial
    c.drawString(345, 670, data.get("event_name", ""))         # Event Name
    c.setFont("Helvetica", 24)
    
    text = data.get("card_game_id", "")
    x, y = 110, 667
    spacing = 12  # pixels extras entre letras

    for i, char in enumerate(text):
        c.drawString(x + i * (c.stringWidth(char, "Helvetica", 12) + spacing), y, char)
        
    if "event_month" in data and "event_day" in data and "event_year" in data:
        c.drawString(347, 718, data["event_month"][0].zfill(2))
        c.drawString(401, 718, data["event_month"][1].zfill(2))
        c.drawString(457, 718, data["event_day"][0].zfill(2))
        c.drawString(495, 718, data["event_day"][1].zfill(2))
        """ for i, ch in enumerate(data["event_year"]):
            c.drawString(530 + i*15, 735, ch) """
    c.setFont("Helvetica", 12)
    

    # -----------------------------
    # Cartas
    # -----------------------------
    line_height = 17

    # Monster Cards (posição inicial aproximada)
    y_monster_start = 636
    for i, card in enumerate(data.get("monster_cards", [])):
        y = y_monster_start - i*line_height
        c.drawString(40, y, str(card.get("qty", "")))       # QTY
        c.drawString(62, y, card.get("name", ""))          # Nome
        c.drawString(205, y, str(card.get("pts", "")))      # PTS

    # Spell Cards
    y_spell_start = 636
    for i, card in enumerate(data.get("spell_cards", [])):
        y = y_spell_start - i*line_height
        c.drawString(225, y, str(card.get("qty", "")))      # QTY
        c.drawString(245, y, card.get("name", ""))          # Nome
        c.drawString(390, y, str(card.get("pts", "")))      # PTS

    # Trap Cards
    y_trap_start = 636
    for i, card in enumerate(data.get("trap_cards", [])):
        y = y_trap_start - i*line_height
        c.drawString(410, y, str(card.get("qty", "")))      # QTY
        c.drawString(430, y, card.get("name", ""))          # Nome
        c.drawString(575, y, str(card.get("pts", "")))      # PTS

    # Side Deck
    y_side_start = 295
    for i, card in enumerate(data.get("side_deck", [])):
        y = y_side_start - i*line_height
        c.drawString(40, y, str(card.get("qty", "")))
        c.drawString(62, y, card.get("name", ""))
        c.drawString(205, y, str(card.get("pts", "")))

    # Extra Deck
    y_extra_start = 295
    for i, card in enumerate(data.get("extra_deck", [])):
        y = y_extra_start - i*line_height
        c.drawString(225, y, str(card.get("qty", "")))
        c.drawString(245, y, card.get("name", ""))
        c.drawString(390, y, str(card.get("pts", "")))

    c.save()

    # -----------------------------
    # Mesclar com PDF original
    # -----------------------------
    template_pdf = PdfReader(input_pdf_path)
    overlay_pdf = PdfReader(temp_pdf_path)

    for page_num, page in enumerate(template_pdf.pages):
        overlay_page = overlay_pdf.pages[0]
        merger = PageMerge(page)
        merger.add(overlay_page).render()

    PdfWriter(output_pdf_path, trailer=template_pdf).write()
    print(f"PDF preenchido salvo em: {output_pdf_path}")
    return output_pdf_path

# -----------------------------
# Teste
# -----------------------------
if __name__ == "__main__":
    input_pdf_file = "./src/static/pdfs/decklist.pdf"  # PDF em branco
    output_pdf_file = "decklist_test_filled.pdf"

    test_data = {
        "first_middle_name": "João Pedro",
        "last_name": "Silva",
        "card_game_id": "1234567891",
        "country_of_residency": "Brazil",
        "last_name_initial": "S",
        "event_name": "Regional Tournament",
        "event_month": "01",
        "event_day": "15",
        "event_year": "2024",
        "monster_cards": [
            {"qty": 3, "name": "Blue-Eyes White Dragon", "pts": 10},
            {"qty": 2, "name": "Dark Magician", "pts": 0},
            {"qty": 3, "name": "Blue-Eyes White Dragon", "pts": 10},
            {"qty": 2, "name": "Dark Magician", "pts": 0},
            {"qty": 3, "name": "Blue-Eyes White Dragon", "pts": 10},
            {"qty": 2, "name": "Dark Magician", "pts": 0},
            {"qty": 3, "name": "Blue-Eyes White Dragon", "pts": 10},
            {"qty": 2, "name": "Dark Magician", "pts": 0},
            {"qty": 3, "name": "Blue-Eyes White Dragon", "pts": 10},
            {"qty": 2, "name": "Dark Magician", "pts": 0},
            {"qty": 3, "name": "Blue-Eyes White Dragon", "pts": 10},
            {"qty": 2, "name": "Dark Magician", "pts": 0},
            {"qty": 3, "name": "Blue-Eyes White Dragon", "pts": 10},
            {"qty": 2, "name": "Dark Magician", "pts": 0},
            {"qty": 3, "name": "Blue-Eyes White Dragon", "pts": 10},
            {"qty": 2, "name": "Dark Magician", "pts": 0},
            {"qty": 3, "name": "Blue-Eyes White Dragon", "pts": 10},
            {"qty": 2, "name": "Dark Magician", "pts": 0},
        ],
        "spell_cards": [
            {"qty": 2, "name": "Monster Reborn", "pts": 10},
            {"qty": 1, "name": "Pot of Greed", "pts": 0},
            {"qty": 2, "name": "Monster Reborn", "pts": 10},
            {"qty": 1, "name": "Pot of Greed", "pts": 0},
            {"qty": 2, "name": "Monster Reborn", "pts": 10},
            {"qty": 1, "name": "Pot of Greed", "pts": 0},
            {"qty": 2, "name": "Monster Reborn", "pts": 10},
            {"qty": 1, "name": "Pot of Greed", "pts": 0},
            {"qty": 2, "name": "Monster Reborn", "pts": 10},
            {"qty": 1, "name": "Pot of Greed", "pts": 0},
        ],
        "trap_cards": [
            {"qty": 2, "name": "Mirror Force", "pts": 10},
            {"qty": 1, "name": "Bottomless Trap Hole", "pts": 0},
            {"qty": 2, "name": "Mirror Force", "pts": 10},
            {"qty": 1, "name": "Bottomless Trap Hole", "pts": 0},
            {"qty": 2, "name": "Mirror Force", "pts": 10},
            {"qty": 1, "name": "Bottomless Trap Hole", "pts": 0},
            {"qty": 2, "name": "Mirror Force", "pts": 10},
            {"qty": 1, "name": "Bottomless Trap Hole", "pts": 0},
            {"qty": 2, "name": "Mirror Force", "pts": 10},
            {"qty": 1, "name": "Bottomless Trap Hole", "pts": 0},
        ],
        "side_deck": [
            {"qty": 1, "name": "Evenly Matched", "pts": 10},
            {"qty": 1, "name": "Evenly Matched", "pts": 10},
            {"qty": 1, "name": "Evenly Matched", "pts": 10},
            {"qty": 1, "name": "Evenly Matched", "pts": 10},
            {"qty": 1, "name": "Evenly Matched", "pts": 10},
            {"qty": 1, "name": "Evenly Matched", "pts": 10},
            {"qty": 1, "name": "Evenly Matched", "pts": 10},
            {"qty": 1, "name": "Evenly Matched", "pts": 10},
            {"qty": 1, "name": "Evenly Matched", "pts": 10},
            {"qty": 1, "name": "Evenly Matched", "pts": 10},
            {"qty": 1, "name": "Evenly Matched", "pts": 10},
            {"qty": 1, "name": "Evenly Matched", "pts": 10},
            {"qty": 1, "name": "Evenly Matched", "pts": 10},
            {"qty": 1, "name": "Evenly Matched", "pts": 10},
        ],
        "extra_deck": [
            {"qty": 1, "name": "Number 39: Utopia", "pts": 0},
        ],
    }

    fill_konami_decklist(input_pdf_file, output_pdf_file, test_data)
