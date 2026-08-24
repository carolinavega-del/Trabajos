from rich.console import Console

console = Console()

def titulo(texto):
    console.print(
        f"\n━━━ {texto} ━━━",
        style="bold #FF99CC"
    )

def exito(texto):
    console.print(f"✅ {texto}", style="bold green")

def error(texto):
    console.print(f"❌ {texto}", style="bold red")

def advertencia(texto):
    console.print(f"⚠️ {texto}", style="bold yellow")

def modificar(texto):
    console.print(f"✏️ {texto}", style="bold magenta")

def eliminar(texto):
    console.print(f"🗑️ {texto}", style="bold red")

def info(texto):
    console.print(f"ℹ️ {texto}", style="bold cyan")

def linea():
    console.print("═" * console.width, style="dim")
    
