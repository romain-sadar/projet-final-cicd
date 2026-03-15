def test_create_note(client):

    response = client.post(
        "/notes",
        json={"title": "Test note", "content": "Test content"},
    )

    assert response.status_code == 201
    assert response.json()["title"] == "Test note"


def test_get_notes(client):

    client.post("/notes", json={"title": "note", "content": "content"})

    response = client.get("/notes")

    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_update_note(client):

    note = client.post("/notes", json={"title": "old", "content": "old"}).json()

    response = client.put(
        f"/notes/{note['id']}", json={"title": "new", "content": "new"}
    )

    assert response.status_code == 200
    assert response.json()["title"] == "new"


def test_delete_note(client):

    note = client.post("/notes", json={"title": "test", "content": "test"}).json()

    response = client.delete(f"/notes/{note['id']}")

    assert response.status_code == 200


def test_create_note_missing_field(client):

    response = client.post("/notes", json={"title": "missing content"})

    assert response.status_code == 422 # FastAPI returns 422


def test_get_invalid_id(client):

    response = client.get("/notes/999999")

    assert response.status_code == 404
