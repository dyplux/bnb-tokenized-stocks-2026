# Praeva browser console

This folder contains the current published Praeva frontend source and its prebuilt static viewer. The viewer runs without Node or a build step.

`Start-Praeva.command` starts a loopback-only Python 3 server on port 8937 and opens `/console/`. `Start-Praeva.bat` is the Windows equivalent. The server has no API, provider, wallet, or server actions. It serves the unchanged files in `web/static` and redirects the two optional video routes to the existing public HTTPS URLs. Video files aren't bundled.

Development files are included for reference. If needed, run `npm ci` and `npm run build` inside `web`. No install or build is required for the viewer and no dependency downloads happen at launch.

The package hasn't been signed or notarized. Windows and macOS launchers have been checked as scripts, but execution hasn't been tested on every operating system.

From the repository root, run `python3 scripts/run_console.py`. The script opens the browser. Python 3.9+ is required; the recorded console cases need no API credentials. The separate fresh review UI is `python3 app/safety_server.py`.
