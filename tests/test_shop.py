import pytest


class TestProducts:

    def test_product_check_quantity(self, product):
        # TODO напишите проверки на метод check_quantity
        assert product.check_quantity(product.quantity - 1) is True
        assert product.check_quantity(product.quantity) is True
        assert product.check_quantity(product.quantity + 1) is False

    def test_product_buy(self, product):
        # TODO напишите проверки на метод buy
        initial_quantity = product.quantity
        product.buy(1)
        assert product.quantity == initial_quantity - 1

        product.buy(product.quantity)
        assert product.quantity == 0

    def test_product_buy_more_than_available(self, product):
        with pytest.raises(ValueError) as exc:
            product.buy(product.quantity + 1)
        assert exc.typename == 'ValueError'
        assert str(exc.value) == f'Недостаточное количество товара ' \
                                 f'{product.name} в наличии'


class TestCart:

    def test_add_product_default_buy_count(self, cart, product):
        cart.add_product(product)
        assert cart.products == {product: 1}

    def test_add_product_custom_buy_count(self, cart, product):
        cart.add_product(product, buy_count=5)
        assert cart.products == {product: 5}

    def test_add_product_increase_buy_count(self, cart, product):
        cart.add_product(product, buy_count=3)
        cart.add_product(product, buy_count=7)
        assert cart.products == {product: 10}

    def test_remove_product_without_remove_count(self, cart, product):
        cart.add_product(product, buy_count=8)
        cart.remove_product(product)
        assert cart.products == {}

    def test_remove_product_less_than_buy_count(self, cart, product):
        cart.add_product(product, buy_count=15)
        cart.remove_product(product, remove_count=6)
        assert cart.products == {product: 9}

    def test_remove_product_equals_buy_count(self, cart, product):
        cart.add_product(product, buy_count=10)
        cart.remove_product(product, remove_count=10)
        assert cart.products == {}

    def test_remove_product_more_than_buy_count(self, cart, product):
        cart.add_product(product, buy_count=10)
        cart.remove_product(product, remove_count=20)
        assert cart.products == {}

    def test_clear(self, cart, product):
        cart.add_product(product, buy_count=1)
        cart.clear()
        assert cart.products == {}

    def test_get_total_price(self, cart, product, another_product):
        books_to_buy = 3
        pens_to_buy = 2
        cart.add_product(product, buy_count=books_to_buy)
        cart.add_product(another_product, buy_count=pens_to_buy)
        assert cart.get_total_price() == (product.price * books_to_buy) + \
               (another_product.price * pens_to_buy)

    def test_buy_products_less_than_available(self, cart, product):
        cart.add_product(product, buy_count=product.quantity - 1)
        cart.buy()
        assert cart.products == {}
        assert product.quantity == 1

    def test_buy_products_all_available(self, cart, product):
        cart.add_product(product, buy_count=product.quantity)
        cart.buy()
        assert cart.products == {}
        assert product.quantity == 0

    def test_buy_products_more_than_available(self, cart, product):
        initial_product_quantity = product.quantity
        cart.add_product(product, buy_count=product.quantity + 1)
        with pytest.raises(ValueError) as exc:
            cart.buy()
        assert exc.typename == 'ValueError'
        assert str(exc.value) == f'Недостаточное количество товара ' \
                                 f'{product.name} в наличии'
        assert cart.products == {product: product.quantity + 1}
        assert product.quantity == initial_product_quantity
