"""
Тесты для классов Detail, DetailMini и DetailBase
"""

from decimal import Decimal

import pytest

from modules.models.detail import Detail
from modules.models.detail_mini import DetailMini

# ============ Тесты для DetailMini ============


def test_detail_mini_creation_with_args():
    """Тест создания DetailMini с позиционными аргументами"""
    detail = DetailMini("FLT-001", "Фильтр масляный")
    assert detail.article == "FLT-001"
    assert detail.name == "Фильтр масляный"


def test_detail_mini_creation_from_dict():
    """Тест создания DetailMini из словаря"""
    data = {"article": "BRK-045", "name": "Тормозные колодки"}
    detail = DetailMini(data)
    assert detail.article == "BRK-045"
    assert detail.name == "Тормозные колодки"


def test_detail_mini_creation_from_string():
    """Тест создания DetailMini из CSV-строки"""
    detail = DetailMini("SPK-123, Свечи зажигания")
    assert detail.article == "SPK-123"
    assert detail.name == "Свечи зажигания"


def test_detail_mini_creation_from_kwargs():
    """Тест создания DetailMini с именованными аргументами"""
    detail = DetailMini(article="OIL-5W40", name="Масло моторное 5W-40")
    assert detail.article == "OIL-5W40"
    assert detail.name == "Масло моторное 5W-40"


def test_detail_mini_str_representation():
    """Тест строкового представления"""
    detail = DetailMini("AIR-089", "Воздушный фильтр")
    assert str(detail) == "Деталь: Воздушный фильтр (артикул: AIR-089)"


def test_detail_mini_to_dict():
    """Тест преобразования в словарь"""
    detail = DetailMini("WIP-007", "Щетки стеклоочистителя")
    result = detail.to_dict()
    assert result == {"article": "WIP-007", "name": "Щетки стеклоочистителя"}


def test_detail_mini_equality():
    """Тест сравнения объектов"""
    detail1 = DetailMini("BAT-60AH", "Аккумулятор 60Ah")
    detail2 = DetailMini("BAT-60AH", "Аккумулятор 60Ah")
    detail3 = DetailMini("BAT-75AH", "Аккумулятор 75Ah")

    assert detail1 == detail2
    assert detail1 != detail3


def test_detail_mini_invalid_article():
    """Тест валидации некорректного артикула"""
    with pytest.raises(ValueError, match="Некорректный артикул"):
        DetailMini("", "Фильтр")  # Пустой артикул

    with pytest.raises(ValueError, match="Некорректный артикул"):
        DetailMini("FLT@001", "Фильтр")  # Недопустимые символы


def test_detail_mini_invalid_name():
    """Тест валидации некорректного наименования"""
    with pytest.raises(ValueError, match="Некорректное наименование"):
        DetailMini("FLT-001", "")  # Пустое название

    with pytest.raises(ValueError, match="Некорректное наименование"):
        DetailMini("FLT-001", "A" * 101)  # Слишком длинное название


def test_detail_mini_missing_fields_dict():
    """Тест создания с отсутствующими полями в словаре"""
    with pytest.raises(ValueError, match="Отсутствует необходимое поле"):
        DetailMini({"article": "FLT-001"})  # Нет name


def test_detail_mini_missing_fields_kwargs():
    """Тест создания с отсутствующими полями в kwargs"""
    with pytest.raises(ValueError, match="Отсутствуют обязательные поля"):
        DetailMini(article="FLT-001")  # Нет name


# ============ Тесты для Detail (полная версия) ============


def test_detail_creation_with_args():
    """Тест создания Detail с позиционными аргументами"""
    detail = Detail("FLT-001", "Фильтр масляный", 500.00)
    assert detail.article == "FLT-001"
    assert detail.name == "Фильтр масляный"
    assert detail.price == Decimal("500.00")


def test_detail_creation_without_price():
    """Тест создания Detail без цены (по умолчанию 0)"""
    detail = Detail("FLT-001", "Фильтр масляный")
    assert detail.price == Decimal("0.00")


def test_detail_creation_from_dict():
    """Тест создания Detail из словаря"""
    data = {"article": "BRK-045", "name": "Тормозные колодки", "price": 1500.00}
    detail = Detail(data)
    assert detail.article == "BRK-045"
    assert detail.name == "Тормозные колодки"
    assert detail.price == Decimal("1500.00")


def test_detail_creation_from_string():
    """Тест создания Detail из CSV-строки"""
    detail = Detail("SPK-123, Свечи зажигания, 150.50")
    assert detail.article == "SPK-123"
    assert detail.name == "Свечи зажигания"
    assert detail.price == Decimal("150.50")


def test_detail_creation_from_string_without_price():
    """Тест создания Detail из CSV-строки без цены"""
    detail = Detail("AIR-089, Воздушный фильтр")
    assert detail.price == Decimal("0.00")


def test_detail_creation_from_kwargs():
    """Тест создания Detail с именованными аргументами"""
    detail = Detail(article="OIL-5W40", name="Масло моторное 5W-40", price=2500.00)
    assert detail.article == "OIL-5W40"
    assert detail.name == "Масло моторное 5W-40"
    assert detail.price == Decimal("2500.00")


def test_detail_str_representation():
    """Тест строкового представления"""
    detail = Detail("WIP-007", "Щетки стеклоочистителя", 450.00)
    assert (
        str(detail)
        == "Деталь: Щетки стеклоочистителя (артикул: WIP-007, цена: 450.00 ₽)"
    )


def test_detail_to_dict():
    """Тест преобразования в словарь"""
    detail = Detail("BAT-60AH", "Аккумулятор 60Ah", 5000.00)
    result = detail.to_dict()
    assert result == {
        "article": "BAT-60AH",
        "name": "Аккумулятор 60Ah",
        "price": 5000.00,
    }


def test_detail_to_mini():
    """Тест преобразования Detail в DetailMini"""
    detail = Detail("TIR-195-65", "Шина 195/65 R15", 3200.00)
    mini = detail.to_mini()

    assert isinstance(mini, DetailMini)
    assert mini.article == "TIR-195-65"
    assert mini.name == "Шина 195/65 R15"


def test_detail_equality():
    """Тест сравнения объектов"""
    detail1 = Detail("CLT-002", "Тормозная жидкость DOT4", 350.00)
    detail2 = Detail("CLT-002", "Тормозная жидкость DOT4", 350.00)
    detail3 = Detail("CLT-002", "Тормозная жидкость DOT4", 400.00)

    assert detail1 == detail2
    assert detail1 != detail3  # Разные цены


def test_detail_price_validation_negative():
    """Тест валидации отрицательной цены"""
    with pytest.raises(ValueError, match="Некорректная цена"):
        Detail("FLT-001", "Фильтр", -100.00)


def test_detail_price_validation_zero():
    """Тест валидации нулевой цены (разрешено для новых записей)"""
    detail = Detail("FLT-001", "Фильтр", 0.00)
    assert detail.price == Decimal("0.00")


def test_detail_price_validation_too_high():
    """Тест валидации слишком высокой цены"""
    with pytest.raises(ValueError, match="Некорректная цена"):
        Detail("FLT-001", "Фильтр", 1_000_000.00)


def test_detail_price_validation_too_many_decimals():
    """Тест валидации цены с более чем 2 знаками после запятой"""
    with pytest.raises(ValueError, match="Некорректная цена"):
        Detail("FLT-001", "Фильтр", 123.456)


def test_detail_price_from_string():
    """Тест установки цены из строки"""
    detail = Detail("FLT-001", "Фильтр", "500.50")
    assert detail.price == Decimal("500.50")


def test_detail_price_from_int():
    """Тест установки цены из целого числа"""
    detail = Detail("FLT-001", "Фильтр", 500)
    assert detail.price == Decimal("500.00")


def test_detail_price_invalid_string():
    """Тест установки некорректной цены из строки"""
    with pytest.raises(ValueError):
        Detail("FLT-001", "Фильтр", "abc")


def test_detail_missing_required_fields():
    """Тест создания с отсутствующими обязательными полями"""
    with pytest.raises(ValueError, match="Отсутствуют обязательные поля"):
        Detail(article="FLT-001", name="Фильтр")  # Нет price


def test_detail_article_with_numbers_only():
    """Тест артикула только из цифр"""
    detail = Detail("123456", "Фильтр", 500.00)
    assert detail.article == "123456"


def test_detail_article_with_hyphen():
    """Тест артикула с дефисом"""
    detail = Detail("FLT-001-X", "Фильтр", 500.00)
    assert detail.article == "FLT-001-X"


def test_detail_name_with_parentheses():
    """Тест названия со скобками"""
    detail = Detail("OIL-5W40", "Масло моторное (синтетика)", 2500.00)
    assert detail.name == "Масло моторное (синтетика)"


def test_detail_name_cyrillic():
    """Тест названия на кириллице"""
    detail = Detail("FLT-001", "Фильтр масляный для двигателя", 500.00)
    assert detail.name == "Фильтр масляный для двигателя"


def test_detail_name_mixed_languages():
    """Тест названия на смешанных языках"""
    detail = Detail("OIL-5W40", "Oil Filter Масляный Фильтр", 500.00)
    assert detail.name == "Oil Filter Масляный Фильтр"


# ============ Граничные случаи ============


def test_detail_article_max_length():
    """Тест артикула максимальной длины (50 символов)"""
    long_article = "A" * 50
    detail = Detail(long_article, "Фильтр", 500.00)
    assert detail.article == long_article


def test_detail_article_too_long():
    """Тест артикула, превышающего максимальную длину"""
    with pytest.raises(ValueError, match="Некорректный артикул"):
        Detail("A" * 51, "Фильтр", 500.00)


def test_detail_name_max_length():
    """Тест названия максимальной длины (100 символов)"""
    long_name = "А" * 100
    detail = Detail("FLT-001", long_name, 500.00)
    assert detail.name == long_name


def test_detail_name_too_long():
    """Тест названия, превышающего максимальную длину"""
    with pytest.raises(ValueError, match="Некорректное наименование"):
        Detail("FLT-001", "А" * 101, 500.00)


def test_detail_price_min_value():
    """Тест минимальной валидной цены"""
    detail = Detail("FLT-001", "Фильтр", 0.00)
    assert detail.price == Decimal("0.00")


def test_detail_price_max_value():
    """Тест максимальной валидной цены"""
    detail = Detail("FLT-001", "Фильтр", 999999.99)
    assert detail.price == Decimal("999999.99")
