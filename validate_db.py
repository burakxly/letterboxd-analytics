"""DB sağlık kontrolü — GitHub Action'da scraper'dan sonra, commit'ten ÖNCE çalışır.

Bozuk veri tespit ederse sıfırdan farklı kodla çıkar; workflow fail olur,
bozuk DB asla commit'lenmez ve GitHub fail bildirimi gönderir.

Kullanım: python validate_db.py [db_yolu] [onceki_db_yolu]
  onceki_db_yolu verilirse (git show HEAD:letterboxd_master.db çıktısı)
  bir önceki güne göre regresyon kontrolleri de yapılır.
"""
import sqlite3
import sys
import os

# Bir gecede bundan fazla yeni film eklendiyse bir şeyler yanlıştır
# (mükerrer ekleme döngüsü, RSS parse hatası vs.)
MAX_NEW_ROWS_PER_RUN = 15


def count(conn: sqlite3.Connection, sql: str) -> int:
    return conn.execute(sql).fetchone()[0]


def main() -> int:
    db_path = sys.argv[1] if len(sys.argv) > 1 else "letterboxd_master.db"
    prev_path = sys.argv[2] if len(sys.argv) > 2 else ""

    errors: list[str] = []
    conn = sqlite3.connect(db_path)

    # ── 1. Mükerrer kayıt: aynı film + aynı izleme tarihi asla olmamalı ──
    dupes = conn.execute("""
        SELECT Name, "Watched Date", COUNT(*) c FROM movies
        GROUP BY Name, "Watched Date" HAVING c > 1
    """).fetchall()
    if dupes:
        sample = ", ".join(f"{n} ({d}) x{c}" for n, d, c in dupes[:5])
        errors.append(f"{len(dupes)} mukerrer kayit grubu var: {sample}")

    # ── 2. Anlık durum özeti ──
    total = count(conn, "SELECT COUNT(*) FROM movies")
    stats = {
        "Year=0":    count(conn, "SELECT COUNT(*) FROM movies WHERE Year IS NULL OR Year = 0"),
        "Director=''": count(conn, "SELECT COUNT(*) FROM movies WHERE Director IS NULL OR Director = ''"),
        "Runtime=0": count(conn, "SELECT COUNT(*) FROM movies WHERE Runtime IS NULL OR Runtime = 0"),
        "Poster=''": count(conn, "SELECT COUNT(*) FROM movies WHERE Poster_URL IS NULL OR Poster_URL = ''"),
    }
    print(f"Toplam satir: {total}")
    for label, val in stats.items():
        print(f"  {label}: {val}")

    # ── 3. Önceki güne göre regresyon kontrolleri ──
    if prev_path and os.path.exists(prev_path) and os.path.getsize(prev_path) > 0:
        pconn = sqlite3.connect(prev_path)
        try:
            prev_total = count(pconn, "SELECT COUNT(*) FROM movies")
            new_rows = total - prev_total
            print(f"Onceki gun: {prev_total} satir -> bu gece +{new_rows}")

            if new_rows < 0:
                errors.append(f"Satir sayisi AZALDI: {prev_total} -> {total} (veri kaybi?)")
            if new_rows > MAX_NEW_ROWS_PER_RUN:
                errors.append(
                    f"Bir gecede {new_rows} yeni satir eklendi (limit {MAX_NEW_ROWS_PER_RUN}) "
                    "— mukerrer ekleme dongusu olabilir"
                )

            # Mevcut (eski) satırlarda alan bozulması: boş alan sayısı, eklenen
            # yeni satır sayısından fazla arttıysa dolu alanlar ezilmiş demektir
            prev_stats = {
                "Year=0":    count(pconn, "SELECT COUNT(*) FROM movies WHERE Year IS NULL OR Year = 0"),
                "Director=''": count(pconn, "SELECT COUNT(*) FROM movies WHERE Director IS NULL OR Director = ''"),
                "Runtime=0": count(pconn, "SELECT COUNT(*) FROM movies WHERE Runtime IS NULL OR Runtime = 0"),
                "Poster=''": count(pconn, "SELECT COUNT(*) FROM movies WHERE Poster_URL IS NULL OR Poster_URL = ''"),
            }
            allowed_increase = max(new_rows, 0)
            for label, prev_val in prev_stats.items():
                if stats[label] - prev_val > allowed_increase:
                    errors.append(
                        f"Alan regresyonu {label}: {prev_val} -> {stats[label]} "
                        f"(izin verilen artis: {allowed_increase})"
                    )
        finally:
            pconn.close()
    else:
        print("Onceki DB yok/bos — regresyon kontrolleri atlandi.")

    conn.close()

    if errors:
        print("\n[FAIL] DB dogrulamasi basarisiz:")
        for e in errors:
            print(f"  - {e}")
        return 1

    print("\n[OK] DB dogrulamasi gecti.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
