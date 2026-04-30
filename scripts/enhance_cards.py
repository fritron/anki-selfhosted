#!/usr/bin/env python3
"""
Script para mejorar tarjetas superficiales de Anki
Añade contexto, datos específicos y explicaciones educativas
"""

import json
import urllib.request

ANKI_CONNECT_URL = "http://localhost:8765"

def anki_request(action, **params):
    payload = json.dumps({"action": action, "version": 6, "params": params}).encode('utf-8')
    req = urllib.request.Request(ANKI_CONNECT_URL, data=payload, headers={'Content-Type': 'application/json'})
    try:
        response = urllib.request.urlopen(req)
        return json.loads(response.read())
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def get_all_notes():
    """Obtiene todas las tarjetas del deck Cultura General Chile"""
    result = anki_request("findNotes", query="deck:\"Cultura General Chile::*\"")
    return result.get('result', []) if result else []

def get_notes_info(note_ids):
    """Obtiene información detallada de las tarjetas"""
    result = anki_request("notesInfo", notes=note_ids)
    return result.get('result', []) if result else []

def is_superficial(front, back):
    """Identifica si una tarjeta es superficial"""
    superficial = False
    reasons = []
    
    # Respuesta muy corta (menos de 50 chars)
    if len(back) < 50:
        superficial = True
        reasons.append("Muy corta")
    
    # Contiene términos vagos
    vague_terms = ['aproximadamente', 'uno de los', 'alrededor', 'más o menos', 'etc']
    if any(term in back.lower() for term in vague_terms):
        superficial = True
        reasons.append("Términos vagos")
    
    # Solo nombre sin explicación
    words = back.split()
    if len(words) < 5 and not any(w in back.lower() for w in ['es', 'son', 'fue', 'fueron', 'hace', 'funciona']):
        superficial = True
        reasons.append("Solo nombre sin contexto")
    
    return superficial, reasons

def enhance_card(note_id, front, back, deck):
    """Mejora una tarjeta con información adicional"""
    
    # Diccionario de mejoras por patrón
    enhancements = {
        "PIB": "El PIB de Chile es de aproximadamente US$300.000 millones (2024), con un PIB per cápita de US$15.000. Esto lo posiciona como la economía más desarrollada de Sudamérica junto a Uruguay. El crecimiento histórico se debe a la minería (especialmente cobre), exportaciones agrícolas (uvas, arándanos, cerezas), acuicultura (salmón), y servicios.",
        
        "IVU": "El IVA (Impuesto al Valor Agregado) en Chile es del 19%. Aplica a la mayoría de bienes y servicios, recaudando cerca del 40% de los ingresos fiscales. Fue creado en 1975 y es similar al VAT europeo. Alimentos básicos y medicamentos están exentos.",
        
        "IPS": "El Instituto de Previsión Social (IPS) era el sistema estatal de pensiones antes de 1981. Funcionaba por reparto: los trabajadores activos pagaban las pensiones de los jubilados. Fue reemplazado por el sistema AFP privado durante la dictadura. Hoy solo gestiona pensiones especiales y regímenes de exonerados.",
        
        "AFP": "Las AFP (Administradoras de Fondos de Pensiones) son empresas privadas que administran las pensiones desde 1981. Cada trabajador aporta ~10% de su sueldo a una cuenta individual. Existen 6 AFP: Capital, Cuprum, Habitat, Modelo, Planvital y Provida. El sistema ha sido criticado por bajas pensiones (promedio $350.000 CLP), generando el movimiento 'No más AFP' y propuestas de reforma.",
        
        "CODELCO": "CODELCO (Corporación Nacional del Cobre de Chile) es la empresa estatal minera más grande del mundo. Produce aproximadamente 10% del cobre mundial. Fue creada en 1976 durante la nacionalización de la gran minería del cobre (ley 17.450 de 1971). Aporta billones de pesos al fisco chileno anualmente.",
        
        "SII": "El Servicio de Impuestos Internos (SII) es el organismo encargado de administrar y fiscalizar los impuestos en Chile. Fue creado en 1925. Gestiona el IVA (19%), impuesto a la renta, impuesto territorial, y otros tributos. Es conocido por su sistema de facturación electrónica obligatoria.",
        
        "TLC": "Chile ha firmado tratados de libre comercio con más de 60 países, cubriendo el 95% del PIB mundial. El primer TLC fue con Canadá (1997). Los más importantes son con China (2005), Estados Unidos (2004), UE (2003), y el TPP-11 (2018). Esto ha convertido a Chile en un país muy abierto al comercio internacional.",
        
        "Fondo de Estabilización": "El Fondo de Estabilización Económica (FEE) es un fondo soberano creado en 1985 (antiguo Fondo de Cobre). Ahorra recursos extraordinarios de la minería para momentos de crisis. En 2023 superó los US$10.000 millones. Es una de las razones por las que Chile resistió bien la crisis del COVID-19.",
    }
    
    # Buscar patrones en la pregunta/respuesta
    for pattern, enhancement in enhancements.items():
        if pattern.lower() in front.lower() or pattern.lower() in back.lower():
            return enhancement
    
    # Si no hay patrón específico, agregar contexto general
    if len(back) < 30:
        return f"{back}\n\n💡 Contexto: Este es un concepto importante para entender la realidad chilena. Investiga más sobre sus orígenes, evolución y situación actual."
    
    return None

def update_note(note_id, new_back):
    """Actualiza el reverso de una tarjeta"""
    result = anki_request("updateNoteFields", note={"id": note_id, "fields": {"Back": new_back}})
    return result and not result.get("error")

def main():
    print("🔍 Analizando tarjetas superficiales...\n")
    
    # Obtener todas las tarjetas
    note_ids = get_all_notes()
    print(f"📊 Total tarjetas encontradas: {len(note_ids)}")
    
    # Obtener información detallada
    notes = get_notes_info(note_ids)
    
    superficial_count = 0
    updated_count = 0
    
    for note in notes:
        note_id = note['noteId']
        front = note['fields']['Front']['value']
        back = note['fields']['Back']['value']
        
        # Verificar si es superficial
        is_super, reasons = is_superficial(front, back)
        
        if is_super:
            superficial_count += 1
            
            # Intentar mejorar
            enhanced = enhance_card(note_id, front, back, note.get('deckName', ''))
            
            if enhanced and enhanced != back:
                if update_note(note_id, enhanced):
                    updated_count += 1
                    print(f"✅ Mejorada: {front[:50]}...")
                else:
                    print(f"❌ Error al actualizar: {front[:50]}...")
    
    print(f"\n📊 RESUMEN:")
    print(f"   Tarjetas analizadas: {len(notes)}")
    print(f"   Tarjetas superficiales: {superficial_count}")
    print(f"   Tarjetas mejoradas: {updated_count}")
    
    # Sincronizar
    print("\n🔄 Sincronizando...")
    sync_result = anki_request("sync")
    if sync_result and not sync_result.get("error"):
        print("✅ Sincronización completada")
    else:
        print("❌ Error en sincronización")

if __name__ == "__main__":
    main()
