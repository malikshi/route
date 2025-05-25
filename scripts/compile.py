import json
import requests
import subprocess
import os

def process_v2ray_source(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []

    lines = response.text.splitlines()
    domains = []
    base_url = "/".join(url.split("/")[:-1]) + "/"
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("include:"):
            included_file = line.split(":")[1].strip()
            included_url = base_url + included_file
            included_domains = process_v2ray_source(included_url)
            domains.extend(included_domains)
        else:
            # Remove any attributes that start with "@"
            parts = line.split()
            domain_info = parts[0]
            if domain_info.startswith("domain:"):
                domain = domain_info.split(":")[1]
                domains.append(domain)
            elif domain_info.startswith("keyword:"):
                keyword = domain_info.split(":")[1]
                domains.append(f"keyword:{keyword}")
            elif domain_info.startswith("regexp:"):
                regexp = domain_info.split(":")[1]
                domains.append(f"regexp:{regexp}")
            elif domain_info.startswith("full:"):
                full_domain = domain_info.split(":")[1]
                domains.append(full_domain)
            else:
                # Assume it's a domain suffix
                domains.append(f"suffix:{domain_info}")
    return domains


def process_plain_source(list):
    domains = []
    ip_cidrs = []
    ports = []
    port_ranges = []
    for item in list:
        item = item.strip()
        if not item or item.startswith("#"):
            continue
        if item.startswith("- "):
            item = item[2:].strip()
        if item.startswith("'") and item.endswith("'"):
            item = item[1:-1].strip()
        if item.startswith("IP-CIDR,") or item.startswith("IP-CIDR6,"):
            ip_cidr = item.split(",")[1].strip()
            ip_cidrs.append(ip_cidr)
        elif "/" in item:
            if "," in item and (item.startswith("IP-CIDR,") or item.startswith("IP-CIDR6,")):
                ip_cidr = item.split(",")[1].strip()
                ip_cidrs.append(ip_cidr)
            else:
                ip_cidrs.append(item)
        elif item.startswith("port:"):
            port = item.split(":")[1].strip()
            ports.append(int(port))
        elif item.startswith("port-range:"):
            port_range = item.split(":")[1].strip()
            port_ranges.append(port_range)
        else:
            # Remove any attributes that start with "@"
            parts = item.split()
            domain_info = item
            if domain_info.startswith("suffix:"):
                domain_suffix = domain_info.split(":")[1].strip()
                domains.append(f"suffix:{domain_suffix}")
            elif domain_info.startswith("domain:"):
                domain = domain_info.split(":")[1].strip()
                domains.append(domain)
            elif domain_info.startswith("keyword:"):
                keyword = domain_info.split(":")[1].strip()
                domains.append(f"keyword:{keyword}")
            elif domain_info.startswith("regexp:"):
                regexp = domain_info.split(":")[1].strip()
                domains.append(f"regexp:{regexp}")
            elif domain_info.startswith("full:"):
                full_domain = domain_info.split(":")[1].strip()
                domains.append(full_domain)
            else:
                domains.append(f"suffix:{domain_info}")
    return domains, ip_cidrs, ports, port_ranges


def process_clash_source(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
    except requests.exceptions.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return [], []

    lines = response.text.splitlines()
    domains = []
    ip_cidrs = []
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("- "):
            line = line[2:].strip()
        if line.startswith("'") and line.endswith("'"):
            line = line[1:-1].strip()
        if line.startswith("DOMAIN-SUFFIX,"):
            domain_suffix = line.split(",")[1].strip()
            domains.append(f"suffix:{domain_suffix}")
        elif line.startswith("DOMAIN,"):
            domain = line.split(",")[1].strip()
            domains.append(domain)
        elif line.startswith("DOMAIN-KEYWORD,"):
            keyword = line.split(",")[1].strip()
            domains.append(f"keyword:{keyword}")
        elif line.startswith("IP-CIDR,") or line.startswith("IP-CIDR6,"):
            ip_cidr = line.split(",")[1].strip()
            ip_cidrs.append(ip_cidr)
        elif "/" in line:
            ip_cidrs.append(line)
    return domains, ip_cidrs


def generate_json(i, route):
    domains = {"domain": [], "domain_suffix": [], "domain_keyword": [], "domain_regex": []}
    ip_cidrs = {"ipv4": [], "ipv6": []}
    ports = []
    port_ranges = []
    for source in route["list"]:
        if source["type"] == "v2ray":
            source_domains = process_v2ray_source(source["url"])
            source_ip_cidrs = []
            source_ports = []
            source_port_ranges = []
        elif source["type"] == "clash":
            source_domains, source_ip_cidrs = process_clash_source(source["url"])
            source_ports = []
            source_port_ranges = []
        elif source["type"] == "plain":
            source_domains, source_ip_cidrs, source_ports, source_port_ranges = process_plain_source(source["list"])
        for domain in source_domains:
            if domain.startswith("suffix:"):
                domains["domain_suffix"].append(domain.split(":")[1])
            elif domain.startswith("keyword:"):
                domains["domain_keyword"].append(domain.split(":")[1])
            elif domain.startswith("regexp:"):
                domains["domain_regex"].append(domain.split(":")[1])
            else:
                domains["domain"].append(domain)
        for ip_cidr in source_ip_cidrs:
            if ":" in ip_cidr.split("/")[0]:
                ip_cidrs["ipv6"].append(ip_cidr)
            else:
                ip_cidrs["ipv4"].append(ip_cidr)
        ports.extend(source_ports)
        port_ranges.extend(source_port_ranges)

    # Remove duplicates and sort
    for key in domains:
        domains[key] = sorted(list(set(domains[key])))
    ip_cidrs["ipv4"] = sorted(list(set(ip_cidrs["ipv4"])))
    ip_cidrs["ipv6"] = sorted(list(set(ip_cidrs["ipv6"])))
    ports = sorted(list(set(ports)))
    port_ranges = sorted(list(set(port_ranges)))

    rule = {
        key: domains[key]
        for key in domains
        if domains[key]
    }
    # Add dot (.) to domain suffixes in json_data_srs
    rule["domain_suffix"] = [f".{domain_suffix}" if '.' not in domain_suffix else domain_suffix for domain_suffix in rule.get("domain_suffix", [])]

    if ip_cidrs["ipv4"] or ip_cidrs["ipv6"]:
        rule["ip_cidr"] = ip_cidrs["ipv4"] + ip_cidrs["ipv6"]
    if ports:
        rule["port"] = ports
    if port_ranges:
        rule["port_range"] = port_ranges

    json_data_srs = {
        "version": 3,
        "rules": [rule]
    }

    if route["routing"] in ["BYPASS", "BLOCK"]:
        routing_action = {
            "BYPASS": {"do": 1, "status": 1},
            "BLOCK": {"do": 0, "status": 1},
        }[route["routing"]]
    else:
        routing_action = {"do": 3, "via": route["routing"], "status": 1}

    json_data_routing = {
        "group": {
            "group": f"{i:03}_{route['name']}",
            "action": routing_action
        },
        "rules": []
    }

    for domain in domains["domain"]:
        json_data_routing["rules"].append({"PK": domain, "action": routing_action})
    for domain_suffix in rule["domain_suffix"]:
        if not domain_suffix.startswith('.'):
            json_data_routing["rules"].append({"PK": domain_suffix, "action": routing_action})
        else:
            json_data_routing["rules"].append({"PK": f"*{domain_suffix}", "action": routing_action})

    return json_data_srs, json_data_routing


def compile_srs(json_data, output_file):
    with open("temp.json", "w") as f:
        json.dump(json_data, f)
    subprocess.run(["sing-box", "rule-set", "compile", "temp.json", "-o", output_file])

def generate_rule_set(config):
    rule_set = []
    for i, route in enumerate(config["route"]):
        name = route["name"]
        rule_set.append({
            "type": "remote",
            "format": "binary",
            "update_interval": "3h",
            "tag": f"{i:03}_{name}",
            "url": f"https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/{name}.srs"
        })
    with open("rule_set.json", "w") as f:
        json.dump({"rule_set": rule_set}, f, indent=4)

def generate_readme(config):
    with open("README.tmp", "r") as f:
        readme_template = f.read()
    srs_files_section = "\n".join([f"* [{route['name']}](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/{route['name']}.srs)" for route in config["route"]])
    readme = readme_template.replace("{% for file in files %}\n* [{{ file }}](https://cdn.jsdelivr.net/gh/malikshi/route@release/srs/convert/{{ file }})\n{% endfor %}", srs_files_section)
    with open("README.md", "w") as f:
        f.write(readme)


def main():
    try:
        with open("config.json") as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error parsing config.json: {e}")
        return

    output_dir = "release"
    os.makedirs(os.path.join(output_dir, "srs", "convert"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "srs", "json"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "json"), exist_ok=True)
    srs_dir = os.path.join(output_dir, "srs", "convert")
    srs_json_dir = os.path.join(output_dir, "srs", "json")
    json_dir = os.path.join(output_dir, "json")

    added_rules = set()
    for i, route in enumerate(config["route"]):
        name = route["name"]
        json_data_srs, json_data_routing = generate_json(i, route)
        output_file_srs = os.path.join(srs_dir, f"{name}.srs")
        output_file_srs_json = os.path.join(srs_json_dir, f"{name}.json")
        output_file_json = os.path.join(json_dir, f"{i:03}_{name}.json")

        compile_srs(json_data_srs, output_file_srs)
        with open(output_file_srs_json, "w") as f:
            json.dump(json_data_srs, f)

        # Filter out duplicate rules
        filtered_rules = []
        for rule in json_data_routing["rules"]:
            if rule["PK"] not in added_rules:
                filtered_rules.append(rule)
                added_rules.add(rule["PK"])
        json_data_routing["rules"] = filtered_rules

        with open(output_file_json, "w") as f:
            json.dump(json_data_routing, f)
    
    generate_rule_set(config)
    generate_readme(config)

if __name__ == "__main__":
    main()