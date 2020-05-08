#!/usr/bin/env python
import yaml

from argparse import ArgumentParser
from dataclasses import dataclass
from dns.resolver import Resolver, NoNameservers
from prometheus_client import make_wsgi_app, Summary
from prometheus_client.core import GaugeMetricFamily, REGISTRY
from wsgiref.simple_server import make_server

parser = ArgumentParser()
parser.add_argument('-c', '--config', default='/etc/dnsttl_reporter/config.yml')

COLLECT_TIME = Summary('dnsrecordttl_collect_time', 'Time spent collecting ttl records')

RESOLVERS = set()
QUERIES = set()

def parse_config(config_file):
    with open(config_file) as f:
        config = yaml.safe_load(f)

    RESOLVERS.update(make_resolver(r) for r in config['resolvers'])
    QUERIES.update((tuple(q) for q in config['queries']))


@dataclass
class QueryResult:
    query: str
    rr: str
    resolver: str
    ttl: int


def make_resolver(nameserver):
    resolver = Resolver(configure=False)
    resolver.nameservers = [nameserver]
    return resolver


def make_queries():
    for query in QUERIES:
        for resolver in RESOLVERS:
            try:
                result = resolver.query(*query)
            except NoNameservers:
                continue
            yield QueryResult(
                query=query[0],
                rr=query[1],
                resolver=resolver.nameservers[0],
                ttl=result.ttl,
            )


class DnsRecordTTLCollector:
    @COLLECT_TIME.time()
    def collect(self):
        metric = GaugeMetricFamily(
            'dns_record_ttl',
            'TTL for a dns record',
            labels=(
                'rr',
                'query',
                'nameserver',
            ),
        )

        queries = make_queries()
        for query in queries:
            metric.add_metric(
                (
                    query.rr,
                    query.query,
                    query.resolver,
                ),
                query.ttl,
            )
        yield metric


REGISTRY.register(DnsRecordTTLCollector())
app = make_wsgi_app()


def main():
    import os
    args = parser.parse_args()

    parse_config(args.config)

    addr = os.getenv('ADDR', 'localhost')
    port = int(os.getenv('PORT', '8000'))
    server = make_server(addr, port, app)
    print(f'Listening on: {addr}:{port}')
    server.serve_forever()


if __name__ == '__main__':
    main()
