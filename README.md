# Proyek Analisis Data: Beijing Air Quality Dashboard 🌬️

**Live Dashboard:** [Beijing Air Quality Analysis - Streamlit App](https://beijing-air-quality-analysis-fakhri.streamlit.app/)

## Deskripsi Proyek
Proyek ini merupakan *dashboard* interaktif yang dikembangkan menggunakan **Streamlit** untuk menganalisis dan memvisualisasikan data kualitas udara di Beijing. Analisis ini mencakup tren polutan udara (seperti CO, PM2.5, PM10) serta pengaruh faktor cuaca terhadap kualitas udara seiring berjalannya waktu. Proyek ini merupakan Capstone Project akhir untuk kelulusan program *coding camp*.

## Struktur Direktori
- `/dashboard`: Berisi file utama `dashboard.py` dan dataset `main_data.csv` yang digunakan untuk aplikasi Streamlit.
- `notebook.ipynb`: Jupyter Notebook yang berisi alur kerja analisis data lengkap mulai dari *Data Wrangling*, *Exploratory Data Analysis* (EDA), hingga visualisasi.
- `requirements.txt`: Daftar *library* Python yang dibutuhkan untuk menjalankan proyek ini.
- `README.md`: Informasi utama mengenai proyek dan instruksi instalasi.

## Setup Environment - Anaconda
```bash
conda create --name main-ds python=3.9
conda activate main-ds
pip install -r requirements.txt

mkdir proyek_analisis_data
cd proyek_analisis_data
pipenv install
pipenv shell
pip install -r requirements.txt

streamlit run dashboard/dashboard.py

Silakan di-*save*, bungkus folder `submission` kamu menjadi ZIP, lalu kirimkan ke portal pengumpulan tugasnya. Selamat beristirahat dan menikmati sisa perjalanan di kereta menuju Jakarta! Pekerjaan kerasmu dengan data dan *coding* hari ini sudah tuntas.
