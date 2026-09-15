# WebPanel — Tek JAR Mimari Tasarım Belgesi

> Minecraft sunucusuna tek bir `.jar` atılarak çalışan, hem Bukkit/Paper eklentisi hem gömülü web paneli sunan sistem.

---

## Genel Bakış

Sistem, Paper sunucusunun JVM'i içinde iki katman olarak çalışır:

```
┌─────────────────────── JVM (Paper Server) ───────────────────────┐
│                                                                   │
│  ┌─── Minecraft Plugin ───┐    ┌─── Gömülü Web Sunucusu ───┐    │
│  │  Event Listeners        │    │  Javalin (Jetty tabanlı)   │    │
│  │  StatisticsCollector    │◄──►│  AuthController            │    │
│  │  ConfigManager          │    │  DashboardController       │    │
│  │  CommandHandler         │    │  JwtManager                │    │
│  │  Async Scheduler        │    │  RateLimiter (Bucket4j)    │    │
│  │                         │    │  Static Resources (SPA)    │    │
│  │  [Server Thread]        │    │  [Jetty Thread Pool]       │    │
│  └─────────────────────────┘    └────────────────────────────┘    │
│                  │                           │                    │
│          ┌───────┴───────────────────────────┘                    │
│          ▼                                                        │
│  ┌─── Paylaşılan Servisler ──────────────────────────────────┐   │
│  │  HikariCP Pool │ Caffeine Cache │ AuthMe Hash Adapter     │   │
│  │  SecurityUtil   │ config.yml                               │   │
│  └────────────────────────────────────────────────────────────┘   │
│          │                           │                            │
└──────────┼───────────────────────────┼────────────────────────────┘
           ▼                           ▼
    ┌────────────┐              ┌────────────┐
    │   MySQL    │              │  Tarayıcı  │
    │  (TLS)     │              │ HTTPS:8443 │
    └────────────┘              └────────────┘
```

**Tek JAR, sıfır dış bağımlılık.** Node.js, PHP, Python veya ayrı bir web sunucusu kurulmaz. Plugin `plugins/` klasörüne atılır, `/webpanel reload` ile yönetilir.

---

## 1. Gömülü HTTP Sunucusu Seçimi

### Neden Javalin?

| Kriter | Javalin (Jetty) | NanoHTTPD | com.sun.net.httpserver |
|---|---|---|---|
| Shade sonrası boyut | ~3.5 MB | ~35 KB | 0 (JDK içi) |
| Thread pool yönetimi | Jetty QueuedThreadPool — tam kontrol | Tek thread / manuel | Basit Executor |
| HTTPS (embedded) | Jetty SslContextFactory, JKS/PKCS12 | Manuel SSLServerSocket | Temel HttpsServer |
| WebSocket | Var | Yok | Yok |
| Routing / middleware | Dekoratif before/after handler | Elle parse | Elle parse |
| Üretim kanıtı | Jetty 15+ yıl | Hobi seviyesi | Oracle "internal API" uyarısı |

**Karar:** Javalin. 3.5 MB boyut artışı Minecraft JAR'ı için ihmal edilebilir. Jetty'nin thread pool'u oyun sunucusundan tamamen izole çalışır, production-grade TLS desteği sunar. NanoHTTPD ciddi trafik altında yetersiz; `com.sun.net.httpserver` JDK'lar arası taşınabilirlik garantisi vermiyor ve Oracle bunu public API olarak desteklemiyor.

---

## 2. Plugin Katmanı (Bukkit/Paper API)

### 2.1 AuthMe Entegrasyonu

- AuthMe'nin `authme` tablosuna **SADECE SELECT** yapılır, hiçbir koşulda INSERT/UPDATE/DELETE çalıştırılmaz.
- Kimlik doğrulama AuthMe'nin sorumluluğunda kalır; web panel sadece şifre hash'ini doğrulama amaçlı okur.
- AuthMe `config.yml`'deki `settings.security.passwordHash` değeri okunarak hash algoritması dinamik belirlenir:

```java
public interface HashStrategy {
    boolean verify(String plainPassword, String storedHash);
}

// Desteklenen algoritmalar (AuthMe ile uyumlu):
// SHA256, BCRYPT, ARGON2, PBKDF2, MD5, XAUTH, CUSTOM
```

Plugin başlarken AuthMe config'i parse edilir, uygun `HashStrategy` implementasyonu seçilir. Sabit kodlama yok — yeni algoritma eklemek tek bir sınıf yazmak kadar kolay.

### 2.2 İstatistik Toplama

Event listener'lar ana thread'de tetiklenir ama veritabanı yazımı **Async Scheduler** üzerinden yapılır:

```
Oyuncu blok kırar → BlockBreakEvent
  → Listener in-memory sayacı artırır (ConcurrentHashMap)
  → Her 60 saniyede bir BukkitRunnable batch olarak MySQL'e yazar
  → Ana thread'e dokunmaz, 20 TPS korunur
```

Toplanan istatistikler:
- Oynama süresi (saniye bazında, join/quit arası delta)
- Blok kırma / yerleştirme
- Oyuncu öldürme / ölüm / mob öldürme
- Yürüme mesafesi
- Son görülme / ilk katılım tarihi
- Günlük bazda kırılım (`wp_daily_stats`)

### 2.3 Yaşam Döngüsü

```java
// onEnable()
1. config.yml yükle (port, MySQL bilgileri, TLS ayarları)
2. HikariCP pool başlat
3. Tablo migration'larını çalıştır (yoksa oluştur)
4. AuthMe config'inden hash algoritmasını tespit et
5. Caffeine cache'i kur
6. Event listener'ları kaydet
7. Web sunucusunu AYRI THREAD'de başlat
8. Async istatistik flush zamanlayıcısını başlat

// onDisable()
1. Async zamanlayıcıyı iptal et
2. Bellekteki istatistikleri son kez flush et
3. Web sunucusunu kapat (Jetty graceful shutdown, 5s timeout)
4. HikariCP pool'u kapat
5. Aktif session'ları veritabanına yaz
```

---

## 3. Gömülü Web Sunucusu Katmanı

### 3.1 API Endpoint'leri

```
POST /api/auth/login          → Kullanıcı adı + şifre, JWT döner
POST /api/auth/logout         → Session sonlandır
GET  /api/auth/me             → Aktif kullanıcı bilgisi

GET  /api/dashboard           → Özet istatistikler (cache'li)
GET  /api/stats/{username}    → Oyuncu detay istatistikleri
GET  /api/stats/{username}/daily?from=&to=  → Günlük kırılım
GET  /api/online              → Anlık çevrimiçi oyuncu listesi

GET  /                        → SPA dashboard (index.html)
GET  /assets/*                → CSS/JS/görseller (jar içinden)
```

### 3.2 Kimlik Doğrulama Akışı

```
Tarayıcı                    Web Sunucusu                    MySQL
   │                            │                              │
   ├─ POST /api/auth/login ────►│                              │
   │  {username, password}      │                              │
   │                            ├─ SELECT password FROM        │
   │                            │  authme WHERE username=? ───►│
   │                            │◄─ stored_hash ───────────────┤
   │                            │                              │
   │                            ├─ HashVerifier.verify(        │
   │                            │    password, stored_hash,    │
   │                            │    algorithm)                │
   │                            │                              │
   │                            ├─ JWT üret (HMAC-SHA256)      │
   │                            │  payload: {sub, iat, exp}    │
   │                            │                              │
   │◄─ Set-Cookie: token=JWT ──┤                              │
   │   HttpOnly; Secure;       │                              │
   │   SameSite=Strict;        │                              │
   │   Path=/; Max-Age=86400   │                              │
   │                            │                              │
   ├─ GET /api/dashboard ──────►│                              │
   │  Cookie: token=JWT        │                              │
   │                            ├─ JWT doğrula                 │
   │                            ├─ Caffeine cache kontrol      │
   │◄─ {stats JSON} ──────────┤                              │
```

### 3.3 Rate Limiting

Bucket4j ile token-bucket algoritması:

```
Her IP adresi için:
- Login endpoint:  5 deneme / 15 dakika (başarısız denemeler sayılır)
- API endpoint'ler: 60 istek / dakika
- Statik dosyalar: 120 istek / dakika

Limit aşımında: HTTP 429 + Retry-After header
Başarısız login'ler wp_login_log tablosuna yazılır (denetim izi)
```

### 3.4 Statik Kaynaklar

SPA arayüzü (HTML/CSS/JS) JAR'ın `resources/web/` dizinine gömülü olarak dağıtılır:

```
src/main/resources/
├── config.yml
├── web/
│   ├── index.html
│   ├── assets/
│   │   ├── app.css
│   │   └── app.js
│   └── favicon.ico
└── db/
    └── migrations/
        ├── V1__create_player_stats.sql
        ├── V2__create_daily_stats.sql
        ├── V3__create_sessions.sql
        └── V4__create_login_log.sql
```

Javalin bu dosyaları classpath'ten sunar — dosya sistemi erişimi gerekmez, JAR içinden okunur.

---

## 4. Veritabanı Şeması

### AuthMe Tablosu (DOKUNULMAZ — sadece okunur)

```sql
-- AuthMe'nin mevcut tablosu, plugin tarafından oluşturulmaz
-- authme (
--     id          INT PRIMARY KEY AUTO_INCREMENT,
--     username    VARCHAR(255) UNIQUE,
--     realname    VARCHAR(255),
--     password    VARCHAR(255),       -- hash'lenmiş şifre
--     ip          VARCHAR(40),
--     lastlogin   BIGINT,
--     regdate     BIGINT,
--     regip       VARCHAR(40),
--     x, y, z     DOUBLE,
--     world       VARCHAR(255),
--     email       VARCHAR(255),
--     isLogged, hasSession, totp ...
-- )
```

### Plugin Tabloları

```sql
CREATE TABLE wp_player_stats (
    username        VARCHAR(255) PRIMARY KEY,
    play_time_sec   BIGINT       NOT NULL DEFAULT 0,
    blocks_broken   BIGINT       NOT NULL DEFAULT 0,
    blocks_placed   BIGINT       NOT NULL DEFAULT 0,
    kills           INT          NOT NULL DEFAULT 0,
    deaths          INT          NOT NULL DEFAULT 0,
    mob_kills       INT          NOT NULL DEFAULT 0,
    distance_walked DOUBLE       NOT NULL DEFAULT 0,
    first_join      TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    last_seen       TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP
                                 ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_last_seen (last_seen)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE wp_daily_stats (
    username        VARCHAR(255) NOT NULL,
    stat_date       DATE         NOT NULL,
    play_time_sec   INT          NOT NULL DEFAULT 0,
    blocks_broken   INT          NOT NULL DEFAULT 0,
    blocks_placed   INT          NOT NULL DEFAULT 0,
    kills           INT          NOT NULL DEFAULT 0,
    deaths          INT          NOT NULL DEFAULT 0,
    PRIMARY KEY (username, stat_date),
    INDEX idx_date (stat_date)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE wp_sessions (
    token_hash      CHAR(64)     PRIMARY KEY,   -- JWT'nin SHA-256 hash'i
    username        VARCHAR(255) NOT NULL,
    ip_address      VARCHAR(45)  NOT NULL,
    created_at      TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    expires_at      TIMESTAMP    NOT NULL,
    INDEX idx_username (username),
    INDEX idx_expires (expires_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE wp_login_log (
    id              BIGINT       AUTO_INCREMENT PRIMARY KEY,
    username        VARCHAR(255) NOT NULL,
    ip_address      VARCHAR(45)  NOT NULL,
    success         BOOLEAN      NOT NULL,
    attempted_at    TIMESTAMP    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_ip_time (ip_address, attempted_at),
    INDEX idx_user_time (username, attempted_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### Tablo İlişkileri

```
authme.username ←──(READ ONLY)── wp_player_stats.username
                                  wp_daily_stats.username
                                  wp_sessions.username
                                  wp_login_log.username
```

Foreign key tanımlanmaz (AuthMe tablosuna DDL müdahale etmemek için). Tutarlılık uygulama katmanında sağlanır.

---

## 5. Build & Paketleme Stratejisi (Maven)

### 5.1 Bağımlılıklar ve Shade Yapılandırması

```xml
<dependencies>
    <!-- Paper API — provided, sunucu zaten sağlıyor -->
    <dependency>
        <groupId>io.papermc.paper</groupId>
        <artifactId>paper-api</artifactId>
        <version>1.21.4-R0.1-SNAPSHOT</version>
        <scope>provided</scope>
    </dependency>

    <!-- Shade edilecekler -->
    <dependency>
        <groupId>io.javalin</groupId>
        <artifactId>javalin</artifactId>
        <version>6.4.0</version>
    </dependency>
    <dependency>
        <groupId>com.zaxxer</groupId>
        <artifactId>HikariCP</artifactId>
        <version>6.2.1</version>
    </dependency>
    <dependency>
        <groupId>com.github.ben-manes.caffeine</groupId>
        <artifactId>caffeine</artifactId>
        <version>3.1.8</version>
    </dependency>
    <dependency>
        <groupId>io.jsonwebtoken</groupId>
        <artifactId>jjwt-impl</artifactId>
        <version>0.12.6</version>
    </dependency>
    <dependency>
        <groupId>io.jsonwebtoken</groupId>
        <artifactId>jjwt-jackson</artifactId>
        <version>0.12.6</version>
    </dependency>
    <dependency>
        <groupId>com.bucket4j</groupId>
        <artifactId>bucket4j-core</artifactId>
        <version>8.14.0</version>
    </dependency>
    <dependency>
        <groupId>com.mysql</groupId>
        <artifactId>mysql-connector-j</artifactId>
        <version>9.1.0</version>
    </dependency>
</dependencies>
```

### 5.2 Maven Shade Plugin Yapılandırması

```xml
<plugin>
    <groupId>org.apache.maven.plugins</groupId>
    <artifactId>maven-shade-plugin</artifactId>
    <version>3.6.0</version>
    <executions>
        <execution>
            <phase>package</phase>
            <goals><goal>shade</goal></goals>
            <configuration>
                <createDependencyReducedPom>false</createDependencyReducedPom>
                <minimizeJar>true</minimizeJar>
                <relocations>
                    <relocation>
                        <pattern>io.javalin</pattern>
                        <shadedPattern>com.r0ine.webpanel.lib.javalin</shadedPattern>
                    </relocation>
                    <relocation>
                        <pattern>org.eclipse.jetty</pattern>
                        <shadedPattern>com.r0ine.webpanel.lib.jetty</shadedPattern>
                    </relocation>
                    <relocation>
                        <pattern>com.zaxxer.hikari</pattern>
                        <shadedPattern>com.r0ine.webpanel.lib.hikari</shadedPattern>
                    </relocation>
                    <relocation>
                        <pattern>com.github.benmanes.caffeine</pattern>
                        <shadedPattern>com.r0ine.webpanel.lib.caffeine</shadedPattern>
                    </relocation>
                    <relocation>
                        <pattern>io.jsonwebtoken</pattern>
                        <shadedPattern>com.r0ine.webpanel.lib.jwt</shadedPattern>
                    </relocation>
                    <relocation>
                        <pattern>io.github.bucket4j</pattern>
                        <shadedPattern>com.r0ine.webpanel.lib.bucket4j</shadedPattern>
                    </relocation>
                    <relocation>
                        <pattern>kotlin</pattern>
                        <shadedPattern>com.r0ine.webpanel.lib.kotlin</shadedPattern>
                    </relocation>
                    <relocation>
                        <pattern>org.slf4j</pattern>
                        <shadedPattern>com.r0ine.webpanel.lib.slf4j</shadedPattern>
                    </relocation>
                </relocations>
                <filters>
                    <filter>
                        <artifact>*:*</artifact>
                        <excludes>
                            <exclude>META-INF/*.SF</exclude>
                            <exclude>META-INF/*.DSA</exclude>
                            <exclude>META-INF/*.RSA</exclude>
                            <exclude>META-INF/MANIFEST.MF</exclude>
                        </excludes>
                    </filter>
                </filters>
            </configuration>
        </execution>
    </executions>
</plugin>
```

### 5.3 Neden Relocate?

| Kütüphane | Relocate Sebebi |
|---|---|
| Jetty | Paper'ın kendi Jetty sürümüyle çakışma (class loader conflict) |
| Kotlin stdlib | Javalin Kotlin'e bağımlı, Paper'ın gömülü Kotlin'iyle çakışır |
| SLF4J | Paper'ın Log4j bridge'iyle çakışır; plugin tarafında `getLogger()` kullanılır |
| HikariCP | Başka plugin'ler farklı HikariCP sürümü kullanabilir |
| Caffeine | Aynı sınıf adı çakışması riski |

`minimizeJar: true` kullanılmayan Jetty modüllerini keser — JAR boyutu ~3.5 MB'den ~2.5 MB'ye düşer.

### 5.4 Tahmini JAR Boyutları

| Bileşen | Boyut |
|---|---|
| Plugin kodu | ~200 KB |
| Javalin + Jetty (shade sonrası) | ~2 MB |
| HikariCP | ~150 KB |
| MySQL Connector/J | ~2.5 MB |
| jjwt | ~400 KB |
| Caffeine | ~300 KB |
| Bucket4j | ~200 KB |
| Kotlin stdlib (minimize sonrası) | ~300 KB |
| Web arayüzü (HTML/CSS/JS) | ~500 KB |
| **Toplam** | **~6.5 MB** |

---

## 6. Güvenlik Riskleri ve Önlemler

### 6.1 Risk Matrisi

| # | Risk | Şiddet | Önlem |
|---|---|---|---|
| 1 | SQL Injection | Kritik | Tüm sorgular `PreparedStatement` ile parametrize — string birleştirme ile sorgu oluşturmak kesinlikle yasak |
| 2 | Brute-force login | Yüksek | Bucket4j ile IP başına 5 deneme / 15 dk; başarısız denemeler `wp_login_log`'a yazılır |
| 3 | JWT secret sızması | Yüksek | İlk çalıştırmada `SecureRandom` ile 256-bit key üretilir, `data/webpanel/secret.key` dosyasına yazılır (config.yml'de düz metin tutulmaz) |
| 4 | XSS | Yüksek | API sadece JSON döner, HTML render sunucu tarafında yapılmaz; SPA tarafında kullanıcı girdisi escape edilir |
| 5 | CSRF | Orta | `SameSite=Strict` cookie + custom header kontrolü (`X-Requested-With`) |
| 6 | Session hijacking | Orta | `HttpOnly`, `Secure`, `SameSite=Strict` cookie flag'leri; JWT token hash'i veritabanında saklanır, çalınan token revoke edilebilir |
| 7 | MySQL bağlantısı dinleme | Orta | `useSSL=true&verifyServerCertificate=true&requireSSL=true` JDBC parametreleri zorunlu |
| 8 | AuthMe tablosuna yazma | Orta | MySQL kullanıcısına `authme` tablosu için yalnızca `SELECT` yetkisi verilir (GRANT ile) |
| 9 | HTTP trafik dinleme | Orta | Gömülü Jetty TLS desteği (aşağıda detay) |
| 10 | Denial of Service | Orta | Jetty thread pool sınırı (max 20 thread), request body boyut limiti (1 MB) |
| 11 | Path traversal | Düşük | Statik dosyalar classpath'ten sunulur, dosya sistemi erişimi yok |
| 12 | Bilgi sızıntısı | Düşük | Hata yanıtlarında stack trace gönderilmez, genel hata mesajları kullanılır |

### 6.2 TLS / HTTPS Yapılandırması

Gömülü Jetty'de HTTPS kurmak, ayrı bir reverse proxy (Nginx/Caddy) olmadan yapıldığında **ekstra çaba gerektirir**:

**Seçenek A — Doğrudan Jetty TLS (reverse proxy yok):**
```yaml
# config.yml
web:
  port: 8443
  tls:
    enabled: true
    keystore-path: "keystore.p12"    # PKCS12 formatı
    keystore-password: "changeit"     # veya ortam değişkeni: ${KEYSTORE_PASS}
    # Let's Encrypt sertifikası:
    # certbot ile .pem alınır, ardından:
    # openssl pkcs12 -export -in fullchain.pem -inkey privkey.pem -out keystore.p12
```

Dezavantaj: Sertifika yenileme otomatik değil, sunucu sahibi her 90 günde `openssl pkcs12` komutunu çalıştırmalı (veya cron job kurmalı).

**Seçenek B — Reverse proxy arkasında (önerilen):**
```
İnternet → Nginx/Caddy (TLS termination, :443) → localhost:8080 (Javalin, HTTP)
```

Bu durumda Javalin düz HTTP dinler, TLS'i Nginx/Caddy halleder. Let's Encrypt otomatik yenileme çalışır. Ekstra yazılım gerektirir ama operasyonel olarak çok daha basit.

Plugin her iki senaryoyu da destekler — config.yml'de `tls.enabled: true/false`.

### 6.3 JWT Anahtar Yönetimi

```
İlk Çalıştırma:
1. plugins/WebPanel/secret.key dosyası var mı? → Oku
2. Yoksa → SecureRandom ile 32 byte üret → dosyaya yaz (chmod 600)
3. HMAC-SHA256 anahtarı olarak kullan
4. config.yml'de anahtar ASLA düz metin tutulmaz
```

JWT payload:
```json
{
  "sub": "oyuncu_adı",
  "iat": 1694700000,
  "exp": 1694786400,
  "jti": "rastgele-uuid"
}
```

Token ömrü: 24 saat (config'den ayarlanabilir). Logout'ta `jti` hash'i blacklist'e eklenir.

---

## 7. Performans ve Thread Yönetimi

### 7.1 Thread İzolasyonu

Tek JVM'de hem oyun hem web sunucusu çalıştırmanın en büyük riski, web trafiğinin oyun tick'ini (20 TPS) düşürmesi. Bu tamamen izole edilmelidir:

```
Paper Server Thread (ana thread)
├── Oyun döngüsü (20 TPS)
├── Event listener'lar (senkron, hafif)
└── BukkitScheduler (senkron task'ler)

Jetty Thread Pool (tamamen ayrı)
├── HTTP istekleri (max 20 thread, config'den ayarlanabilir)
├── TLS handshake
└── Response yazma

HikariCP Thread Pool (paylaşılan)
├── max 10 bağlantı (config'den ayarlanabilir)
├── Plugin async task'leri buradan okur/yazar
└── Web handler'ları buradan okur

Bukkit Async Scheduler
├── İstatistik flush (60 saniyede bir)
├── Session temizleme (5 dakikada bir)
└── Cache invalidation
```

**Kural:** Jetty handler'ları içinden `Bukkit.getScheduler().runTask()` (senkron) çağrılmaz. Bukkit API'ye erişim gerekirse `runTaskAsynchronously()` kullanılır veya paylaşılan cache'ten okunur.

### 7.2 Caffeine Cache Stratejisi

```java
// Sık sorgulanan veriler cache'lenir — her istekte MySQL'e gidilmez
Cache<String, PlayerStatsDTO> statsCache = Caffeine.newBuilder()
    .maximumSize(500)                    // en fazla 500 oyuncu
    .expireAfterWrite(30, TimeUnit.SECONDS)  // 30 saniye TTL
    .build();

Cache<String, DashboardDTO> dashboardCache = Caffeine.newBuilder()
    .maximumSize(1)
    .expireAfterWrite(10, TimeUnit.SECONDS)  // dashboard her 10s yenilenir
    .build();
```

### 7.3 HikariCP Havuz Ayarları

```yaml
database:
  host: "localhost"
  port: 3306
  name: "minecraft"
  username: "webpanel"
  password: "${DB_PASS}"
  pool:
    maximum-size: 10      # plugin + web paylaşımlı
    minimum-idle: 3
    idle-timeout: 300000  # 5 dakika
    max-lifetime: 600000  # 10 dakika
    connection-timeout: 5000
```

---

## 8. Tek-JAR / Tek-JVM Kısıtları ve Darboğazlar

### 8.1 Bilinen Kısıtlar

| Kısıt | Açıklama | Hafifletme |
|---|---|---|
| **Tek hata noktası** | Plugin crash ederse web panel de düşer (ve tersi) | Jetty'de `UncaughtExceptionHandler` — web katmanı hataları plugin'i çökertmez; hata izole edilir, loglanır |
| **Bellek paylaşımı** | JVM heap'i ortak; web trafiği GC baskısı yaratabilir | Jetty thread ve request body limitlerini düşük tut; response streaming kullan, büyük JSON chunk'lamadan dönme |
| **Port çakışması** | 8443 başka bir servis tarafından kullanılıyor olabilir | Config'den port ayarlanabilir; başlatmada `BindException` kontrol edilir, anlaşılır hata mesajı verilir |
| **Yatay ölçekleme yok** | Web paneli sadece ilgili sunucuyu yönetir; multi-sunucu dashboard yok | Her sunucuya kendi JAR'ı atılır; BungeeCord/Velocity seviyesinde birleştirme ayrı bir projedir |
| **Sertifika yönetimi** | Gömülü TLS'de Let's Encrypt otomatik yenileme zahmetli | Reverse proxy önerisi belgelerde belirtilir; keystore rotasyonu için `/webpanel reload-tls` komutu eklenir |
| **Classloader izolasyonu** | Paper'ın plugin classloader'ı ile shade edilmiş kütüphaneler arasında nadir çakışmalar | Tüm bağımlılıklar relocate edilir; `plugin.yml`'de `libraries` kullanılmaz |
| **Hot reload** | Web arayüzü güncellemek için sunucu yeniden başlatma veya `/webpanel reload` gerekir | Statik dosyalar opsiyonel olarak harici dizinden de okunabilir (`web.external-dir` config) |
| **Debug zorluğu** | Aynı JVM'de iki farklı framework debug etmek karmaşık | Her katman kendi logger'ını kullanır; web istekleri `[WebPanel-HTTP]`, plugin `[WebPanel]` prefix'i ile loglanır |

### 8.2 Olası Darboğazlar

**1. Veritabanı bağlantı açlığı:**
HikariCP pool boyutu 10 ise ve hem plugin hem web aynı anda yoğun sorgu atarsa bağlantı kuyruğu oluşur. Çözüm: istatistik yazımını batch'leyerek sorgu sayısını azalt, web tarafında cache ile MySQL'e gidiş sıklığını düşür.

**2. GC pause'ları:**
Web sunucusu çok fazla kısa ömürlü nesne üretirse (her istekte yeni DTO, JSON serialization) minor GC sıklaşır. Çözüm: object pooling değil ama gereksiz allocation'dan kaçınma — response'ları doğrudan stream'e yaz.

**3. Statik dosya servisi:**
JAR'dan classpath resource okumak disk I/O'su gerektirir. Yoğun trafikte darboğaz olabilir. Çözüm: `Cache-Control: public, max-age=86400` header'ı ile tarayıcı cache'ini kullan; `ETag` ile conditional request desteği.

**4. CPU paylaşımı:**
BCRYPT/ARGON2 gibi hash doğrulamaları CPU-yoğun. Aynı anda birçok login isteği gelirse oyun tick'i etkilenebilir. Çözüm: Jetty thread pool'u zaten ayrı, ama pool boyutunu 20 ile sınırla — eşzamanlı hash doğrulama sayısı da bu kadar olur.

---

## 9. Proje Yapısı

```
webpanel/
├── pom.xml
├── src/main/java/com/r0ine/webpanel/
│   ├── WebPanelPlugin.java              // JavaPlugin — giriş noktası
│   ├── core/
│   │   ├── ConfigManager.java           // config.yml okuma
│   │   └── DatabaseManager.java         // HikariCP + migration
│   ├── minecraft/
│   │   ├── listeners/
│   │   │   ├── PlayerStatsListener.java // join/quit/break/kill event'leri
│   │   │   └── ConnectionListener.java  // AuthMe olay yakalama
│   │   ├── commands/
│   │   │   └── WebPanelCommand.java     // /webpanel reload|status|reload-tls
│   │   └── tasks/
│   │       ├── StatsFlushTask.java      // 60s'de bir batch yazım
│   │       └── SessionCleanupTask.java  // süresi dolmuş session silme
│   ├── web/
│   │   ├── WebServer.java              // Javalin başlatma/kapatma
│   │   ├── auth/
│   │   │   ├── AuthController.java     // login/logout endpoint'leri
│   │   │   ├── JwtManager.java         // token üretme/doğrulama
│   │   │   └── AuthMiddleware.java     // before() handler, JWT kontrol
│   │   ├── api/
│   │   │   ├── DashboardController.java
│   │   │   └── StatsController.java
│   │   └── middleware/
│   │       ├── RateLimitMiddleware.java // Bucket4j
│   │       └── CorsHandler.java
│   ├── stats/
│   │   ├── StatisticsCollector.java    // in-memory sayaçlar
│   │   └── CacheManager.java          // Caffeine wrapper
│   └── security/
│       ├── HashVerifier.java           // AuthMe hash adaptörü
│       ├── HashStrategy.java           // interface
│       ├── BcryptStrategy.java
│       ├── Sha256Strategy.java
│       ├── Argon2Strategy.java
│       └── KeyManager.java            // JWT secret üretme/okuma
├── src/main/resources/
│   ├── plugin.yml
│   ├── config.yml
│   ├── web/
│   │   ├── index.html
│   │   └── assets/
│   │       ├── app.css
│   │       └── app.js
│   └── db/
│       └── migrations/
│           ├── V1__create_player_stats.sql
│           ├── V2__create_daily_stats.sql
│           ├── V3__create_sessions.sql
│           └── V4__create_login_log.sql
└── src/test/java/com/r0ine/webpanel/
    ├── security/HashVerifierTest.java
    └── web/AuthControllerTest.java
```

---

## 10. Örnek config.yml

```yaml
# WebPanel Yapılandırması
web:
  enabled: true
  host: "0.0.0.0"
  port: 8443
  max-threads: 20
  tls:
    enabled: false                    # true yapılırsa keystore gerekir
    keystore-path: "keystore.p12"
    keystore-password: "${KEYSTORE_PASS}"  # ortam değişkeni desteklenir
  cors:
    allowed-origins:
      - "https://example.com"
  rate-limit:
    login-attempts: 5
    login-window-minutes: 15
    api-requests-per-minute: 60

database:
  host: "localhost"
  port: 3306
  name: "minecraft"
  username: "webpanel"
  password: "${DB_PASS}"
  use-ssl: true
  pool:
    maximum-size: 10
    minimum-idle: 3

authme:
  table-name: "authme"               # AuthMe tablo adı (genelde "authme")
  hash-algorithm: "auto"             # "auto" = AuthMe config'inden tespit et
  config-path: "../AuthMe/config.yml" # AuthMe config yolu (göreceli, plugins/ içinde)

session:
  jwt-expiry-hours: 24
  cleanup-interval-minutes: 5

stats:
  flush-interval-seconds: 60
  cache-ttl-seconds: 30
  cache-max-entries: 500

messages:
  login-success: "Giriş başarılı."
  login-failed: "Kullanıcı adı veya şifre hatalı."
  rate-limited: "Çok fazla deneme. Lütfen bekleyin."
  unauthorized: "Oturum süresi dolmuş, tekrar giriş yapın."
```

---

## 11. MySQL Kullanıcı Yetkileri (Önerilen)

```sql
-- WebPanel için ayrı MySQL kullanıcısı oluştur
CREATE USER 'webpanel'@'localhost' IDENTIFIED BY 'guclu_sifre_buraya';

-- AuthMe tablosuna SADECE okuma yetkisi
GRANT SELECT ON minecraft.authme TO 'webpanel'@'localhost';

-- Kendi tablolarına tam yetki
GRANT ALL PRIVILEGES ON minecraft.wp_player_stats TO 'webpanel'@'localhost';
GRANT ALL PRIVILEGES ON minecraft.wp_daily_stats  TO 'webpanel'@'localhost';
GRANT ALL PRIVILEGES ON minecraft.wp_sessions     TO 'webpanel'@'localhost';
GRANT ALL PRIVILEGES ON minecraft.wp_login_log    TO 'webpanel'@'localhost';

-- Tablo oluşturma yetkisi (ilk kurulumda migration için)
GRANT CREATE ON minecraft.* TO 'webpanel'@'localhost';

FLUSH PRIVILEGES;
```

---

## 12. Özet Kontrol Listesi

- [ ] Javalin + Jetty shade/relocate edilmiş, classloader çakışması yok
- [ ] Kotlin stdlib relocate edilmiş (Paper'ın Kotlin'iyle çakışma önlendi)
- [ ] AuthMe tablosuna sadece SELECT yetkisi (DB seviyesinde)
- [ ] AuthMe hash algoritması config'den otomatik tespit
- [ ] Tüm SQL sorguları PreparedStatement
- [ ] JWT secret ilk çalıştırmada otomatik üretiliyor
- [ ] Cookie flag'leri: HttpOnly, Secure, SameSite=Strict
- [ ] Rate limiting aktif (login + API)
- [ ] MySQL TLS zorunlu (useSSL=true)
- [ ] Jetty thread pool ayrı, ana thread'e dokunmuyor
- [ ] İstatistik yazımı async batch (60s aralık)
- [ ] Caffeine cache aktif (dashboard + oyuncu istatistikleri)
- [ ] Graceful shutdown (onDisable'da Jetty + HikariCP kapatma)
- [ ] Hata mesajlarında stack trace sızmıyor
- [ ] Statik dosyalar classpath'ten, dosya sistemi erişimi yok
- [ ] TLS opsiyonel — reverse proxy ve doğrudan Jetty TLS seçenekleri belgelenmiş
