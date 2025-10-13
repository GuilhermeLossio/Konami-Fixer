from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from pdfrw import PdfReader, PdfWriter, PageMerge
from flask import url_for
import io
from datetime import datetime



def fill_konami_decklist(data, deck_data):
    input_pdf_file = "KonamiListFixer/src/static/pdfs/decklist.pdf"  # PDF em branco
    output_pdf_file = "KonamiListFixer/src/static/pdfs/decklist_test_filled.pdf"

    temp_pdf_path = "KonamiListFixer/src/static/pdfs/temp_filled_data.pdf"
    c = canvas.Canvas(temp_pdf_path, pagesize=letter)
    c.setFont("Helvetica", 12)

    # -----------------------------
    # Informações Pessoais
    # -----------------------------
    c.drawString(102, 720, data.get("first_middle_names", ""))  # First & Middle Name
    c.drawString(102, 695, data.get("last_names", ""))          # Last Name
    c.drawString(400, 695, data.get("country_residency", ""))  # Country of Residency
    ##c.drawString(520, 735, data.get("last_name_initial", ""))  # Last Name Initial
    c.drawString(345, 670, data.get("event_name", ""))         # Event Name
    c.setFont("Helvetica", 24)
    
    text = data.get("card_game_id", "")
    x, y = 110, 667
    spacing = 12  # pixels extras entre letras

    for i, char in enumerate(text):
        c.drawString(x + i * (c.stringWidth(char, "Helvetica", 12) + spacing), y, char)
        
        event_date_str = data.get("event_date", "")
    try:
        event_dt = datetime.strptime(event_date_str, "%Y-%m-%d")
        event_day = f"{event_dt.day:02}"
        event_month = f"{event_dt.month:02}"
        event_year = str(event_dt.year)
        
        # Desenha mês
        for i, ch in enumerate(event_day):
            c.drawString(347 + i*15, 718, ch)

        # Desenha dia
        for i, ch in enumerate(event_month):
            c.drawString(401 + i*15, 718, ch)

        # Desenha ano
        for i, ch in enumerate(event_year):
            c.drawString(455 + i*18, 718, ch)

    except Exception as e:
        print(f"Erro ao processar event_date: {event_date_str} -> {e}")
    c.setFont("Helvetica", 12)
    

    # -----------------------------
    # Cartas
    # -----------------------------
    line_height = 17
    total_genesys_points = 0
    total_main_quantity = 0
    
    # --- MONSTERS CARDS ---
    max_monster_quantity = 0
    max_monster_points = 0
    data["main"] = deck_data["main"]
    y_monster_start = 636
    monster_index = 0
    for card in data.get("main", []):
        if "monster" in card.get("type", "").lower():
            y = y_monster_start - monster_index * line_height
            quantity = card.get("quantity", 0)
            points = card.get("genesys_points", 0)

            c.drawString(40, y, str(quantity))  # QTY
            draw_fitted_text(c, 62, y, card.get("name", ""), max_width=130)
            c.drawString(205, y, str(points*quantity))  # PTS

            max_monster_quantity += quantity
            max_monster_points += points*quantity
            total_main_quantity += quantity
            total_genesys_points += points*quantity
            monster_index += 1

    # Mostra total de monstros
    c.drawString(40, 330, str(max_monster_quantity))
    c.drawString(205, 330, str(max_monster_points))

    # --- SPELL CARDS ---
    spell_quantity = 0
    spell_points = 0
    y_spell_start = 636
    spell_index = 0
    for card in data.get("main", []):
        if "spell" in card.get("type", "").lower():
            y = y_spell_start - spell_index * line_height
            quantity = card.get("quantity", 0)
            points = card.get("genesys_points", 0)

            c.drawString(225, y, str(quantity))
            draw_fitted_text(c, 245, y, card.get("name", ""), max_width=130)
            c.drawString(390, y, str(points*quantity))

            spell_quantity += quantity
            spell_points += points*quantity
            total_main_quantity += quantity
            total_genesys_points += points*quantity
            spell_index += 1

    c.drawString(225, 330, str(spell_quantity))
    c.drawString(390, 330, str(spell_points))
    

    # --- TRAP CARDS ---
    trap_quantity = 0
    trap_points = 0
    y_trap_start = 636
    trap_index = 0
    for card in data.get("main", []):
        if "trap" in card.get("type", "").lower():
            y = y_trap_start - trap_index * line_height
            quantity = card.get("quantity", 0)
            points = card.get("genesys_points", 0)

            c.drawString(410, y, str(quantity))
            draw_fitted_text(c, 430, y, card.get("name", ""), max_width=130)
            c.drawString(575, y, str(points*quantity))

            trap_quantity += quantity
            trap_points += points*quantity
            total_main_quantity += quantity
            total_genesys_points += points*quantity
            trap_index += 1

    c.drawString(415, 330, str(trap_quantity))
    c.drawString(580, 330, str(trap_points))

    # --- SIDE DECK ---
    side_quantity = 0
    side_points = 0
    y_side_start = 295
    data["side_deck"] = deck_data["side"]
    for i, card in enumerate(data.get("side_deck", [])):
        y = y_side_start - i * line_height
        quantity = card.get("quantity", 0)
        points = card.get("genesys_points", 0)

        c.drawString(40, y, str(quantity))
        draw_fitted_text(c, 62, y, card.get("name", ""), max_width=130)
        c.drawString(205, y, str(points*quantity))

        side_quantity += quantity
        side_points += points*quantity

    c.drawString(40, 40, str(side_quantity))
    c.drawString(205, 40, str(side_points))

    # --- EXTRA DECK ---
    extra_quantity = 0
    extra_points = 0
    y_extra_start = 295
    data["extra_deck"] = deck_data["extra"]
    for i, card in enumerate(data.get("extra_deck", [])):
        y = y_extra_start - i * line_height
        quantity = card.get("quantity", 0)
        points = card.get("genesys_points", 0)

        c.drawString(225, y, str(quantity))
        draw_fitted_text(c, 245, y, card.get("name", ""), max_width=130)
        c.drawString(390, y, str(points*quantity))

        extra_quantity += quantity
        extra_points += points*quantity

    c.drawString(225, 40, str(extra_quantity))
    c.drawString(390, 40, str(extra_points))


    # --- RESUMO GERAL ---
    c.setFont("Helvetica-Bold", 16)
    c.drawString(540, 670, f"{total_main_quantity}")
    c.drawString(570, 670, f"{total_genesys_points}")
    c.setFont("Helvetica-Bold", 12)
    
    

    c.save()

    # -----------------------------
    # Mesclar com PDF original
    # -----------------------------
    template_pdf = PdfReader(input_pdf_file)
    overlay_pdf = PdfReader(temp_pdf_path)

    for page_num, page in enumerate(template_pdf.pages):
        overlay_page = overlay_pdf.pages[0]
        merger = PageMerge(page)
        merger.add(overlay_page).render()
        
    
    # -----------------------------
    # Salvar memorias em Bytes
    # -----------------------------
    buffer = io.BytesIO()
    PdfWriter(buffer, trailer=template_pdf).write()
    buffer.seek(0)

    # This is a old code that save on memory
    """ PdfWriter(output_pdf_file, trailer=template_pdf).write()
    #decklistPath = url_for('static', filename=output_pdf_file)
    print(f"PDF preenchido salvo em: {output_pdf_file}")
    output_pdf_file = output_pdf_file.replace("./", "") """
    
        
    return buffer.getvalue()



def draw_fitted_text(c, x, y, text, max_width, initial_font_size=10, font_name="Helvetica"):
    """
    Diminui a fonte até o texto caber dentro do max_width.
    """
    font_size = initial_font_size
    c.setFont(font_name, font_size)
    
    # Calcula a largura do texto
    text_width = c.stringWidth(text, font_name, font_size)
    
    # Diminui a fonte até caber
    while text_width > max_width and font_size > 4:  # evita fonte minúscula demais
        font_size -= 0.5
        text_width = c.stringWidth(text, font_name, font_size)
    
    c.setFont(font_name, font_size)
    c.drawString(x, y, text)
    
# -----------------------------
# Teste
# -----------------------------
if __name__ == "__main__":
    test_data = {
        "first_middle_name": "João Pedro",
        "last_name": "Silva",
        "card_game_id": "1234567891",
        "country_residency": "Brazil",
        "last_name_initial": "S",
        "event_name": "Regional Tournament",
        "event_date": "2030-01-20",
        "monster_cards": [
            {"quantity": 3, "name": "Blue-Eyes White Dragon", "pts": 10},
            {"quantity": 2, "name": "Dark Magician", "pts": 0},
            {"quantity": 3, "name": "Blue-Eyes White Dragon", "pts": 10},
            {"quantity": 2, "name": "Dark Magician", "pts": 0},
            {"quantity": 3, "name": "Blue-Eyes White Dragon", "pts": 10},
            {"quantity": 2, "name": "Dark Magician", "pts": 0},
            {"quantity": 3, "name": "Blue-Eyes White Dragon", "pts": 10},
            {"quantity": 2, "name": "Dark Magician", "pts": 0},
            {"quantity": 3, "name": "Blue-Eyes White Dragon", "pts": 10},
            {"quantity": 2, "name": "Dark Magician", "pts": 0},
            {"quantity": 3, "name": "Blue-Eyes White Dragon", "pts": 10},
            {"quantity": 2, "name": "Dark Magician", "pts": 0},
            {"quantity": 3, "name": "Blue-Eyes White Dragon", "pts": 10},
            {"quantity": 2, "name": "Dark Magician", "pts": 0},
            {"quantity": 3, "name": "Blue-Eyes White Dragon", "pts": 10},
            {"quantity": 2, "name": "Dark Magician", "pts": 0},
            {"quantity": 3, "name": "Blue-Eyes White Dragon", "pts": 10},
            {"quantity": 2, "name": "Dark Magician", "pts": 0},
        ],
        "spell_cards": [
            {"quantity": 2, "name": "Monster Reborn", "pts": 10},
            {"quantity": 1, "name": "Pot of Greed", "pts": 0},
            {"quantity": 2, "name": "Monster Reborn", "pts": 10},
            {"quantity": 1, "name": "Pot of Greed", "pts": 0},
            {"quantity": 2, "name": "Monster Reborn", "pts": 10},
            {"quantity": 1, "name": "Pot of Greed", "pts": 0},
            {"quantity": 2, "name": "Monster Reborn", "pts": 10},
            {"quantity": 1, "name": "Pot of Greed", "pts": 0},
            {"quantity": 2, "name": "Monster Reborn", "pts": 10},
            {"quantity": 1, "name": "Pot of Greed", "pts": 0},
        ],
        "trap_cards": [
            {"quantity": 2, "name": "Mirror Force", "pts": 10},
            {"quantity": 1, "name": "Bottomless Trap Hole", "pts": 0},
            {"quantity": 2, "name": "Mirror Force", "pts": 10},
            {"quantity": 1, "name": "Bottomless Trap Hole", "pts": 0},
            {"quantity": 2, "name": "Mirror Force", "pts": 10},
            {"quantity": 1, "name": "Bottomless Trap Hole", "pts": 0},
            {"quantity": 2, "name": "Mirror Force", "pts": 10},
            {"quantity": 1, "name": "Bottomless Trap Hole", "pts": 0},
            {"quantity": 2, "name": "Mirror Force", "pts": 10},
            {"quantity": 1, "name": "Bottomless Trap Hole", "pts": 0},
        ],
        "side_deck": [
            {"quantity": 1, "name": "Evenly Matched", "pts": 10},
            {"quantity": 1, "name": "Evenly Matched", "pts": 10},
            {"quantity": 1, "name": "Evenly Matched", "pts": 10},
            {"quantity": 1, "name": "Evenly Matched", "pts": 10},
            {"quantity": 1, "name": "Evenly Matched", "pts": 10},
            {"quantity": 1, "name": "Evenly Matched", "pts": 10},
            {"quantity": 1, "name": "Evenly Matched", "pts": 10},
            {"quantity": 1, "name": "Evenly Matched", "pts": 10},
            {"quantity": 1, "name": "Evenly Matched", "pts": 10},
            {"quantity": 1, "name": "Evenly Matched", "pts": 10},
            {"quantity": 1, "name": "Evenly Matched", "pts": 10},
            {"quantity": 1, "name": "Evenly Matched", "pts": 10},
            {"quantity": 1, "name": "Evenly Matched", "pts": 10},
            {"quantity": 1, "name": "Evenly Matched", "pts": 10},
        ],
        "extra_deck": [
            {"quantity": 1, "name": "Number 39: Utopia", "pts": 0},
        ],
    }

    fill_konami_decklist(test_data)
