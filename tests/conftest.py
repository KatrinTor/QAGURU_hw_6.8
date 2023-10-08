import pytest
from models import Product, Cart


@pytest.fixture(scope='function', autouse=False)
def product():
    return Product("book", 100, "This is a book", 1000)


@pytest.fixture(scope='function', autouse=False)
def another_product():
    return Product("pen", 5.25, "This is a pen", 200)


@pytest.fixture(scope='function', autouse=False)
def cart():
    return Cart()
