import unittest

from models.bank_sampah import BankSampah
from models.jenis_sampah import SampahPlastik, SampahKertas, SampahLogam
from models.penyetor import Penyetor
from services.layanan_setoran import LayananSetoran
from utils.format import format_poin


class TestBankSampah(unittest.TestCase):
    def setUp(self):
        self.bank = BankSampah("Test")
        self.bank.tambah_penyetor(Penyetor("24001", "Dimas"))
        self.layanan = LayananSetoran(self.bank)

    def test_poin_per_jenis(self):
        self.assertEqual(SampahPlastik(2).hitung_poin(), 20)
        self.assertEqual(SampahKertas(2).hitung_poin(), 10)
        self.assertEqual(SampahLogam(2).hitung_poin(), 40)

    def test_berat_tidak_valid(self):
        with self.assertRaises(ValueError):
            SampahPlastik(0)

    def test_nim_duplikat(self):
        with self.assertRaises(ValueError):
            self.bank.tambah_penyetor(Penyetor("24001", "Lain"))

    def test_catat_setoran_menambah_poin(self):
        st = self.layanan.catat_setoran("24001", [SampahPlastik(2), SampahLogam(1)])
        self.assertEqual(st.total_poin(), 40)
        self.assertEqual(self.bank.cari_penyetor("24001").total_poin, 40)

    def test_setoran_ditolak(self):
        with self.assertRaises(ValueError):
            self.layanan.catat_setoran("99999", [SampahPlastik(1)])
        with self.assertRaises(ValueError):
            self.layanan.catat_setoran("24001", [])

    def test_format_poin(self):
        self.assertEqual(format_poin(1000), "1.000 poin")


if __name__ == "__main__":
    unittest.main()