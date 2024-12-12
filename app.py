import streamlit as st
from datetime import datetime, timedelta

def parse_time(time_str):
    """
    Wandelt einen Zeitstring in ein datetime.time Objekt um
    
    Args:
        time_str (str): Zeitstring im Format HH:MM oder H:MM
    
    Returns:
        datetime.time: Geparste Uhrzeit
        None: Bei ungültigem Format
    """
    try:
        # Versuche verschiedene Formate zu parsen
        time_formats = ['%H:%M', '%H.%M', '%H %M']
        for fmt in time_formats:
            try:
                return datetime.strptime(time_str, fmt).time()
            except ValueError:
                continue
        
        # Alternative Formate ohne führende Null
        time_formats = ['%H:%M', '%H.%M', '%H %M', '%k:%M', '%k.%M', '%k %M']
        for fmt in time_formats:
            try:
                return datetime.strptime(time_str, fmt).time()
            except ValueError:
                continue
        
        raise ValueError("Ungültiges Zeitformat")
    
    except ValueError:
        st.error("Bitte geben Sie die Zeit im Format HH:MM ein (z.B. 07:30 oder 9:45)")
        return None

def calculate_work_time(start_time, end_time, pause_duration=45):
    """
    Berechnet die Arbeitszeit abzüglich der Pausenzeit
    
    Args:
        start_time (datetime): Startzeit der Arbeit
        end_time (datetime): Endzeit der Arbeit
        pause_duration (int): Pausendauer in Minuten
    
    Returns:
        timedelta: Netto-Arbeitszeit
    """
    total_time = end_time - start_time
    pause = timedelta(minutes=pause_duration)
    net_work_time = total_time - pause
    return net_work_time

#Main
def main():
    st.title("Arbeitszeit Tracker")
    
    # Standardwerte für Start- und Endzeit
    default_start = datetime.now().replace(hour=7, minute=30, second=0, microsecond=0)
    default_end = datetime.now()
    
    # Eingabefelder für Start- und Endzeit als Text
    col1, col2 = st.columns(2)
    
    with col1:
        start_time_str = st.text_input(
            "Startzeit", 
            value=default_start.strftime("%H:%M"),
            placeholder="HH:MM (z.B. 07:30)"
        )
    
    with col2:
        end_time_str = st.text_input(
            "Endzeit", 
            value=default_end.strftime("%H:%M"),
            placeholder="HH:MM (z.B. 17:00)"
        )
    
    # Pausendauer mit Standardwert
    pause_duration = st.number_input(
        "Pausendauer (Minuten)", 
        min_value=0, 
        max_value=120, 
        value=45
    )
    
    # Versuche Zeitstrings zu parsen
    start_time = parse_time(start_time_str)
    end_time = parse_time(end_time_str)
    
    # Nur fortfahren, wenn beide Zeiten gültig sind
    if start_time and end_time:
        # Datum für die Berechnung kombinieren
        today = datetime.now().date()
        start_datetime = datetime.combine(today, start_time)
        end_datetime = datetime.combine(today, end_time)
        
        # Korrektur für Zeiten über Mitternacht
        if end_datetime < start_datetime:
            end_datetime += timedelta(days=1)
        
        # Arbeitszeit berechnen
        net_work_time = calculate_work_time(start_datetime, end_datetime, pause_duration)
        
        # Ergebnisse anzeigen
        st.write(f"Bruttoarbeitszeit: {end_datetime - start_datetime}")
        st.write(f"Pausendauer: {timedelta(minutes=pause_duration)}")
        st.write(f"Nettoarbeitszeit: {net_work_time}")
        
        # Stunden und Minuten separat anzeigen
        hours, remainder = divmod(net_work_time.seconds, 3600)
        minutes = remainder // 60
        st.success(f"Nettoarbeitszeit: {hours} Stunden und {minutes} Minuten")

if __name__ == "__main__":
    main()