# Spesifikasi API

Isi permintaan dan respons menggunakan JSON. Waktu dicatat dalam format ISO 8601 UTC.

## Entitas data Ticket

Satu rekaman `Ticket` mewakili satu pemesanan untuk satu acara.

| Kolom | Tipe | Aturan |
|---|---|---|
| `ticketId` | string | Kunci utama yang dibuat otomatis dengan awalan `tkt-` dan delapan karakter heksadesimal |
| `eventId` | string | Wajib dan harus terdaftar di event-service saat pemesanan dibuat |
| `eventName` | string | Disalin dari event-service saat pemesanan dibuat |
| `buyerName` | string | Wajib saat pembuatan |
| `buyerEmail` | string | Opsional |
| `quantity` | integer | Minimal 1, dengan nilai bawaan 1 |
| `totalPrice` | integer | Harga acara dalam IDR dikali jumlah tiket |
| `status` | string | `BOOKED` saat dibuat dan dapat diubah ke `PAID` atau `CANCELLED` |
| `createdAt` | string | Waktu pembuatan |
| `updatedAt` | string | Waktu pembuatan atau pembaruan terakhir |

event-service memiliki data acuan baca-saja dengan kolom `eventId`, `name`, `date`, `venue`, `capacity`, dan `price`. CRUD hanya berlaku untuk entitas Ticket.

## Empat endpoint CRUD pada ticket-service (port 8082)

| Operasi | Permintaan | Sukses | Kesalahan |
|---|---|---|---|
| Buat | `POST /tickets` dengan `eventId` dan `buyerName`. `buyerEmail` dan `quantity` bersifat opsional | 201 dan Ticket baru | 400 kolom wajib atau jumlah tiket tidak valid, 404 acara tidak ditemukan, 503 event-service tidak tersedia |
| Baca | `GET /tickets/{ticketId}` | 200 dan Ticket | 404 tiket tidak ditemukan |
| Ubah | `PUT /tickets/{ticketId}` dengan `status`, `buyerName`, atau `buyerEmail` | 200 dan Ticket yang diperbarui | 400 status atau JSON tidak valid, 404 tiket tidak ditemukan |
| Hapus | `DELETE /tickets/{ticketId}` | 204 tanpa isi respons | 404 tiket tidak ditemukan |

Rute tambahan adalah `GET /tickets` untuk daftar tiket dan `GET /health` untuk pemeriksaan layanan.

## event-service (port 8081)

| Permintaan | Respons |
|---|---|
| `GET /events` | 200 dan daftar acara |
| `GET /events/{eventId}` | 200 dan detail acara, atau 404 jika acara tidak ditemukan |
| `GET /health` | 200 dan `{"service":"event-service","status":"ok"}` |

## Permintaan antarlayanan

Saat menerima `POST /tickets`, ticket-service memanggil `GET {EVENT_SERVICE_URL}/events/{eventId}` dengan batas waktu tiga detik. Di Docker, jaringan bridge `ticketing-net` membuat `http://event-service:8081` dapat diakses dengan nama container.
