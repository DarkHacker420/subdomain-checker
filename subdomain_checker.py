#!/usr/bin/env python3

import argparse
import subprocess
import os
import sys
from rich.console import Console

console = Console()

def welcome_message():
    ascii_art_logo = """
        ▓█████▄  ▄▄▄       ██▀███   ██ ▄█▀  ██████  ██░ ██  ▄▄▄      ▓█████▄  ▒█████   █     █░
        ▒██▀ ██▌▒████▄    ▓██ ▒ ██▒ ██▄█▒ ▒██    ▒ ▓██░ ██▒▒████▄    ▒██▀ ██▌▒██▒  ██▒▓█░ █ ░█░
        ░██   █▌▒██  ▀█▄  ▓██ ░▄█ ▒▓███▄░ ░ ▓██▄   ▒██▀▀██░▒██  ▀█▄  ░██   █▌▒██░  ██▒▒█░ █ ░█ 
        ░▓█▄   ▌░██▄▄▄▄██ ▒██▀▀█▄  ▓██ █▄   ▒   ██▒░▓█ ░██ ░██▄▄▄▄██ ░▓█▄   ▌▒██   ██░░█░ █ ░█ 
        ░▒████▓  ▓█   ▓██▒░██▓ ▒██▒▒██▒ █▄▒██████▒▒░▓█▒░██▓ ▓█   ▓██▒░▒████▓ ░ ████▓▒░░░██▒██▓ 
        ▒▒▓  ▒  ▒▒   ▓▒█░░ ▒▓ ░▒▓░▒ ▒▒ ▓▒▒ ▒▓▒ ▒ ░ ▒ ░░▒░▒ ▒▒   ▓▒█░ ▒▒▓  ▒ ░ ▒░▒░▒░ ░ ▓░▒ ▒  
        ░ ▒  ▒   ▒   ▒▒ ░  ░▒ ░ ▒░░ ░▒ ▒░░ ░▒  ░ ░ ▒ ░▒░ ░  ▒   ▒▒ ░ ░ ▒  ▒   ░ ▒ ▒░   ▒ ░ ░  
        ░ ░  ░   ░   ▒     ░░   ░ ░ ░░ ░ ░  ░  ░   ░  ░░ ░  ░   ▒    ░ ░  ░ ░ ░ ░ ░ ▒    ░   ░  
        ░          ░  ░   ░     ░  ░         ░   ░  ░  ░      ░  ░   ░        ░ ░      ░    
    """
    console.print(f"[bold magenta]{ascii_art_logo}[/bold magenta]")
    console.print("[cyan][bold]Welcome to the subdomains checker[/bold][/cyan]\n")

def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return result.stdout.strip()

def install_tools(tools):
    console.print("[yellow]Installing missing tools...[/yellow]")
    for tool in tools:
        console.print(f"[cyan]Installing {tool}...[/cyan]")
        subprocess.run(f"sudo apt install {tool} -y", shell=True)

def check_tools():
    tools = ['subfinder', 'httprobe', 'whatweb', 'anew']
    missing_tools = []
    for tool in tools:
        if subprocess.run(f"command -v {tool}", shell=True, stdout=subprocess.DEVNULL).returncode != 0:
            missing_tools.append(tool)

    if missing_tools:
        install_tools(missing_tools)
    else:
        console.print("[green]All necessary tools are installed.[/green]")

def find_subdomains(domain, output_dir):
    console.print(f"[yellow]Finding subdomains for [bold]{domain}[/bold]...[/yellow]")
    subdomains = run_command(f"subfinder -d {domain} -all -recursive -silent")
    subdomains_file = os.path.join(output_dir, "subdomains.txt")
    with open(subdomains_file, "w") as file:
        file.write(subdomains)
    console.print(f"[green]Subdomains saved to {subdomains_file}[/green]")
    return subdomains_file

def filter_and_probe_subdomains(domain, subdomains_file, output_dir):
    console.print("[yellow]Filtering, sorting, and probing subdomains...[/yellow]")
    unique_filtered_subdomains_file = os.path.join(output_dir, "unique_filtered_subdomains.txt")
    alive_subdomains_file = os.path.join(output_dir, "alivesub.txt")

    unique_filtered_subdomains = run_command(f"grep '{domain}' {subdomains_file} | sort -u")
    if unique_filtered_subdomains:
        with open(unique_filtered_subdomains_file, "w") as file:
            file.write(unique_filtered_subdomains)
        alive_subdomains = run_command(f"cat {unique_filtered_subdomains_file} | httprobe -p https | grep https | anew {alive_subdomains_file}")
        if alive_subdomains:
            console.print(f"[green]Alive subdomains saved to {alive_subdomains_file}[/green]")
            os.remove(unique_filtered_subdomains_file)
            os.remove(subdomains_file)
            check_web_technologies(alive_subdomains_file, output_dir)
        else:
            console.print("[red]No alive subdomains found.[/red]")
    else:
        console.print("[red]No subdomains found containing the specified domain.[/red]")

def check_web_technologies(alive_subdomains_file, output_dir):
    console.print("[yellow]Checking web technologies of alive subdomains...[/yellow]")
    technologies_file = os.path.join(output_dir, "web_technologies.txt")
    web_technologies = run_command(f"whatweb -i {alive_subdomains_file}")
    console.print(web_technologies)
    with open(technologies_file, "w") as file:
        file.write(web_technologies)
    console.print(f"[green]Web technologies information saved to {technologies_file}[/green]")

def main():
    welcome_message()  # Show the welcome message
    check_tools()  # Check and install necessary tools
    parser = argparse.ArgumentParser(description="Find subdomains, filter and probe for alive subdomains, and check their web technologies.")
    parser.add_argument("domain", help="Domain to find subdomains for")
    parser.add_argument("-o", "--output-dir", default=".", help="Directory to save the output files (default: current directory)")
    args = parser.parse_args()

    # Ensure the output directory exists
    os.makedirs(args.output_dir, exist_ok=True)

    subdomains_file = find_subdomains(args.domain, args.output_dir)
    filter_and_probe_subdomains(args.domain, subdomains_file, args.output_dir)

if __name__ == "__main__":
    main()
