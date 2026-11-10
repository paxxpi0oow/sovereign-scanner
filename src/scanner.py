import asyncio
import socket

async def scan_port(host: str, port: int, timeout: float = 0.5) -> bool:
    """
    Mencoba membuka koneksi TCP ke host:port.
    Mengembalikan True jika port terbuka, False jika tertutup/filtered.
    """
    try:
        # asyncio.open_connection adalah cara async untuk membuat koneksi TCP
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(host, port),
            timeout=timeout
        )
        writer.close()
        await writer.wait_closed()
        return True
    except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
        return False

async def scan_host(host: str, ports: range, concurrency: int = 500):
    """
    Memindai daftar port secara bersamaan dengan batas konkurensi.
    Mengembalikan list port yang terbuka.
    """
    semaphore = asyncio.Semaphore(concurrency)
    open_ports = []

    async def scan_with_limit(port):
        async with semaphore:
            if await scan_port(host, port):
                open_ports.append(port)

    await asyncio.gather(*(scan_with_limit(p) for p in ports))
    return sorted(open_ports)
