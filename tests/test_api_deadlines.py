from fastapi.testclient import TestClient
from application.main import app

client = TestClient(app)


def test_deadlines_endpoint_no_results():
    resp = client.get('/cnj/lawyer-name/deadlines', params={'lawyer_name': '___nonexistent___'})
    assert resp.status_code == 200
    data = resp.json()
    assert 'items' in data


def test_deadlines_endpoint_status_filter():
    # We can't guarantee real data, but endpoint should accept status param
    resp = client.get('/cnj/lawyer-name/deadlines', params={'lawyer_name': 'Silva', 'status': 'expired', 'page': 1, 'page_size': 5})
    assert resp.status_code == 200
    data = resp.json()
    assert 'items' in data and isinstance(data['items'], list)


def test_deadlines_endpoint_multi_status():
    resp = client.get('/cnj/lawyer-name/deadlines', params={'lawyer_name': 'Silva', 'status': 'expired,approaching', 'page': 1, 'page_size': 5})
    assert resp.status_code == 200
    data = resp.json()
    assert 'items' in data and isinstance(data['items'], list)
