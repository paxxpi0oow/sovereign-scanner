import asyncio
import numpy as np
from src.scanner import scan_host
from src.neural_net import SimpleAutoencoder

PORTS = range(1, 1025)

def scan_to_vector(open_ports, port_range):
    vector = np.zeros(len(port_range))
    for p in open_ports:
        if p in port_range:
            vector[p - port_range.start] = 1
    return vector

async def collect_baseline(host, n_scans=5):
    print(f"[*] Mengumpulkan baseline dari {host}...")
    vectors = []
    for i in range(n_scans):
        open_ports = await scan_host(host, PORTS)
        vectors.append(scan_to_vector(open_ports, PORTS))
        print(f"    Scan {i+1}: {len(open_ports)} port terbuka")
    return np.array(vectors)

async def main():
    target_for_training = "127.0.0.1"
    target_to_check = input("Masukkan target untuk dipindai: ").strip()

    X_train = await collect_baseline(target_for_training, n_scans=5)
    if X_train.shape[0] == 0:
        print("[!] Baseline gagal.")
        return

    print("[*] Melatih neural network...")
    model = SimpleAutoencoder(input_dim=len(PORTS), hidden_dim=4)
    model.train(X_train, epochs=1000)

    train_errors = model.reconstruction_error(X_train)
    threshold = np.mean(train_errors) + 2 * np.std(train_errors)
    print(f"[*] Ambang batas anomali: {threshold:.4f}")

    print(f"[*] Memindai target: {target_to_check}")
    open_ports_new = await scan_host(target_to_check, PORTS)
    X_new = scan_to_vector(open_ports_new, PORTS).reshape(1, -1)
    error = model.reconstruction_error(X_new)[0]

    print(f"[*] Open ports: {open_ports_new}")
    print(f"[*] Reconstruction error: {error:.4f}")

    if error > threshold:
        print("[!] ANOMALI TERDETEKSI: Pola port tidak seperti biasanya!")
    else:
        print("[+] Pola port normal.")

if __name__ == "__main__":
    asyncio.run(main())
