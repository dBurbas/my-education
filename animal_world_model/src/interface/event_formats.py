EVENT_FORMATS = {
    "move": lambda e: (
        f"[green]🐾 {e['mover']} moved to x:{e['x']:.1f}, y:{e['y']:.1f}. Sprint: {e['is_sprint']}[/green]"
    ),
    "death": lambda e: f"[red]💀 {e['name']} died: {e['cause']}[/red]",
    "eat": lambda e: f"[yellow]🍽️ {e['eater']} eaten {e['food']}[/yellow]",
    "sound": lambda e: f"[blue]🔊 {e['sound_maker']} says: {e['sound']}[/blue]",
    "rest": lambda e: (
        f"[cyan]🐾 {e['animal']} rests, hp:{e['health']} en:{e['energy']}[/cyan]"
    ),
    "reproduction": lambda e: (
        f"[magenta]👶 {e['baby']} born from {e['parent']}[/magenta]"
    ),
}
