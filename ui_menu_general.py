from rich.console import Console

console = Console()

def titulo(texto):

    console.print(
        f"\n━━━ {texto} ━━━",
        style="bold #e0b16d"
    )


def exito(texto):
    console.print(
        f"✅ {texto}",
        style="bold green"
    )


def error(texto):
    console.print(
        f"❌ {texto}",
        style="bold red"
    )


def advertencia(texto):
    console.print(
        f"⚠️ {texto}",
        style="bold yellow"
    )


def modificar(texto):
    console.print(
        f"✏️ {texto}",
        style="bold magenta"
    )


def eliminar(texto):
    console.print(
        f"🗑️ {texto}",
        style="bold red"
    )