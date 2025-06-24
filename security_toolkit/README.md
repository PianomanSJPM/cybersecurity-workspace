# Security Toolkit

A modular, extensible cybersecurity toolkit for analysts, students, and professionals. This toolkit features a modern Python GUI and integrates multiple security tools in one place.

---

## Features

- **Modular Design:** Each security function is a separate module, making it easy to extend and maintain.
- **Modern GUI:** Built with `tkinter` and `ttk` for a clean, tabbed interface.
- **Cross-Platform:** Designed for macOS and Linux.

---

## Module Status

| Module                | Status         | Description                                      |
|---------------------- |---------------|--------------------------------------------------|
| Network Monitor       | Minimal       | Placeholder UI; no real monitoring yet            |
| Vulnerability Scanner | Functional    | Nmap-based scanning, CVE checks, export results   |
| Log Analyzer          | Minimal       | Placeholder UI; no real log analysis yet          |
| Incident Response     | Functional    | Incident tracking, playbooks, export, UI          |
| Security Policy       | Minimal       | Placeholder UI; no real policy management yet     |
| Patch Manager         | Minimal       | Placeholder UI; no real patching yet              |
| Risk Assessor         | Minimal       | Placeholder UI; no real risk assessment yet       |
| Threat Intelligence   | Functional    | Multi-source lookups, API integration, export     |

---

## Development Progress

- **Project Structure Created:**
  - `main.py` launches the GUI and initializes all modules.
  - Each module is in its own file under `modules/`.
  - Centralized configuration with `config_manager.py`.
- **Minimal Modules:**
  - Network Monitor, Log Analyzer, Security Policy, Patch Manager, and Risk Assessor have placeholder UIs and an `update_ui` method for integration.
- **Functional Modules:**
  - Vulnerability Scanner, Incident Response, and Threat Intelligence have real features and UI.
- **Error Handling:**
  - All modules now have an `update_ui` method to prevent runtime errors.
- **Dependency Management:**
  - All required Python packages are listed in `requirements.txt`.
  - System dependencies (like `nmap`) are required for some modules.
- **Testing:**
  - The application launches cleanly and displays all tabs.

---

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd security_toolkit
   ```
2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
3. **Install system dependencies:**
   - On macOS: `brew install nmap`
   - On Linux: `sudo apt install nmap`
4. **Configure API keys:**
   - Copy `config/config.example.json` to `config/config.json` and add your API keys for Threat Intelligence.
5. **Run the application:**
   ```bash
   sudo python security_toolkit/main.py
   ```

---

## Usage

- **Explore each tab:** Each module is accessible via a tab in the main window.
- **Placeholder modules:** These display a message and a button, but do not yet have real functionality.
- **Functional modules:**
  - **Vulnerability Scanner:** Scan targets, view results, export to CSV.
  - **Incident Response:** Track incidents, use playbooks, export reports.
  - **Threat Intelligence:** Search IPs/domains/hashes, view results, export data.

---

## Next Steps

- Implement real functionality for minimal modules.
- Polish the UI and add more user feedback.
- Expand documentation and add screenshots.
- Prepare for public release and portfolio/demo use.

---

## Contributing

Contributions are welcome! Please open issues or submit pull requests for improvements, bug fixes, or new modules.

---

## License

MIT License (see LICENSE file)

## Acknowledgments

- Thanks to all contributors and the open-source community
- Inspired by various security tools and frameworks
- Built with Python and modern security practices

## Contact

Your Name - [@yourtwitter](https://twitter.com/yourtwitter) - email@example.com

Project Link: [https://github.com/yourusername/security_toolkit](https://github.com/yourusername/security_toolkit) 