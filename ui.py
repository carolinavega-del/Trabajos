from rich.console import Console

# force_terminal asegura la visualización de colores ANSI en la terminal integrada de VS Code.
console = Console(force_terminal=True, color_system="truecolor")


def titulo(texto):
    console.print(
        f"\n━━━ {texto} ━━━",
                style="bold #A8D8C0"    )


def menu(texto):
    console.print(texto)


def exito(texto):
    console.print(
        f"✅   {texto}",
        style="bold green"
    )


def error(texto):
    console.print(
        f"❌   {texto}",
        style="bold red"
    )


def advertencia(texto):
    console.print(
        f"⚠️   {texto}",
        style="bold yellow"
    )


def modificar(texto):
    console.print(
        f"✏️   {texto}",
        style="bold magenta"
    )


def eliminar(texto):
    console.print(
        f"🗑️   {texto}",
        style="bold red"
    )
