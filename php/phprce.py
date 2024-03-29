import os
import re
import json

def scan_file(file_path):
    with open(file_path, 'r') as f:
        contents = f.read()

    result = {}

    if re.search(r'<\?php', contents):
        if re.search(r'eval\(|exec\(|passthru\(|system\(|shell_exec\(|popen\(', contents):
            result['status'] = 'Vulnerable'
            rce_vuln_lines = []
            lines = contents.split('\n')
            for i, line in enumerate(lines):
                if re.search(r'eval\(|exec\(|passthru\(|system\(|shell_exec\(|popen\(', line):
                    rce_vuln_lines.append(i+1)
            if rce_vuln_lines:
                result['vulnerable_lines'] = rce_vuln_lines
        else:
            result['status'] = 'Input tracking found'
    else:
        pass

    result['file_path'] = file_path

    return result

def php_scan_directory_rce(path):
    results = []

    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.php'):
                full_path = os.path.join(root, file)
                result = scan_file(full_path)
                results.append(result)

    output = json.dumps(results, indent=4)
    print(output)
