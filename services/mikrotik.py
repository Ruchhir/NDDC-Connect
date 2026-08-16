import os
from dotenv import load_dotenv
from routeros_api import RouterOsApiPool

load_dotenv()


def authorize_mac(mac_address, duration_hours):

    print("=" * 50)
    print("MIKROTIK ACTIVATION")
    print("MAC Address:", mac_address)
    print("Duration:", duration_hours, "hours")

    host = os.getenv("MIKROTIK_HOST")
    username = os.getenv("MIKROTIK_USERNAME")
    password = os.getenv("MIKROTIK_PASSWORD")
    port = int(os.getenv("MIKROTIK_PORT", 8728))

    try:
        connection = RouterOsApiPool(
            host,
            username=username,
            password=password,
            port=port,
            plaintext_login=True,
        )

        api = connection.get_api()

        bindings = api.get_resource("/ip/hotspot/ip-binding")

        bindings.add(
            mac_address=mac_address,
            type="bypassed",
            comment=f"NDDC {duration_hours}h",
        )

        print("Device authorized successfully.")

        connection.disconnect()

    except Exception as e:
        print("MikroTik connection failed.")
        print(e)

    print("=" * 50)


def remove_mac(mac_address):

    print("=" * 50)
    print("MIKROTIK REMOVE")
    print("MAC Address:", mac_address)

    host = os.getenv("MIKROTIK_HOST")
    username = os.getenv("MIKROTIK_USERNAME")
    password = os.getenv("MIKROTIK_PASSWORD")
    port = int(os.getenv("MIKROTIK_PORT", 8728))

    try:
        connection = RouterOsApiPool(
            host,
            username=username,
            password=password,
            port=port,
            plaintext_login=True,
        )

        api = connection.get_api()

        bindings = api.get_resource("/ip/hotspot/ip-binding")

        entries = bindings.get(mac_address=mac_address)

        for entry in entries:
            bindings.remove(id=entry[".id"])

        print("Device removed successfully.")

        connection.disconnect()

    except Exception as e:
        print("MikroTik removal failed.")
        print(e)

    print("=" * 50)