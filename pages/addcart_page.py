from selenium.webdriver.common.by import By

from pages.base import Base


class Cart(Base):

    product_select = (By.CSS_SELECTOR, ".product-thumbnail.position-relative")
    add_cart = (By.CSS_SELECTOR, "button.btn_add_cart.add_to_cart")

    see_cart = (By.CSS_SELECTOR, ".cart-count.d-inline-block.px-2.mb-2")

    # Thông tin chi tiết sản phẩm
    details_name = (By.CSS_SELECTOR, "h1.title-product")
    details_price = (By.CSS_SELECTOR, ".product-price")
    details_color = (By.CSS_SELECTOR, ".swatch[data-option-index='0'] .header .value")
    details_size = (By.CSS_SELECTOR, ".swatch[data-option-index='1'] .swatch-element input:checked")

    # Thông tin sản phẩm trong giỏ hàng
    cart_name = (By.CSS_SELECTOR, ".product-name.d-block.font-weight-bold")
    cart_price = (By.CSS_SELECTOR, ".item-price.p-1")
    cart_color_size = (By.CSS_SELECTOR, ".cart_name .variant.variant-title")
    cart_quantity = (By.NAME, "updates[]")

    # Tổng tiền
    total_amount = (By.CSS_SELECTOR, "div[class='cart-footer'] div[class='cart_total total-price text-right font-weight-bold']")

    def select_product_buy(self):
        self.click(self.product_select)

    def get_information_details(self):
        name = self.get_text(self.details_name).strip()
        price = self.get_text(self.details_price).strip()

        try:
            color = self.get_text(self.details_color).strip()
        except:
            color = ""

        try:
            size = self.driver.find_element(*self.details_size).get_attribute("value").strip()
        except:
            size = ""

        return {"name": name, "price": price, "color": color, "size": size}

    def add_product_cart(self):
        self.click(self.add_cart)
        self.click(self.see_cart)

    def get_information_cart(self):
        name = self.get_text(self.cart_name).strip()
        price = self.get_text(self.cart_price).strip()

        try:
            color_size = self.get_text(self.cart_color_size).strip()
        except:
            color_size = ""

        quantity_element = self.driver.find_element(*self.cart_quantity)
        quantity = int(quantity_element.get_attribute("value"))

        return {"name": name,"price": price,"color_size": color_size, "quantity": int(quantity)
        }

    def get_total_amount(self):
        total_text = self.get_text(self.total_amount)
        return int(''.join(filter(str.isdigit, total_text)))

    def calculate_total_amount(self):
        prices = self.get_elements(self.cart_price)
        quantities = self.get_elements(self.cart_quantity)
        total = 0
        for p, q in zip(prices, quantities):
            price = int(''.join(filter(str.isdigit, p.text)))
            qty = int(q.get_attribute("value"))
            total += price * qty
        return total
