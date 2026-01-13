from application.services.deadline import annotate_deadlines
from types import SimpleNamespace
from datetime import date, timedelta


def test_annotate_deadlines_basic():
    settings = SimpleNamespace(deadlines={'Intimacao': 2}, deadlines_default=10, deadlines_threshold=3)
    items = [{'data_disponibilizacao': (date.today()-timedelta(days=1)).isoformat(), 'tipoComunicacao': 'Intimação'}]
    out = annotate_deadlines(items, settings)
    assert out[0]['deadline_date'] is not None
    assert out[0]['deadline_status'] in ('approaching','ok','expired')


def test_expired_and_approaching():
    settings = SimpleNamespace(deadlines={'Intimacao': 1}, deadlines_default=10, deadlines_threshold=3)
    # publication 5 days ago, prazo 1 -> expired
    items = [{'data_disponibilizacao': (date.today()-timedelta(days=5)).isoformat(), 'tipoComunicacao': 'Intimação'}]
    out = annotate_deadlines(items, settings)
    assert out[0]['deadline_status'] == 'expired'

    # publication today, prazo 1 -> approaching (days_left 1)
    items2 = [{'data_disponibilizacao': date.today().isoformat(), 'tipoComunicacao': 'Intimação'}]
    out2 = annotate_deadlines(items2, settings)
    assert out2[0]['deadline_status'] in ('approaching','ok')
