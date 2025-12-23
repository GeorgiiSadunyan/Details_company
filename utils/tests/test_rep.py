import os
import tempfile

from modules.models.supplier import Supplier
from modules.repositories import Supplier_rep_json, Supplier_rep_yaml


def test_json_repo_create_empty_file():
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
        file_path = f.name

    repo = Supplier_rep_json(file_path)
    assert repo.get_count() == 0

    os.unlink(file_path)


def test_json_repo_add_and_get_all():
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
        file_path = f.name

    repo = Supplier_rep_json(file_path)

    s1 = Supplier(name="Поставщик 1", phone="+71234567890", address="Москва")
    s2 = Supplier(name="Поставщик 2", phone="+70987654321", address="СПб")

    repo.add(s1)
    repo.add(s2)

    all_suppliers = repo.get_all()
    assert len(all_suppliers) == 2
    assert all_suppliers[0].name == "Поставщик 1"
    assert all_suppliers[1].name == "Поставщик 2"

    os.unlink(file_path)


def test_json_repo_get_by_id():
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
        file_path = f.name

    repo = Supplier_rep_json(file_path)

    s = Supplier(name="Тест", phone="+7123790909", address="Город")
    repo.add(s)

    found = repo.get_by_id(1)
    assert found is not None
    assert found.name == "Тест"
    assert found.supplier_id == 1

    not_found = repo.get_by_id(999)
    assert not_found is None

    os.unlink(file_path)


def test_json_repo_replace_by_id():
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
        file_path = f.name

    repo = Supplier_rep_json(file_path)

    s = Supplier(name="Старый", phone="+7123790909", address="СтарыйГород")
    repo.add(s)

    new_s = Supplier(name="Новый", phone="+7123790909", address="НовыйГород")
    repo.replace_by_id(1, new_s)

    updated = repo.get_by_id(1)
    assert updated is not None
    assert updated.name == "Новый"
    assert updated.phone == "+7123790909"
    assert updated.address == "НовыйГород"

    os.unlink(file_path)


def test_json_repo_remove_by_id():
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
        file_path = f.name

    repo = Supplier_rep_json(file_path)

    s = Supplier(name="Для удаления", phone="+7123790909", address="Город")
    repo.add(s)

    assert repo.get_count() == 1
    repo.remove_by_id(1)
    assert repo.get_count() == 0

    os.unlink(file_path)


def test_json_repo_sort_by_field():
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
        file_path = f.name

    repo = Supplier_rep_json(file_path)

    s1 = Supplier(name="Б", phone="+7123790909", address="Город")
    s2 = Supplier(name="А", phone="+7123790909", address="Город")
    repo.add(s1)
    repo.add(s2)

    repo.sort_by_field("name")
    all_suppliers = repo.get_all()
    assert all_suppliers[0].name == "А"
    assert all_suppliers[1].name == "Б"

    os.unlink(file_path)


def test_json_repo_k_n_list():
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
        file_path = f.name

    repo = Supplier_rep_json(file_path)

    for i in range(1, 26):  # 25 поставщиков
        s = Supplier(name=f"Поставщик {i}", phone="+7123790909", address="Город")
        repo.add(s)

    # Вторые 10 (с 11 по 20)
    short_list = repo.get_k_n_short_list(k=3, n=5)
    assert len(short_list) == 10
    # assert short_list[0].name == "Поставщик 11"
    # assert short_list[-1].name == "Поставщик 20"

    os.unlink(file_path)


# === YAML ===


def test_yaml_repo_create_empty_file():
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".yaml") as f:
        file_path = f.name

    repo = Supplier_rep_yaml(file_path)
    assert repo.get_count() == 0

    os.unlink(file_path)


def test_yaml_repo_add_and_get_all():
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".yaml") as f:
        file_path = f.name

    repo = Supplier_rep_yaml(file_path)

    s1 = Supplier(name="Поставщик YAML 1", phone="+71234567890", address="Москва")
    s2 = Supplier(name="Поставщик YAML 2", phone="+70987654321", address="СПб")

    repo.add(s1)
    repo.add(s2)

    all_suppliers = repo.get_all()
    assert len(all_suppliers) == 2
    assert all_suppliers[0].name == "Поставщик YAML 1"
    assert all_suppliers[1].name == "Поставщик YAML 2"

    os.unlink(file_path)


def test_yaml_repo_get_by_id():
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".yaml") as f:
        file_path = f.name

    repo = Supplier_rep_yaml(file_path)

    s = Supplier(name="YAML Тест", phone="+7123790909", address="Город")
    repo.add(s)

    found = repo.get_by_id(1)
    assert found is not None
    assert found.name == "YAML Тест"
    assert found.supplier_id == 1

    not_found = repo.get_by_id(999)
    assert not_found is None

    os.unlink(file_path)


def test_yaml_repo_replace_by_id():
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".yaml") as f:
        file_path = f.name

    repo = Supplier_rep_yaml(file_path)

    s = Supplier(name="YAML Старый", phone="+7123790909", address="СтарыйГород")
    repo.add(s)

    new_s = Supplier(name="YAML Новый", phone="+7123790909", address="НовыйГород")
    repo.replace_by_id(1, new_s)

    updated = repo.get_by_id(1)
    assert updated is not None
    assert updated.name == "YAML Новый"
    assert updated.phone == "+7123790909"
    assert updated.address == "НовыйГород"

    os.unlink(file_path)


def test_yaml_repo_remove_by_id():
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".yaml") as f:
        file_path = f.name

    repo = Supplier_rep_yaml(file_path)

    s = Supplier(name="YAML Для удаления", phone="+7123790909", address="Город")
    repo.add(s)

    assert repo.get_count() == 1
    repo.remove_by_id(1)
    assert repo.get_count() == 0

    os.unlink(file_path)


def test_yaml_repo_sort_by_field():
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".yaml") as f:
        file_path = f.name

    repo = Supplier_rep_yaml(file_path)

    s1 = Supplier(name="YAML Б", phone="+7123790909", address="Город")
    s2 = Supplier(name="YAML А", phone="+7123790909", address="Город")
    repo.add(s1)
    repo.add(s2)

    repo.sort_by_field("name")
    all_suppliers = repo.get_all()
    assert all_suppliers[0].name == "YAML А"
    assert all_suppliers[1].name == "YAML Б"

    os.unlink(file_path)


def test_yaml_repo_k_n_list():
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".yaml") as f:
        file_path = f.name

    repo = Supplier_rep_yaml(file_path)

    for i in range(1, 26):  # 25 поставщиков
        s = Supplier(name=f"YAML Поставщик {i}", phone="+7123790909", address="Город")
        repo.add(s)

    # Вторые 10 (с 11 по 20)
    short_list = repo.get_k_n_short_list(k=2, n=10)
    assert len(short_list) == 10
    assert short_list[0].name == "YAML Поставщик 11"
    assert short_list[-1].name == "YAML Поставщик 20"

    os.unlink(file_path)


# === Тесты на ошибки ===


def test_json_repo_invalid_id_error():
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".json") as f:
        file_path = f.name

    repo = Supplier_rep_json(file_path)

    s = Supplier(name="Тест", phone="+7123790909", address="Город")
    repo.add(s)

    # Попытка заменить несуществующий ID
    new_s = Supplier(name="Новый", phone="+7123790909", address="Город")
    try:
        repo.replace_by_id(999, new_s)
        assert False, "Ожидалась ошибка"
    except ValueError:
        pass

    # Попытка удалить несуществующий ID
    try:
        repo.remove_by_id(999)
        assert False, "Ожидалась ошибка"
    except ValueError:
        pass

    os.unlink(file_path)


def test_yaml_repo_invalid_id_error():
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".yaml") as f:
        file_path = f.name

    repo = Supplier_rep_yaml(file_path)

    s = Supplier(name="YAML Тест", phone="+7123790909", address="Город")
    repo.add(s)

    # Попытка заменить несуществующий ID
    new_s = Supplier(name="YAML Новый", phone="+7123790909", address="Город")
    try:
        repo.replace_by_id(999, new_s)
        assert False, "Ожидалась ошибка"
    except ValueError:
        pass

    # Попытка удалить несуществующий ID
    try:
        repo.remove_by_id(999)
        assert False, "Ожидалась ошибка"
    except ValueError:
        pass

    os.unlink(file_path)
