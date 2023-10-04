import fileinput

with open(r'configs/helm-charts/cloud-docs/Chart.yaml', 'r') as chart:
    data = chart.readlines()
    num = -1
    for line in data:
        line = line.replace('\n','')
        num = num + 1
        if 'version:' in line:
            version = line
            ver = line.split('.')
            ver[1] = str(int(ver[1]) + 1)
            new_ver = '.'.join(ver)
            data[num] = line.replace(version, new_ver)

with open('configs/helm-charts/cloud-docs/Chart.yaml', 'w') as chart:
    chart.write(''.join(data))