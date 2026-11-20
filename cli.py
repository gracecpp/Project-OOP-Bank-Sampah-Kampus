from models.jenis_sampah import JENIS_SAMPAH
from models.penyetor import Penyetor
from utils.format import format_poin

GARIS = "=" * 44


def baca_teks(prompt):
    while True:
        nilai = input(prompt).strip()
        if nilai:
            return nilai
        print("  ! Input tidak boleh kosong.")


def baca_berat(prompt):
    while True:
        mentah = input(prompt).strip().replace(",", ".")
        try:
            berat = float(mentah)
        except ValueError:
            print("  ! Masukkan angka, contoh: 2 atau 1.5")
            continue
        if berat <= 0:
            print("  ! Berat harus lebih dari nol.")
            continue
        return berat


def baca_pilihan(prompt, jumlah):
    """Minta angka 0..jumlah, ulangi sampai valid."""
    while True:
        mentah = input(prompt).strip()
        if mentah.isdigit() and 0 <= int(mentah) <= jumlah:
            return int(mentah)
        print(f"  ! Pilih angka 0 sampai {jumlah}.")


def konfirmasi(prompt):
    while True:
        jawab = input(prompt + " (y/n): ").strip().lower()
        if jawab in ("y", "n"):
            return jawab == "y"
        print("  ! Ketik y atau n.")


class MenuBankSampah:
    def __init__(self, bank, layanan):
        self.bank = bank
        self.layanan = layanan

    def jalankan(self):
        aksi = {
            1: self.daftar_penyetor,
            2: self.catat_setoran,
            3: self.lihat_penyetor,
            4: self.lihat_riwayat,
        }
        while True:
            print(f"{self.bank.nama.upper()}")
            print("  1. Daftarkan penyetor baru")
            print("  2. Catat setoran sampah")
            print("  3. Lihat daftar penyetor & poin")
            print("  4. Lihat riwayat setoran")
            print("  0. Keluar")
            pilihan = baca_pilihan("Pilih menu: ", 4)
            if pilihan == 0:
                print("Terima kasih!")
                return
            try:
                aksi[pilihan]()
            except ValueError as e:
                print(f"  ! Gagal: {e}")


    def daftar_penyetor(self):
        print("\n-- Daftar Penyetor Baru --")
        nim = baca_teks("NIM  : ")
        nama = baca_teks("Nama : ")
        self.bank.tambah_penyetor(Penyetor(nim, nama))
        print(f"  Penyetor {nama} ({nim}) berhasil didaftarkan.")

    def catat_setoran(self):
        print("\n-- Catat Setoran --")
        if not self.bank.daftar_penyetor:
            print("  Belum ada penyetor. Daftarkan dulu lewat menu 1.")
            return

        penyetor = self._pilih_penyetor()
        if penyetor is None:
            return
        print(f"  Penyetor: {penyetor.nama}")

        daftar_sampah = self._input_sampah()
        if not daftar_sampah:
            print("  Setoran dibatalkan (tidak ada sampah).")
            return

        total = sum(s.hitung_poin() for s in daftar_sampah)
        print("\n  Ringkasan:")
        for s in daftar_sampah:
            print(f"   - {s}")
        print(f"  Total: {format_poin(total)}")

        if not konfirmasi("Simpan setoran ini?"):
            print("  Setoran dibatalkan.")
            return

        setoran = self.layanan.catat_setoran(penyetor.nim, daftar_sampah)
        print(f"  Tersimpan! Setoran #{setoran.nomor} | "
              f"Poin {penyetor.nama} sekarang: {format_poin(penyetor.total_poin)}")

    def lihat_penyetor(self):
        print("\n-- Daftar Penyetor --")
        if not self.bank.daftar_penyetor:
            print("  (kosong)")
            return
        for p in self.bank.daftar_penyetor:
            print(f"  {p.nim} | {p.nama} | {format_poin(p.total_poin)}")

    def lihat_riwayat(self):
        print("\n-- Riwayat Setoran --")
        if not self.bank.daftar_setoran:
            print("  (belum ada setoran)")
            return
        for st in self.bank.daftar_setoran:
            print(f"  #{st.nomor} {st.penyetor.nama} ({st.penyetor.nim}) "
                  f"- {format_poin(st.total_poin())}")
            for item in st.items:
                print(f"      * {item}")


    def _pilih_penyetor(self):
        while True:
            nim = input("NIM penyetor (kosong = batal): ").strip()
            if not nim:
                return None
            penyetor = self.bank.cari_penyetor(nim)
            if penyetor:
                return penyetor
            print("  ! NIM tidak ditemukan.")

    def _input_sampah(self):
        jenis = list(JENIS_SAMPAH.items())
        hasil = []
        while True:
            print("\n  Jenis sampah:")
            for i, (nama, kelas) in enumerate(jenis, 1):
                print(f"   {i}. {nama} ({kelas.POIN_PER_KG} poin/kg)")
            print("   0. Selesai")
            pilihan = baca_pilihan("Pilih jenis: ", len(jenis))
            if pilihan == 0:
                return hasil
            nama, kelas = jenis[pilihan - 1]
            berat = baca_berat(f"Berat {nama} (kg): ")
            hasil.append(kelas(berat))
            print(f"  + {hasil[-1]}")