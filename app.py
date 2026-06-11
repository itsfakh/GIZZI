import json
import streamlit as st
from PIL import Image
from google import genai

# ==========================
# KONFIGURASI HALAMAN
# ==========================

st.set_page_config(
page_title="CekGizi AI",
page_icon="🥗",
layout="centered"
)

st.title("🥗 CekGizi AI")
st.caption("Deteksi kalori dan nutrisi makanan menggunakan Gemini AI")

# ==========================
# API KEY
# ==========================

try:
    api_key = st.secrets["GEMINI_API_KEY"]
except Exception:
    st.error("GEMINI_API_KEY tidak ditemukan.")
    st.stop()

client = genai.Client(api_key=api_key)

# ==========================
# INPUT FOTO
# ==========================

uploaded_file = st.file_uploader(
"Upload Foto Makanan",
type=["jpg", "jpeg", "png"]
)

if uploaded_file:

    image = Image.open(uploaded_file)

    st.image(
        image,
        caption="Foto yang diunggah",
        use_container_width=True
    )

if st.button("🔍 Analisis Nutrisi"):

    with st.spinner("Menganalisis gambar..."):

        prompt = """

Anda adalah ahli gizi profesional.

Analisis gambar makanan.

Balas HANYA dalam format JSON berikut:

{
"nama_makanan":"",
"kalori_kcal":"",
"protein_g":"",
"karbohidrat_g":"",
"lemak_g":"",
"tips":""
}

Jangan gunakan markdown.
Jangan gunakan penjelasan tambahan.
"""

        try:

            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=[
                    prompt,
                    image
                ]
            )

            result_text = response.text

            result_text = result_text.replace(
                "```json",
                ""
            ).replace(
                "```",
                ""
            ).strip()

            data = json.loads(result_text)

            st.success("Analisis berhasil!")

            st.subheader(
                f"🍽️ {data['nama_makanan']}"
            )

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "🔥 Kalori",
                    data["kalori_kcal"]
                )

                st.metric(
                    "💪 Protein",
                    data["protein_g"]
                )

            with col2:
                st.metric(
                    "🍚 Karbohidrat",
                    data["karbohidrat_g"]
                )

                st.metric(
                    "🥑 Lemak",
                    data["lemak_g"]
                )

            st.info(
                f"💡 {data['tips']}"
            )

        except Exception as e:

            error_text = str(e)

            if "429" in error_text:
                st.warning(
                    "⚠️ Kuota Gemini habis. Silakan coba lagi nanti atau gunakan API key lain."
                )
            else:
                st.error(
                    f"Gagal menganalisis gambar: {e}"
                )
