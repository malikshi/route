# Route Converter Script
This script converts routing rules from various sources into Sing-box compatible format.

## Features
* Supports multiple input formats: V2Ray, Clash, and plain text
* Converts domain rules into Sing-box compatible format
* Supports IP CIDR, port, and port range rules
* Generates SRS files for Sing-box

## Usage
1. Clone the repository: `git clone https://github.com/malikshi/route.git`
2. Run the script: `python compile.py`
3. The script will generate SRS files in the `release/srs/convert` directory

## Download Pre-Generated SRS Files
You can download pre-generated SRS files from the following links:

### SRS Files
{% for file in files %}
* [{{ file }}](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/{{ file }})
{% endfor %}

## Configuration
The script uses a `config.json` file to configure the input sources and routing rules. You can modify this file to suit your needs.

## Notes
* Make sure to update the `config.json` file with your own input sources and routing rules.
* The script assumes that the Sing-box binary is installed and available in the system's PATH.

## Contributing
If you want to contribute to this project, feel free to fork the repository and submit a pull request.