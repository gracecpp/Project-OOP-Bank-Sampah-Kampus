from models.bank_sampah import BankSampah
from services.layanan_setoran import LayananSetoran
from ui.cli import MenuBankSampah


def main():
    bank = BankSampah("Bank Sampah Kampus")
    layanan = LayananSetoran(bank)
    MenuBankSampah(bank, layanan).jalankan()


if __name__ == "__main__":
    main()