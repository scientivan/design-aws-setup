# Ticketing di AWS (Jalur B, Container)

Proyek individu Minggu 12 mata kuliah Komputasi Awan. Pengguna melihat katalog acara kampus dan memesan tiket. Dua layanan berjalan sebagai container Docker pada EC2. Image keduanya tersedia di repositori privat Amazon ECR.

| Aspek | Pilihan |
|---|---|
| Kasus penggunaan | Pemesanan tiket acara kampus |
| Jalur | B (EC2 + Docker + ECR) |
| Entitas data | `Ticket` (satu pemesanan) |
| Layanan | `event-service` untuk katalog baca-saja dan `ticket-service` untuk CRUD tiket |
| Lingkungan AWS | AWS Academy Lab Project “Microservices and CI/CD Pipeline Builder” (kelas 195218), wilayah `us-east-1` |

[Briefing Minggu 12 dalam bahasa Indonesia](docs/briefing-minggu-12-id.pdf)

## Status Minggu 12

Kedua image dibangun, dijalankan sebagai container pada host EC2 Cloud9, dan diunggah ke ECR. Uji CRUD dijalankan melalui localhost di dalam instance. Pemesanan tersimpan di memori dan port 8081 serta 8082 belum terbuka ke internet.

## Struktur repositori

| Lokasi | Isi |
|---|---|
| `services/event-service/` | Kode dan Dockerfile untuk katalog acara pada port 8081 |
| `services/ticket-service/` | Kode dan Dockerfile untuk CRUD tiket pada port 8082 |
| `scripts/run-local.sh` | Membangun image dan menjalankan kedua container pada satu jaringan Docker |
| `scripts/test-crud.sh` | Memeriksa respons layanan dan menjalankan uji CRUD |
| `scripts/push-ecr.sh` | Membuat repositori ECR jika perlu, memberi tag, dan mengunggah image |
| [Spesifikasi API](docs/api-spec.md) | Entitas, endpoint, dan kode status |
| [Rencana deployment](docs/deployment-plan.md) | Implementasi saat ini dan tahap berikutnya |
| [Catatan serah terima](docs/CODEX_HANDOFF.md) | Sumber fakta untuk deliverable |
| `evidence/` | Keluaran perintah asli dan tangkapan layar AWS |
| [Deliverable Minggu 12](deliverables/) | Diagram arsitektur, ringkasan desain, dan laporan bukti AWS |

## Menjalankan proyek

Gunakan Docker. Langkah unggah juga membutuhkan AWS CLI dan kredensial AWS, misalnya kredensial sementara dari Cloud9. Kedua layanan hanya memakai pustaka standar Python.

```bash
./scripts/run-local.sh
./scripts/test-crud.sh
./scripts/push-ecr.sh
```

Untuk CRUD yang berhasil, kode status yang diharapkan adalah 201 saat membuat, 200 saat membaca, 200 saat mengubah, dan 204 saat menghapus. Membaca kembali tiket yang sudah dihapus menghasilkan 404.

## Endpoint

| Layanan | Metode dan path | Fungsi |
|---|---|---|
| event-service | `GET /events`, `GET /events/{eventId}` | Membaca katalog dan detail acara |
| ticket-service | `POST /tickets` | Membuat pemesanan |
| ticket-service | `GET /tickets/{ticketId}` | Membaca satu pemesanan |
| ticket-service | `PUT /tickets/{ticketId}` | Mengubah status atau data pembeli |
| ticket-service | `DELETE /tickets/{ticketId}` | Menghapus pemesanan |

Kedua layanan menyediakan `GET /health`. Daftar tiket tersedia melalui `GET /tickets`.
