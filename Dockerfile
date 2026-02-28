# 1. Gerçek bir Python ortamı kuruyoruz
FROM python:3.10-slim

# 2. İçeride çalışma klasörü oluşturuyoruz
WORKDIR /app

# 3. Önce kütüphaneleri (requirements.txt) kopyalayıp kuruyoruz
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Projenin kalan tüm kodlarını içeri kopyalıyoruz
COPY . .

# 5. Uygulamayı 5000 portundan dışarı açıyoruz
EXPOSE 5000

# 6. Python uygulamanı başlatıyoruz 
# (Eğer ana dosyanın adı app.py veya run.py ise aşağıyı ona göre düzelt)
CMD ["python", "run.py"]