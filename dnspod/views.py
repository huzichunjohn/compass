import json
import requests
from django.shortcuts import render
from django.http import HttpResponse

def get_all_lines(domain_id, domain_grade="D_Free"):
    headers = {
        "UserAgent": "Dnspod client/0.0.1 (huzichunjohn@126.com)"
    }

    payload = {
        "login_token": "23432,7a266b74cdceb1dd49c97e860dbce685",
        "format": "json",
        "lang": "cn",
        "domain_id": domain_id,
        "domain_grade": domain_grade
    }

    try:
        r = requests.post("https://dnsapi.cn/Record.Line", data=payload, headers=headers, timeout=1)  
        r.raise_for_status()
        data = r.json()
        if data["status"]["code"] == "1":
            return data["lines"]
    except requests.exceptions.ConnectionError:
        # log
        pass
    except requests.exceptions.Timeout:
        # log
        pass
    except requests.exceptions.HTTPError:
        # log
        pass
    except Exception as e:
        # log 
        pass
    return []

def index(request):
    headers = {
        "UserAgent": "Dnspod client/0.0.1 (huzichunjohn@126.com)"
    }

    payload = {
        "login_token": "23432,7a266b74cdceb1dd49c97e860dbce685",
        "format": "json",
        "lang": "cn"
    }

    error = False
    domains = []
    detail = ""
    try:
        r = requests.post("https://dnsapi.cn/Domain.List", data=payload, headers=headers, timeout=1)  
        r.raise_for_status()
        data = r.json()
        if data["status"]["code"] == "1":
            for domain in data["domains"]:
                domains.append({
                    "id": int(domain["id"]),
                    "name": domain["name"],
                    "remark": domain["remark"]
                })
            
        else:
            error = True
            detail = data["status"]["message"]
    except requests.exceptions.ConnectionError:
        error = True
        detail = "connect error"

    except requests.exceptions.Timeout:
        error = True
        detail = "timeout"

    except requests.exceptions.HTTPError:
        error = True
        detail = "http error"

    except Exception as e:
        error = True
        detail = "unknown"

    return render(request, 'dnspod/index.html', {"domains": domains, "error": error, "detail": detail})

def get_records_by_domain_id(request, domain_id):
    lines = get_all_lines(domain_id)

    headers = {
        "UserAgent": "Dnspod client/0.0.1 (huzichunjohn@126.com)"
    }

    payload = {
        "login_token": "23432,7a266b74cdceb1dd49c97e860dbce685",
        "format": "json",
        "lang": "cn",
        "domain_id": domain_id
    }

    error = False
    records = []
    detail = ""
    try:
        r = requests.post("https://dnsapi.cn/Record.List", data=payload, headers=headers, timeout=1)
        r.raise_for_status()
        data = r.json()
        print data
        if data["status"]["code"] == "1":
            for record in data["records"]:
                records.append({
                    "id": record["id"],
                    "name": record["name"],
                    "type": record["type"],
                    "ttl": record["ttl"],
                    "line": record["line"],
                    "value": record["value"],
                    "remark": record["remark"],
                    "enabled": record["enabled"]
                })

        else:
            error = True
            detail = data["status"]["message"]
    except requests.exceptions.ConnectionError:
        error = True
        detail = "connect error"

    except requests.exceptions.Timeout:
        error = True
        detail = "timeout"

    except requests.exceptions.HTTPError:
        error = True
        detail = "http error"

    except Exception as e:
        raise
        error = True
        detail = "unknown"

    print records
    return render(request, 'dnspod/records.html', {"domain_id": domain_id, "records": records, "lines": lines, "error": error, "detail": detail})

def edit_record(request, domain_id, record_id):
    sub_domain = request.POST["sub_domain"]
    value = request.POST["value"]
    record_type = request.POST["record_type"]
    record_line = request.POST["record_line"]
    ttl = int(request.POST["ttl"])

    headers = {
        "UserAgent": "Dnspod client/0.0.1 (huzichunjohn@126.com)"
    }

    payload = {
        "login_token": "23432,7a266b74cdceb1dd49c97e860dbce685",
        "format": "json",
        "lang": "cn",
        "domain_id": int(domain_id),
        "record_id": record_id,
        "sub_domain": sub_domain,
        "value": value,
        "record_type": record_type,
        "record_line": record_line,
        "ttl": ttl
    }

    try:
        r = requests.post("https://dnsapi.cn/Record.Modify", data=payload, headers=headers, timeout=1)  
        r.raise_for_status()
        data = r.json()
        if data["status"]["code"] == "1":
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            return HttpResponse("error")
    except requests.exceptions.ConnectionError:
        # log
        raise
    except requests.exceptions.Timeout:
        # log
        raise
    except requests.exceptions.HTTPError:
        # log
        raise
    except Exception as e:
        # log
        raise

def delete_record(reqeust, domain_id, record_id):
    headers = {
        "UserAgent": "Dnspod client/0.0.1 (huzichunjohn@126.com)"
    }

    payload = {
        "login_token": "23432,7a266b74cdceb1dd49c97e860dbce685",
        "format": "json",
        "lang": "cn",
        "domain_id": int(domain_id),
        "record_id": record_id
    }

    try:
        r = requests.post("https://dnsapi.cn/Record.Remove", data=payload, headers=headers, timeout=1)
        r.raise_for_status()
        data = r.json()
        if data["status"]["code"] == "1":
            return HttpResponse(json.dumps(data), content_type="application/json")
        else:
            return HttpResponse("error")
    except requests.exceptions.ConnectionError:
        # log
        raise
    except requests.exceptions.Timeout:
        # log
        raise
    except requests.exceptions.HTTPError:
        # log
        raise
    except Exception as e:
        # log
        raise

def edit_record_status(request, domain_id, record_id):
    pass
