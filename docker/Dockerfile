# Usa a imagem base Alpine
FROM alpine:latest

# Instala dependências do sistema
RUN apk add --no-cache \
    sqlite \
    python3 \
    py3-pip \
    gcc \
    musl-dev \
    libc-dev \
    libpng-dev \
    freetype-dev

# Cria e ativa um ambiente virtual
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Instala as dependências do Python no ambiente virtual
RUN pip install --no-cache-dir \
    sqlalchemy \
    numpy \
    matplotlib

# Cria o diretório de trabalho
RUN mkdir -p /swifit-orm
WORKDIR /swifit-orm

# Expõe a porta 5432 (se necessário)
EXPOSE 5432

# Define o comando padrão
CMD ["python3"]