from rich.console import Console

console = Console()

def titulo(texto):

    console.print(
        f"\n━━━ {texto} ━━━",
        style="bold #8A2BE2"
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