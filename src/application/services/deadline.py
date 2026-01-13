from datetime import datetime, date, timedelta
from typing import List, Dict, Any
import re
import unicodedata

DATE_FORMATS = ["%Y-%m-%d", "%d/%m/%Y"]


def _parse_date(s: str) -> date:
    if not s or not isinstance(s, str):
        raise ValueError("Invalid date")
    s = s.strip()
    for fmt in DATE_FORMATS:
        try:
            return datetime.strptime(s, fmt).date()
        except Exception:
            continue
    # If contains only numbers like YYYYMMDD try extracting
    m = re.search(r"(\d{4})-(\d{2})-(\d{2})", s)
    if m:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    raise ValueError(f"Unknown date format: {s}")


def _normalize_type(t: str) -> str:
    if not t:
        return ""
    # remove accents and non-alphanumeric
    t = unicodedata.normalize('NFKD', t)
    t = ''.join(c for c in t if not unicodedata.combining(c))
    t = re.sub(r'[^A-Za-z0-9]', '', t)
    return t


def annotate_deadlines(items: List[Dict[str, Any]], settings) -> List[Dict[str, Any]]:
    """Annotate items with deadline_date (ISO), days_left (int) and deadline_status"""
    out = []
    today = date.today()
    for it in items:
        # extract publication date from known fields
        pub = None
        for fld in ('data_disponibilizacao', 'datadisponibilizacao', 'dataPublicacao', 'data', 'publicationDate'):
            if fld in it and it.get(fld):
                try:
                    pub = _parse_date(str(it.get(fld)))
                    break
                except Exception:
                    continue
        if not pub:
            # Can't compute deadline; leave fields null
            it['deadline_date'] = None
            it['days_left'] = None
            it['deadline_status'] = 'unknown'
            out.append(it)
            continue

        tipo = it.get('tipoComunicacao') or it.get('tipo_comunicacao') or ''
        key = _normalize_type(tipo) or ''
        # Try match per-type in settings.deadlines (keys normalized similarly)
        per_type = {k if isinstance(k,str) else str(k): v for k, v in getattr(settings, 'deadlines', {}).items()}
        # Normalize keys for matching
        per_type_norm = { _normalize_type(k): v for k, v in per_type.items() }
        prazo = per_type_norm.get(key, getattr(settings, 'deadlines_default', 10))

        deadline_dt = pub + timedelta(days=int(prazo))
        days_left = (deadline_dt - today).days
        threshold = getattr(settings, 'deadlines_threshold', 3)
        status = 'ok'
        if days_left < 0:
            status = 'expired'
        elif days_left <= threshold:
            status = 'approaching'

        it['deadline_date'] = deadline_dt.isoformat()
        it['days_left'] = days_left
        it['deadline_status'] = status
        out.append(it)
    return out
