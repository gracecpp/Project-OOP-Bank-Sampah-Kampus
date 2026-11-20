import streamlit as st

from models.bank_sampah import BankSampah
from models.jenis_sampah import JENIS_SAMPAH
from models.penyetor import Penyetor
from services.layanan_setoran import LayananSetoran
from utils.format import format_poin

st.set_page_config(page_title="Bank Sampah Kampus", page_icon="♻️")

if "bank" not in st.session_state:
    st.session_state.bank = BankSampah("Bank Sampah Kampus")
    st.session_state.layanan = LayananSetoran(st.session_state.bank)

bank = st.session_state.bank
layanan = st.session_state.layanan

st.sidebar.title("♻️ Bank Sampah")
halaman = st.sidebar.radio(
    "Menu", ["Beranda", "Daftar Penyetor", "Catat Setoran", "Riwayat"]
)
st.sidebar.caption("Tugas MiniApps - Pemrograman Berbasis Objek")


if halaman == "Beranda":
    st.title("Beranda")
    total_poin = sum(p.total_poin for p in bank.daftar_penyetor)

    c1, c2, c3 = st.columns(3)
    c1.metric("Penyetor", len(bank.daftar_penyetor))
    c2.metric("Setoran", len(bank.daftar_setoran))
    c3.metric("Total Poin", format_poin(total_poin))

    st.divider()
    if bank.daftar_penyetor:
        st.subheader("Poin per Penyetor")
        st.bar_chart(
            [{"Nama": p.nama, "Poin": p.total_poin} for p in bank.daftar_penyetor],
            x="Nama",
            y="Poin",
        )
    else:
        st.info("Belum ada data. Mulai dari menu Daftar Penyetor.")


elif halaman == "Daftar Penyetor":
    st.title("Daftar Penyetor")

    with st.form("form_daftar", clear_on_submit=True):
        nim = st.text_input("NIM").strip()
        nama = st.text_input("Nama").strip()
        kirim = st.form_submit_button("Daftarkan", type="primary")

    if kirim:
        if not nim or not nama:
            st.error("NIM dan nama harus diisi.")
        else:
            try:
                bank.tambah_penyetor(Penyetor(nim, nama))
                st.success(f"{nama} berhasil didaftarkan.")
            except ValueError as e:
                st.error(str(e))

    st.subheader("Penyetor Terdaftar")
    if bank.daftar_penyetor:
        st.dataframe(
            [{"NIM": p.nim, "Nama": p.nama, "Total Poin": p.total_poin}
             for p in bank.daftar_penyetor],
            hide_index=True,
        )
    else:
        st.caption("Belum ada penyetor.")


elif halaman == "Catat Setoran":
    st.title("Catat Setoran")

    if not bank.daftar_penyetor:
        st.info("Daftarkan penyetor dulu di menu Daftar Penyetor.")
    else:
        with st.form("form_setoran"):
            penyetor = st.selectbox(
                "Penyetor",
                bank.daftar_penyetor,
                format_func=lambda p: f"{p.nim} - {p.nama}",
            )
            st.write("Berat sampah (kg), isi 0 jika tidak ada:")
            kolom = st.columns(len(JENIS_SAMPAH))
            berat = {}
            for col, (jenis, kelas) in zip(kolom, JENIS_SAMPAH.items()):
                berat[jenis] = col.number_input(
                    f"{jenis} ({kelas.POIN_PER_KG}/kg)", min_value=0.0, step=0.5
                )
            simpan = st.form_submit_button("Simpan Setoran", type="primary")

        if simpan:
            daftar_sampah = [JENIS_SAMPAH[j](b) for j, b in berat.items() if b > 0]
            try:
                setoran = layanan.catat_setoran(penyetor.nim, daftar_sampah)
                st.success(
                    f"Setoran #{setoran.nomor} tersimpan: "
                    f"{format_poin(setoran.total_poin())}"
                )
                st.balloons()
            except ValueError as e:
                st.error(str(e))


else:
    st.title("Riwayat Setoran")

    if not bank.daftar_setoran:
        st.info("Belum ada setoran.")
    for s in reversed(bank.daftar_setoran):
        with st.expander(f"#{s.nomor} | {s.penyetor.nama} | {format_poin(s.total_poin())}"):
            for item in s.items:
                st.write(f"- {item}")