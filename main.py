from pathlib import Path
import json
import sys

import uvicorn

from app import app


if __name__ == "__main__":
    config = {"host": "0.0.0.0", "port": 8000}
    config_path = Path("config.json")

    if config_path.exists():
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                config.update(json.load(f))
            print(f"✅ Loaded config from config.json → Host: {config['host']}, Port: {config['port']}")
        except Exception as exc:
            print(f"⚠️ Error reading config.json: {exc}. Using defaults.")

    for i, arg in enumerate(sys.argv):
        if arg == "--host" and i + 1 < len(sys.argv):
            config["host"] = sys.argv[i + 1]
        elif arg == "--port" and i + 1 < len(sys.argv):
            config["port"] = int(sys.argv[i + 1])

    bind_host = config.get("host", "0.0.0.0")
    if isinstance(bind_host, str) and bind_host in ("all", "*"):
        bind_host = "::"

    cert_dir = Path("certs")
    crt_path = cert_dir / "server.crt"
    key_path = cert_dir / "server.key"
    pfx_path = cert_dir / "server.pfx"

    display_host = bind_host if bind_host != "::" else ":: (all IPv6/IPv4-dual)"
    print(f"🚀 Starting server on http://{display_host}:{config['port']}")

    if crt_path.exists() and key_path.exists():
        print("✅ Running with HTTPS using .crt + .key")
        uvicorn.run(
            app,
            host=bind_host,
            port=config["port"],
            ssl_certfile=str(crt_path),
            ssl_keyfile=str(key_path),
        )
    elif pfx_path.exists():
        print("✅ PFX found. Running with HTTPS (limited support)")
        uvicorn.run(app, host=bind_host, port=config["port"])
    else:
        print("⚠️ No certificate found. Running on HTTP.")
        uvicorn.run(app, host=bind_host, port=config["port"])

