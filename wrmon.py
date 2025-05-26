from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.widgets import Header, Footer, Static
from textual.reactive import reactive
from textual.widget import Widget
from rich.table import Table
import psutil

# ================================
# WIDGET: Monitor Jaringan
# ================================
class NetworkMonitor(Widget):
    upload_speed = reactive("0 KB/s")
    download_speed = reactive("0 KB/s")

    def on_mount(self) -> None:
        counters = psutil.net_io_counters()
        self.prev_sent = counters.bytes_sent
        self.prev_recv = counters.bytes_recv
        self.set_interval(1.0, self.refresh_network)

    def refresh_network(self) -> None:
        counters = psutil.net_io_counters()
        sent_now = counters.bytes_sent
        recv_now = counters.bytes_recv
        upload = (sent_now - self.prev_sent) / (1024 * 1024)
        download = (recv_now - self.prev_recv) / (1024 * 1024)
        self.upload_speed = f"{upload:.2f} MB/s"
        self.download_speed = f"{download:.2f} MB/s"
        self.prev_sent = sent_now
        self.prev_recv = recv_now

    def render(self) -> Table:
        table = Table(title="Network Traffic", expand=True)
        table.add_column("Type", justify="center", style="bold green")
        table.add_column("Speed", justify="center", style="bold cyan")
        table.add_row("Upload", self.upload_speed)
        table.add_row("Download", self.download_speed)
        return table

# ================================
# WIDGET: Monitor Storage
# ================================
class StorageMonitor(Widget):
    def on_mount(self) -> None:
        self.set_interval(5.0, self.refresh)

    def render(self) -> Table:
        table = Table(title="Storage Usage", expand=True)
        table.add_column("Mount", style="bold magenta")
        table.add_column("Total", justify="right")
        table.add_column("Used", justify="right")
        table.add_column("Free", justify="right")
        table.add_column("Usage %", justify="right")

        for part in psutil.disk_partitions():
            try:
                usage = psutil.disk_usage(part.mountpoint)
                table.add_row(
                    part.mountpoint,
                    f"{usage.total // (1024**3)} GB",
                    f"{usage.used // (1024**3)} GB",
                    f"{usage.free // (1024**3)} GB",
                    f"{usage.percent}%",
                )
            except PermissionError:
                continue

        return table

# ================================
# APP: Aplikasi wrmon
# ================================
class WRMonApp(App):
    CSS_PATH = "wrmon.css"
    BINDINGS = [("q", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Vertical(
            Static("📊 wrmon - Storage + Network Monitor", id="title", classes="title"),
            Horizontal(
                StorageMonitor(classes="panel"),
                NetworkMonitor(classes="panel"),
                id="monitors"
            ),
            id="main"
        )
        yield Footer()

# ================================
# ENTRY POINT
# ================================
if __name__ == "__main__":
    WRMonApp().run()
