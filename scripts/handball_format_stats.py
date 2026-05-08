#!/usr/bin/env python3
import re
from datetime import datetime

from loguru import logger

def parse_line(line):
    parts = line.strip().split()
    
    # vérifier si la ligne contient des stats (x/y pattern)
    if not re.search(r'(\d+)/(\d+)', line):
        return None
    
    # récupérer le numéro de maillot (premier élément si numérique)
    jersey = None
    name_start_idx = 1
    
    if parts[0].isdigit():
        jersey = int(parts[0])
        name_start_idx = 1
    
    # trouver le premier x/y (début des stats)
    stats_start_idx = None
    for i, p in enumerate(parts[name_start_idx:], name_start_idx):
        if "/" in p:
            stats_start_idx = i
            break
    
    if stats_start_idx is None:
        return None
    
    # les éléments avant stats_start_idx contiennent: nom + matches
    pre_stats = parts[name_start_idx:stats_start_idx]
    
    # le dernier élément numérique est le nombre de matchs
    matches_str = pre_stats[-1] if pre_stats and pre_stats[-1].isdigit() else None
    if matches_str:
        name_parts = pre_stats[:-1]
    else:
        name_parts = pre_stats
    
    name = " ".join(name_parts)
    
    # récupérer tous les champs à partir des stats
    remaining_fields = parts[stats_start_idx:]
    
    return {
        "jersey": jersey,
        "name": format_name(name) if name else "",
        "raw_name": name,
        "matches": int(matches_str) if matches_str else 0,
        "all_data": remaining_fields
    }

def format_name(name):
    if not name:
        return name
    
    parts = name.split()
    
    # cas noms composés (dos, da, de…)
    if parts[0].lower() in ["dos", "da", "de"]:
        first = parts[-1].capitalize()
        last = " ".join(parts[:-1]).title()
        return f"{first} {last}"
    
    # format classique NOM Prénom
    if len(parts) >= 2:
        first = parts[1].capitalize()
        last = parts[0].capitalize()
        return f"{first} {last}"
    
    return name

def generate_table_players(data):
    logger.info(f"generate_table_players")
    if not data:
        logger.error(f"No data")
        return "No player data available"
    
    # Extract goal/shots from 1st element of all_data (format: "19/26")
    for d in data:
        # matches already extracted in parse_line
        matches = d.get("matches", 0)
        d["matches"] = matches
        
        if d["all_data"] and len(d["all_data"]) >= 1:
            # First element: goals/shots (format: "19/26")
            match = re.search(r'(\d+)/(\d+)', d["all_data"][0])
            if match:
                d["goals"] = int(match.group(1))
                d["shots"] = int(match.group(2))
                d["percent"] = round((d["goals"] / d["shots"]) * 100) if d["shots"] > 0 else 0
            else:
                d["goals"] = 0
                d["shots"] = 0
                d["percent"] = 0
            
            # Compute goals per match
            d["goals_per_match"] = round(d["goals"] / d["matches"], 2) if d["matches"] > 0 else 0
        else:
            d["goals"] = 0
            d["shots"] = 0
            d["percent"] = 0
            d["goals_per_match"] = 0
    
    data = sorted(data, key=lambda x: x["goals"], reverse=True)
    
    # Remove players with 0 goals
    data = [d for d in data if d["goals"] > 0]
    
    max_goals = max(d["goals"] for d in data) if data else 0
    max_shots = max(d["shots"] for d in data) if data else 0
    max_matches = max(d["matches"] for d in data) if data else 0
    
    total_goals = sum(d["goals"] for d in data)
    total_shots = sum(d["shots"] for d in data)
    total_percent = round((total_goals / total_shots) * 100, 1) if total_shots > 0 else 0
    avg_goals_per_match = round(total_goals / max_matches, 2) if max_matches > 0 else 0
    
    table = []

    months_fr = {
        1: 'janvier', 2: 'février', 3: 'mars', 4: 'avril', 5: 'mai', 6: 'juin',
        7: 'juillet', 8: 'août', 9: 'septembre', 10: 'octobre', 11: 'novembre', 12: 'décembre'
    }
    today = datetime.now()
    current_date = f"{today.day} {months_fr[today.month]} {today.year}"
    
    table.append('{| class="wikitable" style="text-align:center"')
    table.append(f"|+ Buteurs<ref name=\"stats\">{{{{Lien web |langue=en |format=pdf |url=  |titre= - Statistiques cumulées |site= |date= |consulté le= {current_date}}}}}</ref>")
    table.append('! scope=col| Rang')
    table.append('! scope=col| Joueur')
    table.append('! scope=col| Buts')
    table.append('! scope=col| Tirs')
    table.append('! scope=col| {{abréviation|%|Pourcentage de réussite}}')
    table.append('! scope=col| Matchs')
    table.append('! scope=col| {{abréviation|Moy.|Moyenne de but par match}}')
    
    for i, d in enumerate(data, 1):
        goals = f"'''{d['goals']}'''" if d["goals"] == max_goals else d["goals"]
        shots = f"'''{d['shots']}'''" if d["shots"] == max_shots else d["shots"]
        matches = f"'''{d['matches']}'''" if d["matches"] == max_matches else d["matches"]
        
        if i == 1:
            table.append('|- bgcolor={{Sport couleur|meilleur buteur}}')
        else:
            table.append('|-')
        table.append(f"| {i} ||align=\"left\"| {{{{Lien|{d['name']}}}}} || {goals} || {shots} || {d['percent']} % || {matches} || {d['goals_per_match']}")
    
    table.append('|-class="sortbottom" style="background-color: #e6e6e6;font-weight: bold;"')
    table.append(f"| colspan=2| Total || {total_goals} || {total_shots} || {total_percent} % || {max_matches} || {avg_goals_per_match}")
    table.append('|}')
    
    return "\n".join(table)

def generate_table_goalkeepers(data):
    logger.info(f"generate_table_goalkeepers")
    if not data:
        logger.error(f"No data")
        return "No goalkeeper data available"
    
    # Extract saves/shots from first element of all_data (format: "35/114")
    for d in data:
        if d["all_data"]:
            match = re.search(r'(\d+)/(\d+)', d["all_data"][0])
            if match:
                d["saves"] = int(match.group(1))
                d["shots"] = int(match.group(2))
                d["percent"] = round((d["saves"] / d["shots"]) * 100)
            else:
                d["saves"] = 0
                d["shots"] = 0
                d["percent"] = 0
        else:
            d["saves"] = 0
            d["shots"] = 0
            d["percent"] = 0
    
    data = sorted(data, key=lambda x: x["saves"], reverse=True)
    
    max_saves = max(d["saves"] for d in data)
    max_shots = max(d["shots"] for d in data)
    
    total_saves = sum(d["saves"] for d in data)
    total_shots = sum(d["shots"] for d in data)
    total_percent = round((total_saves / total_shots) * 100, 1)
    
    table = []
    
    table.append('{| class="wikitable" style="text-align:center"')
    table.append('|+ Gardiens de but<ref name="stats"/>')
    table.append('! scope=col| Rang')
    table.append('! scope=col| Joueur')
    table.append('! scope=col| Arrêts')
    table.append('! scope=col| Tirs')
    table.append('! scope=col| {{abréviation|%|Pourcentage d\'arrêts}}')
    
    for i, d in enumerate(data, 1):
        saves = f"'''{d['saves']}'''" if d["saves"] == max_saves else d["saves"]
        shots = f"'''{d['shots']}'''" if d["shots"] == max_shots else d["shots"]
        
        table.append('|-')
        # TODO check if player page exixts
        table.append(f"| {i} ||align=\"left\"| {{{{Lien|{d['name']}}}}} || {saves} || {shots} || {d['percent']} %")
    
    table.append('|-class="sortbottom" style="background-color: #e6e6e6;font-weight: bold;"')
    table.append(f"| colspan=2| Total || {total_saves} || {total_shots} || {total_percent} %")
    table.append('|}')
    
    return "\n".join(table)


# ===== UTILISATION =====
file_path = "scripts/handball_format_stats.txt"

data = {
    "players": [],
    "goalkeepers": []
}
index = ''

logger.info(f"OPEN file {file_path}")
with open(file_path, "r", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if line:  # ignorer lignes vides
            if line.startswith('Players'):
                # in players table
                index = 'players'
                logger.info(f"EXTRACT {index}")
            elif line.startswith('Goalkeepers'):
                # in goalkeepers table
                index = 'goalkeepers'
                logger.info(f"EXTRACT {index}")
            elif 'Totals' in line or 'Bench' in line:
                # skip totals and bench rows
                logger.info(f"SKIP {line[:50]}")
            else:
                parsed = parse_line(line)
                if parsed and index:
                    data[index].append(parsed)


wiki_table_players = generate_table_players(data["players"])
wiki_table_goalkeepers = generate_table_goalkeepers(data["goalkeepers"])

# optionnel : sauvegarder dans un fichier
file_path = "scripts/handball_format_stats.res.txt"
logger.info(f"WRITE file {file_path}")
with open(file_path, "w", encoding="utf-8") as f:
    f.write('== Statistiques ==\n')
    f.write('=== Buteurs ===\n')
    f.write(wiki_table_players)
    f.write('\n')
    f.write('=== Gardiens de but ===\n')
    f.write(wiki_table_goalkeepers)
    f.write('\n')