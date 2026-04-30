#!/usr/bin/env python3
"""
AnkiConnect Client - Interactúa con Anki Desktop via AnkiConnect addon
Requiere: Anki Desktop con addon AnkiConnect (code: 2055492159)
"""

import json
import urllib.request
import sys
import os

# Config
ANKI_CONNECT_URL = "http://localhost:8765"

def anki_request(action, **params):
    """Envia request a AnkiConnect"""
    payload = json.dumps({
        "action": action,
        "version": 6,
        "params": params
    }).encode('utf-8')
    
    req = urllib.request.Request(
        ANKI_CONNECT_URL,
        data=payload,
        headers={'Content-Type': 'application/json'}
    )
    
    try:
        response = urllib.request.urlopen(req)
        return json.loads(response.read())
    except Exception as e:
        print(f"❌ Error conectando a Anki: {e}")
        print(f"💡 Asegúrate que Anki Desktop esté abierto con AnkiConnect instalado")
        return None

def sync():
    """Sincroniza con el servidor"""
    result = anki_request("sync")
    if result and not result.get("error"):
        print("✅ Sincronización completa")
        return True
    else:
        error = result.get("error", "Unknown error") if result else "No response"
        print(f"❌ Error en sync: {error}")
        return False

def create_card(front, back, deck="Default"):
    """Crea una tarjeta básica y fuerza sync automático"""
    note = {
        "deckName": deck,
        "modelName": "Basic",
        "fields": {
            "Front": front,
            "Back": back
        },
        "tags": ["openclaw"]
    }
    
    result = anki_request("addNote", note=note)
    if result and not result.get("error"):
        print(f"✅ Card creada (ID: {result['result']})")
        
        # Sync automático después de crear
        print("🔄 Sincronizando con servidor...")
        sync()
        
        return result['result']
    else:
        error = result.get("error", "Unknown error") if result else "No response"
        print(f"❌ Error: {error}")
        return None

def create_deck(name):
    """Crea un nuevo deck"""
    result = anki_request("createDeck", deck=name)
    if result and not result.get("error"):
        print(f"✅ Deck '{name}' creado")
        
        # Sync automático después de crear
        print("🔄 Sincronizando con servidor...")
        sync()
        
        return True
    else:
        error = result.get("error", "Unknown error") if result else "No response"
        print(f"❌ Error: {error}")
        return False

def delete_card(note_id):
    """Elimina una card"""
    result = anki_request("deleteNotes", notes=[note_id])
    if result and not result.get("error"):
        print(f"✅ Card {note_id} eliminada")
        
        # Sync automático después de eliminar
        print("🔄 Sincronizando con servidor...")
        sync()
        
        return True
    else:
        error = result.get("error", "Unknown error") if result else "No response"
        print(f"❌ Error: {error}")
        return False

def list_decks():
    """Lista todos los decks"""
    result = anki_request("deckNames")
    if result and not result.get("error"):
        decks = result['result']
        print("📚 Decks disponibles:")
        for i, deck in enumerate(decks, 1):
            # Get card count
            cards = anki_request("findNotes", query=f'deck:"{deck}"')
            count = len(cards['result']) if cards and not cards.get("error") else 0
            print(f"  {i}. {deck} ({count} cards)")
        return decks
    return []

def search_cards(query):
    """Busca cards"""
    result = anki_request("findNotes", query=query)
    if result and not result.get("error"):
        note_ids = result['result']
        if not note_ids:
            print("🔍 No se encontraron cards")
            return []
        
        # Get note info
        notes = anki_request("notesInfo", notes=note_ids)
        if notes and not notes.get("error"):
            print(f"🔍 {len(note_ids)} cards encontradas:")
            for i, note in enumerate(notes['result'][:10], 1):
                front = note['fields']['Front']['value'][:60]
                print(f"  {i}. {front}...")
            return notes['result']
    return []

def get_stats():
    """Muestra estadísticas"""
    # Get collection stats
    result = anki_request("getCollectionStatsHTML")
    if result and not result.get("error"):
        print("📊 Estadísticas de Anki:")
        # Simplified stats
        decks = list_decks()
        total_cards = sum(
            len(anki_request("findNotes", query=f'deck:"{deck}"')['result'] or [])
            for deck in decks
        )
        print(f"\n💾 Total cards: {total_cards}")
        return result['result']
    return None

def main():
    if len(sys.argv) < 2:
        print("""
🧠 AnkiConnect Manager

Uso: python3 anki-connect.py <comando> [args]

Comandos:
  create <front> <back> [deck]     Crea una tarjeta
  deck <name>                      Crea un deck
  list                             Lista decks
  search <query>                  Busca cards
  delete <note_id>                Elimina card
  stats                            Muestra stats
  sync                             Sincroniza

Ejemplos:
  python3 anki-connect.py create "Capital de Francia" "París" "Geografía"
  python3 anki-connect.py deck "Ciencias"
  python3 anki-connect.py search "tag:openclaw"
        """)
        return
    
    command = sys.argv[1]
    
    if command == "create":
        if len(sys.argv) < 4:
            print("❌ Uso: create <front> <back> [deck]")
            return
        create_card(sys.argv[2], sys.argv[3], sys.argv[4] if len(sys.argv) > 4 else "Default")
    
    elif command == "deck":
        if len(sys.argv) < 3:
            print("❌ Uso: deck <name>")
            return
        create_deck(sys.argv[2])
    
    elif command == "list":
        list_decks()
    
    elif command == "search":
        if len(sys.argv) < 3:
            print("❌ Uso: search <query>")
            return
        search_cards(sys.argv[2])
    
    elif command == "delete":
        if len(sys.argv) < 3:
            print("❌ Uso: delete <note_id>")
            return
        delete_card(int(sys.argv[2]))
    
    elif command == "stats":
        get_stats()
    
    elif command == "sync":
        sync()
    
    else:
        print(f"❌ Comando desconocido: {command}")

if __name__ == "__main__":
    main()
