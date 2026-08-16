import sqlite3
from apscheduler.schedulers.background import BackgroundScheduler
from services.mikrotik import remove_mac


def cleanup_expired_sessions():

    conn = sqlite3.connect("data/wifi.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM transactions
        WHERE status='success'
          AND expires_at IS NOT NULL
          AND expires_at <= datetime('now')
    """)

    expired_sessions = cursor.fetchall()

    for session in expired_sessions:

        mac = session["mac_address"]

        print("=" * 50)
        print("EXPIRED SESSION FOUND")
        print("MAC:", mac)
        print("Reference:", session["reference"])

        # Remove device from MikroTik
        remove_mac(mac)

        # Mark as expired
        cursor.execute("""
            UPDATE transactions
            SET status='expired'
            WHERE reference=?
        """, (session["reference"],))

        print("Session expired successfully.")
        print("=" * 50)

    conn.commit()
    conn.close()


scheduler = BackgroundScheduler()
scheduler.add_job(cleanup_expired_sessions, 'interval', minutes=1)
scheduler.start()

print("⏰ Expiry scheduler started...")


if __name__ == "__main__":
    try:
        import time
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        scheduler.shutdown()