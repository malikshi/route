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
        else:
            # Remove any attributes that start with "@"
            parts = item.split()
            domain_info = parts[0]
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
    return domains, ip_cidrs


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


def generate_json(route):
    domains = {"domain": [], "domain_suffix": [], "domain_keyword": [], "domain_regex": []}
    ip_cidrs = {"ipv4": [], "ipv6": []}
    for source in route["list"]:
        if source["type"] == "v2ray":
            source_domains = process_v2ray_source(source["url"])
            source_ip_cidrs = []
        elif source["type"] == "clash":
            source_domains, source_ip_cidrs = process_clash_source(source["url"])
        elif source["type"] == "plain":
            source_domains, source_ip_cidrs = process_plain_source(source["list"])
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

    # Remove duplicates and sort
    for key in domains:
        domains[key] = sorted(list(set(domains[key])))
    ip_cidrs["ipv4"] = sorted(list(set(ip_cidrs["ipv4"])))
    ip_cidrs["ipv6"] = sorted(list(set(ip_cidrs["ipv6"])))

    rule = {
        key: domains[key]
        for key in domains
        if domains[key]
    }
    if ip_cidrs["ipv4"] or ip_cidrs["ipv6"]:
        rule["ip_cidr"] = ip_cidrs["ipv4"] + ip_cidrs["ipv6"]

    json_data_srs = {
        "version": 3,
        "rules": [rule]
    }

    rules = []
    for domain in domains["domain"]:
        rules.append({"PK": domain, "action": {"do": 3, "via": route["routing"], "status": 1}})
    for domain_suffix in domains["domain_suffix"]:
        rules.append({"PK": domain_suffix, "action": {"do": 3, "via": route["routing"], "status": 1}})

    json_data_routing = {
        "group": {
            "group": route["name"],
            "action": {
                "do": 3,
                "via": route["routing"],
                "status": 1
            }
        },
        "rules": rules
    }

    return json_data_srs, json_data_routing


def compile_srs(json_data, output_file):
    with open("temp.json", "w") as f:
        json.dump(json_data, f)
    subprocess.run(["sing-box", "rule-set", "compile", "temp.json", "-o", output_file])


def main():
    try:
        with open("config.json") as f:
            config = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error parsing config.json: {e}")
        return

    output_dir = "release"
    os.makedirs(os.path.join(output_dir, "srs"), exist_ok=True)
    os.makedirs(os.path.join(output_dir, "json"), exist_ok=True)
    srs_dir = os.path.join(output_dir, "srs")
    json_dir = os.path.join(output_dir, "json")

    for route in config["route"]:
        name = route["name"]
        json_data_srs, json_data_routing = generate_json(route)
        output_file_srs = os.path.join(srs_dir, f"{name}.srs")
        compile_srs(json_data_srs, output_file_srs)
        output_file_json = os.path.join(json_dir, f"{name}.json")
        with open(output_file_json, "w") as f:
            json.dump(json_data_routing, f)

if __name__ == "__main__":
    main()