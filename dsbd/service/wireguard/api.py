import requests
import json

from dsbd.service.wireguard.models import Service


def wg_create(server, service):
    url = 'http://%s:%d/api/v1/peer' % (server.mgmt_ip, server.mgmt_port)
    ips = []
    if service.ipv4:
        ips.append(service.ipv4)
    if service.ipv6:
        ips.append(service.ipv6)
    requests.post(url, data=json.dumps({
        "public_key": service.public_key,
        "allowed_ips": ips
    }))


def wg_update(server, old_public_key, service):
    url = 'http://%s:%d/api/v1/peer' % (server.mgmt_ip, server.mgmt_port)
    ips = []
    if service.ipv4:
        ips.append(service.ipv4)
    if service.ipv6:
        ips.append(service.ipv6)
    requests.put(url, data=json.dumps({
        "old_public_key": old_public_key,
        "client": {
            "public_key": service.public_key,
            "allowed_ips": ips
        }
    }))


def wg_delete(server, public_key):
    url = 'http://%s:%d/api/v1/peer' % (server.mgmt_ip, server.mgmt_port)
    requests.delete(url, data=json.dumps({"public_key": public_key}))


def wg_all_delete(server):
    url = 'http://%s:%d/api/v1/peer/all' % (server.mgmt_ip, server.mgmt_port)
    requests.delete(url)


def wg_overwrite(server):
    url = 'http://%s:%d/api/v1/peer/all' % (server.mgmt_ip, server.mgmt_port)
    services = Service.objects.filter(service_id=server.id).all()
    clients = []
    for service in services:
        ips = []
        if not service.ipv4 and not service.ipv6:
            continue
        if service.ipv4:
            ips.append(service.ipv4)
        if service.ipv6:
            ips.append(service.ipv6)
        clients.append({
            "public_key": service.public_key,
            "allowed_ips": ips
        })
    requests.put(url, data=json.dumps({"clients": clients}))
