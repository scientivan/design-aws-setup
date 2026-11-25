# Catatan serah terima dokumentasi

Gunakan briefing resmi dan sumber di repositori untuk mendokumentasikan Minggu 12. Pertahankan ID sumber daya dan hasil pengujian sesuai bukti.

## Persyaratan tugas

1. Diagram arsitektur dengan alur data, IAM atau keamanan, dan label untuk komponen rencana.
2. Ringkasan desain sepanjang satu sampai dua halaman yang membahas kasus penggunaan, jalur, entitas data, dan empat endpoint CRUD.
3. Repositori Git berisi README, kode awal, rencana deployment, dan commit bertahap.
4. Bukti AWS berupa tangkapan layar dan keluaran tes atau pemeriksaan konektivitas.

Briefing resmi berada satu folder di atas repositori dengan nama `Lab_Project_Cloud_Computing_AWS_Lab_Project_Briefing_Updated.pdf`. Jalur B mensyaratkan minimal dua layanan yang direncanakan dan satu image Docker yang dibangun. Proyek sudah membangun serta mengunggah kedua image.

## Sumber fakta

| Topik | Sumber |
|---|---|
| Entitas, endpoint, dan kode status | `docs/api-spec.md` |
| Tahap deployment | `docs/deployment-plan.md` |
| Akun, VPC, subnet, instance, security group, digest, dan IAM | `evidence/outputs/07-infrastructure-inventory.txt` |
| Versi alat dan identitas | `evidence/outputs/01-environment.txt` |
| Build, container, dan image lokal | `evidence/outputs/02-docker-build-run.txt`, `03-docker-ps.txt`, `06-docker-images.txt` |
| Uji CRUD | `evidence/outputs/04-crud-test.txt` |
| Push ECR | `evidence/outputs/05-ecr-push.txt` |

## Arsitektur

Akun AWS `339712824643` memakai wilayah `us-east-1`. EC2 `aws-cloud9-MicroservicesIDE` adalah host Docker `t3.small` dengan Amazon Linux 2023 dan IP privat `10.16.10.227`. Host berada di Public Subnet1 `10.16.10.0/24` pada `us-east-1a`, di dalam LabVPC `10.16.0.0/16`. Browser pengembang mengakses Cloud9 melalui konsol AWS. Cloud9 menjangkau host lewat SSH. Security group `sg-010fc165085e65785` hanya mengizinkan TCP 22 dari rentang IP layanan Cloud9.

Jaringan Docker `ticketing-net` menghubungkan event-service pada port 8081 dan ticket-service pada port 8082. Alur bernomor dimulai dari curl di host yang mengirim `POST /tickets`. ticket-service meminta `GET /events/{id}`, event-service mengembalikan detail acara, lalu ticket-service menyimpan pemesanan di memori dan membalas HTTP 201. Port aplikasi belum terbuka ke internet.

Host mengunggah image `ticketing/event-service:v1` dan `ticketing/ticket-service:v1` ke ECR privat. Cloud9 menggunakan kredensial sementara dari peran lab `voclabs`. Login ECR memakai token sementara dari `aws ecr get-login-password`. Repositori tidak menyimpan access key statis.

Tandai rencana dengan garis putus-putus dan label `planned`. Rencana mencakup `docker pull`, Application Load Balancer di Public Subnet1 dan Public Subnet2 sebagai satu-satunya akses publik, SQLite pada volume Docker, layanan ECS per microservice, serta CodePipeline dan CodeDeploy dalam rangkaian fase lab 5–9. ALB merutekan `/events*` ke event-service dan `/tickets*` ke ticket-service. `MonolithicAppServer` merupakan instance bawaan lab di luar aplikasi ini.

## Ringkasan desain

Jelaskan pemesanan tiket acara kampus dan pilihan Jalur B yang didukung lab dan briefing. event-service memiliki katalog acara dan ticket-service mengelola pemesanan agar keduanya dapat dibangun, di-deploy, dan kelak diskalakan secara mandiri. Gunakan entitas Ticket dan empat endpoint utama pada spesifikasi API. Sebutkan bahwa Ticket disimpan di memori, port belum publik, dan tes berlangsung dari dalam instance.

## Indeks tangkapan layar

| Berkas dalam `evidence/screenshots/` | Isi |
|---|---|
| `01-cloud9-docker-ps-and-post-ticket.jpg` | Dua container aktif dan demo `POST /tickets` membalas HTTP 201 |
| `02-ecr-repositories.jpg` | Dua repositori privat ECR |
| `03-ecr-ticket-service-image-v1.jpg` | Image `v1` ticket-service berukuran 18,05 MB dengan awalan digest `sha256:2cce6dc1` |
| `04-ec2-instances-running.jpg` | Host Cloud9 `t3.small` aktif dan 3/3 pemeriksaan lulus |
| `05-cloud9-environment.jpg` | Lingkungan Cloud9 `MicroservicesIDE`, EC2, dan koneksi SSH |

Pemilik mengizinkan email UGM tetap terlihat pada tangkapan layar.

## Keterbatasan bukti

1. Detail image event-service dibuktikan lewat `05-ecr-push.txt`. Tangkapan layar detail image itu tidak tersedia.
2. Metadata tipe instance tidak tersedia pada `01-environment.txt`. Tipe `t3.small` terlihat pada tangkapan layar EC2.
3. Log CRUD mencetak isi respons create, sementara respons HTTP 201 terlihat pada demo terpisah.
4. Remote `origin` menunjuk ke `https://github.com/scientivan/design-aws-setup.git`. Push menunggu persetujuan pemilik.

## Aturan penulisan pemilik

Gunakan paragraf, daftar bernomor, atau tabel. Hindari karakter bullet, tanda pisah panjang, dan titik koma. Gunakan kalimat tersendiri untuk penjelasan.
