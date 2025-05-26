from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static
from textual.containers import Horizontal
from textual.reactive import reactive
import psutil
import time
from rich.text import Text

# ----- Network Monitor Widget -----
class NetworkMonitor(Static):
    download_speed = reactive(0.0)
    upload_speed = reactive(0.0)

    def on_mount(self):
        self.prev_counters = psutil.net_io_counters()
        self.set_interval(1, self.refresh_stats)

    def refresh_stats(self):
        counters = psutil.net_io_counters()
        self.download_speed = (counters.bytes_recv - self.prev_counters.bytes_recv) / 1024 / 1024
        self.upload_speed = (counters.bytes_sent - self.prev_counters.bytes_sent) / 1024 / 1024
        self.prev_counters = counters
        self.refresh()

    def render(self):
        text = Text()
        text.append("📡 Network Monitor\n\n", style="bold underline")
        text.append(f"↓ Download: {self.download_speed:.2f} MB/s\n")
        text.append(f"↑ Upload: {self.upload_speed:.2f} MB/s\n")
        return text

# ----- Storage Monitor Widget (partitions) -----
class StorageMonitor(Static):
    def on_mount(self):
        self.set_interval(5, self.refresh)

    def render(self):
        text = Text()
        text.append("💾 Storage Usage (Partitions)\n\n", style="bold underline")
        partitions = psutil.disk_partitions(all=False)
        for p in partitions:
            try:
                usage = psutil.disk_usage(p.mountpoint)
                text.append(f"{p.device} [{p.mountpoint}]\n")
                text.append(f"  Total: {usage.total / (1024**3):.2f} GB\n")
                text.append(f"  Used:  {usage.used / (1024**3):.2f} GB\n")
                text.append(f"  Free:  {usage.free / (1024**3):.2f} GB\n")
                text.append(f"  Usage: {usage.percent}%\n\n")
            except PermissionError:
                # skip inaccessible partitions
                continue
        return text

# ----- Physical Disk Monitor Widget -----
class PhysicalDiskMonitor(Static):
    def on_mount(self):
        self.set_interval(5, self.refresh)

    def render(self):
        text = Text()
        text.append("🛠️ Physical Disks info\n\n", style="bold underline")
        disks = psutil.disk_partitions(all=False)
        # collect physical disks unique by device root (e.g. /dev/sda)
        physical_disks = {}
        for p in disks:
            root_dev = p.device.rstrip("0123456789")  # rough trim device number
            if root_dev not in physical_disks:
                physical_disks[root_dev] = []
            physical_disks[root_dev].append(p.mountpoint)

        for disk, mountpoints in physical_disks.items():
            # aggregate usage of all mountpoints under one physical disk
            total = used = free = 0
            for mnt in mountpoints:
                try:
                    usage = psutil.disk_usage(mnt)
                    total += usage.total
                    used += usage.used
                    free += usage.free
                except PermissionError:
                    continue
            if total == 0:
                continue
            usage_percent = used / total * 100
            text.append(f"{disk}\n")
            text.append(f"  Total: {total / (1024**3):.2f} GB\n")
            text.append(f"  Used:  {used / (1024**3):.2f} GB\n")
            text.append(f"  Free:  {free / (1024**3):.2f} GB\n")
            text.append(f"  Usage: {usage_percent:.1f}%\n\n")
        return text


# ----- Main App -----
class WRMonApp(App):
    CSS_PATH = "wrmon.css"

    def compose(self) -> ComposeResult:
        yield Header()
        with Horizontal(id="main-horizontal"):
            yield NetworkMonitor(id="network-monitor")
            yield StorageMonitor(id="storage-monitor")
            yield PhysicalDiskMonitor(id="physical-disk-monitor")
        yield Footer()


if __name__ == "__main__":
    WRMonApp().run()
