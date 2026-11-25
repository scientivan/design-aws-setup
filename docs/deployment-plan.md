# Rencana deployment

## Tahap 1 (Minggu 12, selesai)

1. Lingkungan Cloud9 `MicroservicesIDE` memakai instance EC2 `t3.small` dengan Amazon Linux 2023 di LabVPC, Public Subnet1, dan koneksi SSH. Lab membatasi konfigurasi yang dapat dipakai.
2. Kode diunggah ke Cloud9. `scripts/run-local.sh` membangun dua image dengan image dasar `public.ecr.aws/docker/library/python:3.12-alpine` untuk menghindari batas penarikan image Docker Hub.
3. Kedua container berjalan pada jaringan bridge Docker `ticketing-net`. Host memublikasikan port 8081 untuk event-service dan 8082 untuk ticket-service. Security group tidak membuka kedua port ke internet. Uji dilakukan dari dalam instance.
4. `scripts/test-crud.sh` mencatat respons pemesanan saat create, 200 saat baca dan ubah, 204 saat hapus, serta 404 saat membaca kembali tiket yang sudah dihapus. Respons create 201 terlihat pada demo terpisah dalam tangkapan layar Cloud9.
5. `scripts/push-ecr.sh` membuat repositori privat `ticketing/event-service` dan `ticketing/ticket-service` dengan pemindaian saat push, lalu mengunggah tag `v1` untuk masing-masing image.

## Tahap 2 (rencana)

1. Ganti penyimpanan di memori dengan SQLite pada volume Docker di host EC2 agar tiket bertahan ketika container dimulai ulang. Basis data terkelola dapat dipertimbangkan jika lab mengizinkannya.
2. Jalankan image dari ECR dengan `docker pull` dan `docker run` pada host EC2.
3. Gunakan Application Load Balancer sebagai satu-satunya jalur HTTP publik. Rute `/events*` menuju event-service dan `/tickets*` menuju ticket-service.

## Tahap 3 (rencana, mengikuti fase lab 5–9)

1. Pindahkan container ke Amazon ECS dengan satu task definition dan satu layanan untuk setiap microservice agar masing-masing dapat diskalakan secara mandiri.
2. Tambahkan pipeline CI/CD dengan CodeCommit atau sumber Git lain, CodePipeline, dan CodeDeploy. Push ke repositori akan memicu pembangunan image dan deployment.

## Biaya dan anggaran

Anggaran lab sebesar USD 40 dan tidak dapat diatur ulang. Biaya utama berasal dari instance `t3.small` Cloud9, yang masuk hibernasi setelah 30 menit tanpa aktivitas. Catatan proyek memperkirakan biaya penyimpanan dua image ECR yang masing-masing berukuran sekitar 18 MB jauh di bawah USD 0,01 per bulan. Akhiri sesi lab setelah bekerja untuk menghentikan penghitung waktu.
