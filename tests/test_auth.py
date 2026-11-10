from app.extensions import db
from app.models import User
from app.services.roles import ROLE_ADMIN, get_or_create_role

VALID = {
    "full_name": "Awa Dossou",
    "email": "Awa@Exemple.com",
    "phone": "+22990000000",
    "password": "motdepasse1",
    "password_confirm": "motdepasse1",
}


def register(client, **overrides):
    return client.post("/inscription", data={**VALID, **overrides}, follow_redirects=False)


def test_public_pages(client):
    assert client.get("/").status_code == 200
    assert client.get("/formations").status_code == 200
    assert client.get("/connexion").status_code == 200
    assert client.get("/inscription").status_code == 200
    assert client.get("/css/style.css").status_code == 200
    assert client.get("/js/app.js").status_code == 200


def test_register_creates_student_and_logs_in(client):
    res = register(client)
    assert res.status_code == 302 and res.location.endswith("/espace-apprenant")
    user = db.session.query(User).one()
    assert user.email == "awa@exemple.com"
    assert user.has_role("apprenant")
    assert user.password_hash != VALID["password"]
    assert client.get("/espace-apprenant").status_code == 200


def test_register_rejects_duplicates_and_bad_input(client):
    register(client)
    client.post("/deconnexion")
    assert register(client, phone="").status_code == 400  # e-mail déjà pris
    assert register(client, email="autre@exemple.com").status_code == 400  # téléphone déjà pris
    assert register(client, email="x@exemple.com", phone="", password_confirm="autre").status_code == 400
    assert register(client, email="pas-un-email", phone="").status_code == 400
    assert db.session.query(User).count() == 1


def test_login_logout(client):
    register(client)
    client.post("/deconnexion")
    assert client.get("/espace-apprenant").status_code == 302

    bad = client.post("/connexion", data={"email": "awa@exemple.com", "password": "faux"})
    assert bad.status_code == 401

    ok = client.post("/connexion", data={"email": "AWA@exemple.com", "password": VALID["password"]})
    assert ok.status_code == 302
    assert client.get("/espace-apprenant").status_code == 200

    assert client.post("/deconnexion").status_code == 302
    assert client.get("/espace-apprenant").status_code == 302


def test_login_blocks_inactive_user(client):
    register(client)
    client.post("/deconnexion")
    db.session.query(User).one().is_active = False
    db.session.commit()
    res = client.post("/connexion", data={"email": "awa@exemple.com", "password": VALID["password"]})
    assert res.status_code == 401


def test_login_redirects_only_to_local_paths(client):
    register(client)
    client.post("/deconnexion")
    creds = {"email": "awa@exemple.com", "password": VALID["password"]}
    res = client.post("/connexion?next=/formations", data=creds)
    assert res.location.endswith("/formations")
    client.post("/deconnexion")
    res = client.post("/connexion?next=//evil.example", data=creds)
    assert res.location.endswith("/espace-apprenant")


def test_protected_page_redirects_to_login(client):
    res = client.get("/espace-apprenant")
    assert res.status_code == 302 and "/connexion?next=" in res.location


def test_admin_area_requires_admin_role(client):
    assert client.get("/admin/").status_code == 302  # non connecté
    register(client)
    assert client.get("/admin/").status_code == 403  # apprenant
    user = db.session.query(User).one()
    user.roles.append(get_or_create_role(ROLE_ADMIN))
    db.session.commit()
    res = client.get("/admin/")
    assert res.status_code == 200 and b"awa@exemple.com" in res.data


def test_logout_requires_post(client):
    register(client)
    assert client.get("/deconnexion").status_code == 405
