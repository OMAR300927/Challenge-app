# =============================
# Custom Jenkins Image for DevOps Lab
# =============================
FROM jenkins/jenkins:2.554-jdk21

USER root

# -----------------------------
# 1️⃣ تثبيت الأدوات الأساسية
# -----------------------------
RUN apt-get update --allow-releaseinfo-change \
    && apt-get install -y --no-install-recommends \
        curl \
        wget \
        gnupg \
        ca-certificates \
        lsb-release \
        unzip \
        git \
    && rm -rf /var/lib/apt/lists/*

# -----------------------------
# 2️⃣ تثبيت Docker CLI فقط
# -----------------------------
RUN mkdir -p /etc/apt/keyrings \
    && curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
        https://download.docker.com/linux/debian $(lsb_release -cs) stable" \
        | tee /etc/apt/sources.list.d/docker.list > /dev/null \
    && apt-get update \
    && apt-get install -y docker-ce-cli \
    && rm -rf /var/lib/apt/lists/*

# -----------------------------
# 3️⃣ تثبيت kubectl
# -----------------------------
RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" \
    && install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl \
    && rm kubectl

# -----------------------------
# 4️⃣ تثبيت Trivy
# -----------------------------
RUN curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh \
    && mv ./bin/trivy /usr/local/bin/trivy \
    && chmod +x /usr/local/bin/trivy

# -----------------------------
# 5️⃣ تثبيت Gitleaks
# -----------------------------
RUN wget https://github.com/zricethezav/gitleaks/releases/download/v8.16.2/gitleaks_8.16.2_linux_x64.tar.gz -O gitleaks.tar.gz \
    && tar -xzf gitleaks.tar.gz \
    && mv gitleaks /usr/local/bin/ \
    && chmod +x /usr/local/bin/gitleaks \
    && rm gitleaks.tar.gz

# -----------------------------
# 6️⃣ إنشاء مجلدات للمستخدم
# -----------------------------
RUN mkdir -p /var/jenkins_home/.kube \
    && mkdir -p /var/jenkins_home/.docker

# -----------------------------
# 7️⃣ تثبيت uv (FIXED)
# -----------------------------
RUN curl -LsSf https://astral.sh/uv/install.sh | sh \
    && install -m 0755 /root/.local/bin/uv /usr/local/bin/uv \
    && install -m 0755 /root/.local/bin/uvx /usr/local/bin/uvx

# -----------------------------
# 8️⃣ الرجوع لمستخدم Jenkins
# -----------------------------
USER jenkins