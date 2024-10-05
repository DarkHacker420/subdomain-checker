# Subdomain Checker

Welcome to the Subdomain Checker! This tool allows you to find, filter, and probe subdomains for a given domain and check their web technologies.

## Features

- **Subdomain Discovery**: Uses `subfinder` to identify subdomains.
- **Filtering and Probing**: Filters and checks for alive subdomains using `httprobe`.
- **Web Technology Detection**: Identifies technologies used on the alive subdomains with `whatweb`.
- **Output Management**: Saves results in specified directories for easy access.

## Requirements

- Python 3
- Required tools:
  - `subfinder`
  - `httprobe`
  - `whatweb`
  - `anew`

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/subdomain-checker.git
   cd subdomain-checker
   ```

2. **Install dependencies**:
   You can run the script, and it will check for missing tools and prompt you to install them if necessary.

3. **Run the script**:
   ```bash
   python3 checker.py <domain> [-o <output-dir>]
   ```

   - `<domain>`: The domain for which you want to find subdomains.
   - `-o` or `--output-dir`: (Optional) Directory to save the output files (default is the current directory).

## Usage

```bash
./checker.py example.com -o output
```

This command will find subdomains for `example.com`, filter them, and check their web technologies, saving all results in the `output` directory.

## Output Files

- `subdomains.txt`: List of found subdomains.
- `unique_filtered_subdomains.txt`: Unique filtered subdomains related to the specified domain.
- `alivesub.txt`: Alive subdomains that responded to the probing.
- `web_technologies.txt`: Information about the technologies used on the alive subdomains.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any enhancements or fixes.

---

### Note

Ensure you have the necessary permissions and follow ethical guidelines when using this tool.
