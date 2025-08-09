# Dépannage - GreenCart API

## 🔥 Problème de dépendances Python

### Symptôme :
```
ERROR: ResolutionImpossible: for help visit https://pip.pypa.io/en/latest/topics/dependency-resolution/
```

### 🛠️ Solutions (dans l'ordre) :

#### 1. **Test local des requirements**
```bash
python check_requirements.py
```

#### 2. **Versionning Python**
Le Dockerfile utilise `python:3.13-slim` qui peut avoir des problèmes de compatibilité.

**Alternative 1 - Python 3.11 stable :**
```dockerfile
FROM python:3.11-slim
```

**Alternative 2 - Python 3.12 :**
```dockerfile
FROM python:3.12-slim
```

#### 3. **Strategy de fallback**
Le Dockerfile a 4 niveaux de fallback :

1. `requirements.txt` (versions exactes)
2. `requirements-flexible.txt` (ranges flexibles) 
3. `requirements-minimal.txt` (sans versions)
4. Installation individuelle des packages core

#### 4. **Fix manuel rapide**

Si le problème persiste, utiliser cette version simplifiée du Dockerfile :

```dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=core.settings.production

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy et install en une fois
COPY requirements-minimal.txt .
RUN pip install --no-cache-dir -r requirements-minimal.txt

COPY . .

RUN python manage.py collectstatic --noinput || true

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate --noinput && python create_test_data.py && gunicorn --bind 0.0.0.0:$PORT core.wsgi:application"]
```

### 🚀 Versions testées compatibles :

```
Django==5.2.4
djangorestframework==3.15.2  
drf-spectacular==0.27.2
python-decouple==3.8
psycopg2-binary==2.9.9
gunicorn==23.0.0
```

### 📞 Support rapide

En cas de blocage, les requirements-minimal.txt devrait toujours fonctionner.