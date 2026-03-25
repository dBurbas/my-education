import cmd
from rich.console import Console
from rich.table import Table
from rich.progress import track
import time
import questionary
import readline

console = Console()

# Auto-complete commands for Mac/Linux
if "libedit" in readline.__doc__:
    readline.parse_and_bind("bind ^I rl_complete")
else:
    readline.parse_and_bind("tab: complete")


class EcosystemCLI(cmd.Cmd):
    prompt = "\033[1;36m❀(eco)*\033[0m "

    def __init__(self, simulation):
        super().__init__()
        # TODO: добавить класс связи с моделью экосистемы
        self.sim = simulation

    def preloop(self):
        """Onetime print before program work"""
        console.print(r"""[bold #77CC08]
          .#H:    :H#.           █████╗ ███╗   ██╗██╗███╗   ███╗ █████╗ ██╗
        ~=##=~L  J~=##=~        ██╔══██╗████╗  ██║██║████╗ ████║██╔══██╗██║
        +=##=+|  |+=##=+        ███████║██╔██╗ ██║██║██╔████╔██║███████║██║
         H##WiT  TiW##H         ██╔══██║██║╚██╗██║██║██║╚██╔╝██║██╔══██║██║
   t#t    TTT      TTT    t#t   ██║  ██║██║ ╚████║██║██║ ╚═╝ ██║██║  ██║███████╗
  .:#=+      .*=#=.      +=#:.  ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝
 =gM##W;    *=%##%=*    ;W##Mg=  
 =gM##W!    =M%##%M=    !W##Mg= ██╗    ██╗ ██████╗ ██████╗ ██╗     ██████╗
   :v#;  .wHW$@##@$WHw.  ;#v:   ██║    ██║██╔═══██╗██╔══██╗██║     ██╔══██╗
         whW$@####@$Whw         ██║ █╗ ██║██║   ██║██████╔╝██║     ██║  ██║
        .=w%%$####$%%w=.        ██║███╗██║██║   ██║██╔══██╗██║     ██║  ██║
        \Y%%$##NMN##$%%Y/       ╚███╔███╔╝╚██████╔╝██║  ██║███████╗██████╔╝
         .=*&8#####8&*=.         ╚══╝╚══╝  ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═════╝[/bold #77CC08]
    """)
        console.print("[bold #6ABB00]✿ Animal World Simulation v1.0 ✿[/bold #6ABB00]\n")
        console.print("? Type [cyan]help[/] or [cyan]?[/] for list of commands.\n")

    def do_help(self, arg):
        """Show help.
        :param arg: command (optional)"""
        if arg:
            return super().do_help(arg)

        super().do_help(arg)

        console.print()
        console.print("[bold cyan]Quick start:[/bold cyan]")
        console.print("- [green]run[/]   — run / continue simulation")
        console.print("- [green]stats[/] — show statistics")
        console.print("- [green]organism[/]   — organism operations")
        console.print("- [green]food_chain[/]   — food chain operations")
        console.print("- [green]load[/]   — load ecosystem from file")
        console.print("- [green]save[/]   — save ecosystem in file")
        console.print("- [green]exit[/]  — exit program\n")

    def do_run(self, arg):
        """Runs an ecosystem simulation for a specified number of steps.
        :param: arg: number of steps
        :type arg: int (default: 1)"""
        if not arg:
            steps = 1
        else:
            try:
                steps = int(arg.strip())
                if steps <= 0:
                    raise ValueError
            except ValueError:
                # TODO: перевести на английский
                console.print(f"[red]Error: '{arg}' is not a positive integer.[/]")
                console.print("Usage: [cyan]run [N][/] — for example, [cyan]run 7[/]")
                return

        console.print(f"[green]Запуск симуляции на {steps} шаг(ов)...[/]")
        for step in track(range(steps), description="Simulating :) ..."):
            # TODO: Симулируем какую-то работу
            time.sleep(0.5)

    def do_stats(self, arg):
        """Show statistics of the ecosystem
        Details:
        Shows number of organisms, current state, simulation age, etc.
        """
        table = Table(title="Current population")
        table.add_column("Type", justify="left", style="cyan")
        table.add_column("Count", justify="right", style="magenta")

        # TODO: Здесь данные запрашиваются из модели
        table.add_row("Wolves", "12")
        table.add_row("Rabbits", "45")

        console.print(table)

    def do_organism(self, arg):
        """organism operations (add/remove/stats)
        Details:
        Allows user to add organism / remove organism / view statistics of organism"""
        animal_type = questionary.select(
            # TODO: выбор запрашиваются из модели
            "Which organism would you like to add?",
            choices=["Wolf", "Rabbit", "Fox"],
        ).ask()
        count = questionary.text("Enter the count:").ask()
        # TODO: сделать выбор операции через questionate
        if animal_type and count.isdigit():
            console.print(
                f"[green]✔ Successfully added {count} animals: {animal_type}![/green]"
            )
        else:
            console.print("[red]Error: invalid input!\nExpect number (0,1,2,...)[/red]")

    def do_food_chain(self, arg):
        """Food chain operations (add/remove/view)
        Details:
        Allows user to modify food chain of the ecosystem, view current food chain"""

    def do_save(self, arg):
        """Save the ecosystem to a file"""

        # TODO: save("ecosystem.json")

    def do_load(self, arg):
        """Load the ecosystem from a file
        :param: file_path
        :type: str (default: "/save_files/ecosystem.json")"""

    # TODO: load("ecosystem.json")

    def do_exit(self, arg):
        """Exit the program"""
        console.print("[bold red]Stop program...[/bold red]")
        return True


if __name__ == "__main__":
    cli = EcosystemCLI(simulation=None)
    cli.cmdloop()
