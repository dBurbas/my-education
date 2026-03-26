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


# TODO: добавить кастомные Exceptions для интерфейса
class EcosystemCLI(cmd.Cmd):
    prompt = "\033[1;36m❀(eco)*\033[0m "

    def __init__(self, controller):
        super().__init__()
        # TODO: добавить класс связи с моделью экосистемы
        self.controller = controller

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
                console.print(f"[red]Error: '{arg}' is not a positive integer.[/]")
                console.print("Usage: [cyan]run [N][/] — for example, [cyan]run 7[/]")
                return

        console.print(f"[green]Running simulation for {steps} step(s)...[/]")
        for step in track(range(steps), description="Simulating :) ..."):
            self.controller.run_steps(1)
            time.sleep(0.1)

        logs = self.controller.get_latest_logs()
        if logs:
            console.print(
                "\n[bold yellow]Events (what happened) during steps:[/bold yellow]"
            )
            for log in logs:
                console.print(log)
        else:
            console.print("[dim]Nothing remarkable happened.[/dim]")

    def do_stats(self, arg):
        """Show statistics of the ecosystem
        Details:
        Shows number of organisms, current state, simulation age, etc.
        """
        table = Table(title="Current population")
        table.add_column("Type", justify="left", style="cyan")
        table.add_column("Count", justify="right", style="magenta")

        stats = self.controller.get_population_stats()

        if not stats:
            table.add_row("Пусто", "0")
        else:
            for org_type, count in stats.items():
                table.add_row(org_type, str(count))

        console.print(table)

    def do_organism(self, arg):
        """organism operations (add/remove/stats)
        Details:
        Allows user to add organism / remove organism / view statistics of organism"""
        operation = questionary.select(
            "Which operation to do?", choices=["Add", "Remove", "View Stats"]
        ).ask()

        organism_type = questionary.select(
            # TODO: выбор запрашиваются из модели
            "Which organism would you like to choose?",
            choices=["Wolf", "Rabbit", "Fox"],
        ).ask()

        # TODO: убрать дублирование кода
        if operation == "Add":
            count = questionary.text("Enter the count:").ask()
            if organism_type and count.isdigit():
                console.print(
                    f"[green]✔ Successfully added {count} organisms: {organism_type}![/green]"
                )
            else:
                console.print(
                    "[red]Error: invalid input!\nExpect non negative number (0,1,2,...)[/red]"
                )
        elif operation == "Remove":
            count = questionary.text("Enter the count:").ask()
            if organism_type and count.isdigit():
                console.print(
                    f"[green]✔ Successfully killed {count} organisms: {organism_type}![/green]"
                )
            else:
                console.print(
                    "[red]Error: invalid input!\nExpect non negative number (0,1,2,...)[/red]"
                )
        elif operation == "View Stats":
            # TODO: количество вида запрашивается у модели
            console.print(f"Species:{organism_type}. Count:{1}")

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
