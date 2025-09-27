from selenium.webdriver.common.by import By

from pages.base import Base


class Giohang(Base):

    chon_sanpham = (By.XPATH, "(//a[@class='line_1'][contains(text(),'[F5 x TEELAB 5TH BIRTHDAY] Áo Polo Local Brand Uni')])[1]")
    them_vaogio = (By.CSS_SELECTOR, "button.btn_add_cart.add_to_cart")

    xem_gh = (By.CSS_SELECTOR, ".cart-count.d-inline-block.px-2.mb-2")

    # Thông tin chi tiết sản phẩm
    ctsp_ten = (By.CSS_SELECTOR, "h1.title-product")
    ctsp_gia = (By.CSS_SELECTOR, ".product-price")
    ctsp_mausac = (By.CSS_SELECTOR, ".swatch[data-option-index='0'] .header .value")
    ctsp_kichthuoc = (By.CSS_SELECTOR, ".swatch[data-option-index='1'] .swatch-element input:checked")

    # Thông tin sản phẩm trong giỏ hàng
    gh_ten = (By.CSS_SELECTOR, ".product-name.d-block.font-weight-bold")
    gh_gia = (By.CSS_SELECTOR, ".item-price.p-1")
    gh_maukichthuoc = (By.CSS_SELECTOR, ".cart_name .variant.variant-title")

    def chon_sp_mua (self):
        self.click(self.chon_sanpham)

    def lay_thongtin_ctsp (self):
        ten = self.get_text(self.ctsp_ten).strip()
        gia = self.get_text(self.ctsp_gia).strip()

        try:
            mausac = self.get_text(self.ctsp_mausac).strip()
        except:
            mausac = ""

        try:
            kichthuoc = self.driver.find_element(*self.ctsp_kichthuoc).get_attribute("value").strip()
        except:
            kichthuoc = ""

        return {
            "ten": ten,
            "gia": gia,
            "mausac": mausac,
            "kichthuoc": kichthuoc
        }

    def them_giohang (self):
        self.click(self.them_vaogio)
        self.click(self.xem_gh)

    def lay_thongtin_gh (self):
        ten = self.get_text(self.gh_ten).strip()
        gia = self.get_text(self.gh_gia).strip()

        try:
            mau_kichthuoc = self.get_text(self.gh_maukichthuoc).strip()
        except:
            mau_kichthuoc = ""

        return {
            "ten": ten,
            "gia": gia,
            "mau_kichthuoc": mau_kichthuoc
        }