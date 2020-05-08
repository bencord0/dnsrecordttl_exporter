# dnsrecordttl_exporter

A Prometheus style metrics exporter for tracking TTLs of DNS Records

## Install

    $ sudo eselect repository add bencord0 git https://github.com/bencord0/portage-overlay
    $ sudo emaint sync -r bencord0
    $ sudo emerge app-metrics/dnsrecordttl_exporter

    $ sudo systemctl enable --now dnsrecordttl_exporter.service


## Configuration

### /etc/dnsrecordttl_exporter/env

```
ADDR=localhost
PORT=8000
```

### /etc/dnsrecordttl_exporter/config.yml

```
resolvers:
    - '1.1.1.1' # Cloudflare
    - '8.8.8.8' # Google

queries:
    - ['google.com', 'ns']
    - ['gmail.com', 'mx']
    - ['www.google.com', 'a']
    - ['www.google.com', 'aaaa']
```

### /etc/prometheus/prometheus.yml

```
...
scrape_configs:
  - job_name: 'prometheus'
    - targets:
      ...
      - 'localhost:8000'
      ...

  - job_name: ...
    ...
...
```
