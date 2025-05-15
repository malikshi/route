import json
import requests
import subprocess

def process_v2ray_source(url):
    response = requests.get(url)
    lines = response.text.splitlines()
    domains = []
    for line in lines:
        line = line.strip()
        if line.startswith("include:"):
            included_file = line.split(":")[1].strip()
            # Assume included files are in the same directory
            included_url = url.replace(url.split("/")[-1], included_file)
            included_domains = process_v2ray_source(included_url)
            domains.extend(included_domains)
        elif line.startswith("domain:"):
            domain = line.split(":")[1].strip().split()[0]
            domains.append(domain)
        elif line.startswith("keyword:"):
            keyword = line.split(":")[1].strip()
            domains.append(f"keyword:{keyword}")
        elif line.startswith("regexp:"):
            regexp = line.split(":")[1].strip()
            domains.append(f"regexp:{regexp}")
        elif line.startswith("full:"):
            full_domain = line.split(":")[1].strip()
            domains.append(full_domain)
    return domains

def process_clash_source(url):
    response = requests.get(url)
    lines = response.text.splitlines()
    domains = []
    for line in lines:
        line = line.strip()
        if line.startswith("DOMAIN-SUFFIX,"):
            domain_suffix = line.split(",")[1].strip()
            domains.append(f"suffix:{domain_suffix}")
        elif line.startswith("DOMAIN,"):
            domain = line.split(",")[1].strip()
            domains.append(domain)
        elif line.startswith("DOMAIN-KEYWORD,"):
            keyword = line.split(",")[1].strip()
            domains.append(f"keyword:{keyword}")
    return domains

def process_plain_source(list):
    domains = []
    for item in list:
        if item.startswith("suffix:"):
            domain_suffix = item.split(":")[1].strip()
            domains.append(f"suffix:{domain_suffix}")
        else:
            domains.append(item)
    return domains

def generate_json(route):
    domains = {"domain": [], "domain_suffix": [], "domain_keyword": [], "domain_regex": []}
    for source in route["list"]:
        if source["type"] == "v2ray":
            source_domains = process_v2ray_source(source["url"])
        elif source["type"] == "clash":
            source_domains = process_clash_source(source["url"])
        elif source["type"] == "plain":
            source_domains = process_plain_source(source["list"])
        for domain in source_domains:
            if domain.startswith("suffix:"):
                domains["domain_suffix"].append(domain.split(":")[1])
            elif domain.startswith("keyword:"):
                domains["domain_keyword"].append(domain.split(":")[1])
            elif domain.startswith("regexp:"):
                domains["domain_regex"].append(domain.split(":")[1])
            else:
                domains["domain"].append(domain)
    # Remove duplicates
    for key in domains:
        domains[key] = list(set(domains[key]))
    json_data = {
        "version": 3,
        "rules": [
            {key: domains[key] for key in domains if domains[key]}
        ]
    }
    return json_data

def compile_srs(json_data, output_file):
    with open("temp.json", "w") as f:
        json.dump(json_data, f)
    subprocess.run(["sing-box", "rule-set", "compile", "temp.json", "-o", output_file])

def main():
    with open("config.json") as f:
        config = json.load(f)
    for route in config["route"]:
        name = route["name"]
        json_data = generate_json(route)
        output_file = f"{name}.srs"
        compile_srs(json_data, output_file)

if __name__ == "__main__":
    main()