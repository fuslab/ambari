#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@author: whoami
@license: Apache Licence 2.0
@contact: realXuJiang@foxmail.com
@site: http://www.jikelab.com
@software: PyCharm
@file: utils.py
@time: 2018-03-29 09:40
"""

import json
from xml.dom import minidom
import re

def json2xml(json_data):
    #obj = json.loads(json_data)

    xdoc = minidom.Document()

    e = xdoc.createElement('configuration')
    xdoc.appendChild(e)

    for k,v in json_data.items():
        a = xdoc.createElement('property')

        b = xdoc.createElement('name')
        bv = xdoc.createTextNode(k)
        b.appendChild(bv)
        a.appendChild(b)

        c = xdoc.createElement('value')
        cv = xdoc.createTextNode(str(v))
        c.appendChild(cv)
        a.appendChild(c)

        e.appendChild(a)

    return e.toprettyxml(encoding='utf-8')

def clickhouseConfigToXML(json_string):
    doc = minidom.parseString(json2xml(json_string))

    root = doc.documentElement

    employees = root.getElementsByTagName('property')

    xdoc = minidom.Document()

    e = xdoc.createElement('yandex')
    xdoc.appendChild(e)
    for employee in employees:
        nameNode = employee.getElementsByTagName('name')[0].childNodes[0].nodeValue
        valueNode = employee.getElementsByTagName('value')[0].childNodes[0].nodeValue

        if nameNode == 'macros':
            a = xdoc.createElement(nameNode)
            a.setAttribute('incl', valueNode)
            a.setAttribute('optional', 'true')
            e.appendChild(a)

        elif nameNode == 'zookeeper':
            a = xdoc.createElement(nameNode)
            a.setAttribute('incl', valueNode)
            a.setAttribute('optional', 'true')
            e.appendChild(a)

        elif nameNode == 'remote_servers':
            a = xdoc.createElement(nameNode)
            a.setAttribute('incl', valueNode)
            e.appendChild(a)

        elif nameNode == 'clickhouse_logs_config':
            # convert string dict to dict type
            obj = json.loads(str(valueNode))

            for k, v in obj.items():
                a = xdoc.createElement(k)
                for x, y in v.items():
                    b = xdoc.createElement(x)
                    bv = xdoc.createTextNode(y)
                    b.appendChild(bv)
                    a.appendChild(b)

                e.appendChild(a)
                
        elif nameNode == 'distributed_ddl_config':
            # convert string dict to dict type
            obj = json.loads(str(valueNode))

            for k, v in obj.items():
                a = xdoc.createElement(k)
                for x, y in v.items():
                    b = xdoc.createElement(x)
                    bv = xdoc.createTextNode(y)
                    b.appendChild(bv)
                    a.appendChild(b)

                e.appendChild(a)

        else:
            Ename = xdoc.createElement(nameNode)
            Vname = xdoc.createTextNode(valueNode)
            Ename.appendChild(Vname)
            e.appendChild(Ename)

    return xdoc.toprettyxml(encoding='utf-8')

def clickhouseMetrikaToXML(tcp_port, user, password, ck_hosts, zk_hosts, 
                           clickhouse_remote_servers, hostname,
                           zookeeper_servers,json_string):
    doc = minidom.parseString(json2xml(json_string))
    root = doc.documentElement

    employees = root.getElementsByTagName('property')

    xdoc = minidom.Document()

    e = xdoc.createElement('yandex')
    xdoc.appendChild(e)

    for employee in employees:
        # get xml object elements name and value
        nameNode = employee.getElementsByTagName('name')[0].childNodes[0].nodeValue
        valueNode = employee.getElementsByTagName('value')[0].childNodes[0].nodeValue

        if nameNode == 'internal_replication':
            shard_internal_replication_key = nameNode
            shard_internal_replication_value = valueNode

        elif nameNode == 'ck_cluster_name':

            a = xdoc.createElement(clickhouse_remote_servers)

            b = xdoc.createElement(valueNode)
            a.appendChild(b)

            for ck_host in ck_hosts:
                c = xdoc.createElement('shard')
                b.appendChild(c)

                d = xdoc.createElement(shard_internal_replication_key)
                dv = xdoc.createTextNode(shard_internal_replication_value)
                d.appendChild(dv)
                c.appendChild(d)

                d = xdoc.createElement('replica')
                c.appendChild(d)

                f = xdoc.createElement('host')
                fv = xdoc.createTextNode(ck_host)
                f.appendChild(fv)
                d.appendChild(f)

                g = xdoc.createElement('user')
                gv = xdoc.createTextNode(user)
                g.appendChild(gv)
                d.appendChild(g)

                h = xdoc.createElement('password')
                hv = xdoc.createTextNode(password)
                h.appendChild(hv)
                d.appendChild(h)

                i = xdoc.createElement('port')
                iv = xdoc.createTextNode(tcp_port)
                i.appendChild(iv)
                d.appendChild(i)

                e.appendChild(a)

        elif nameNode == 'networks':
            # convert string dict to dict type
            obj = json.loads(str(valueNode))
            
            a = xdoc.createElement(nameNode)
            for k, v in obj.items():
                b = xdoc.createElement(k)
                bv = xdoc.createTextNode(v)
                b.appendChild(bv)

                a.appendChild(b)

            e.appendChild(a)

        elif nameNode == 'clickhouse_compression':
            # convert string dict to dict type
            obj = json.loads(str(valueNode))

            a = xdoc.createElement(nameNode)

            for k, v in obj.items():
                b = xdoc.createElement(k)
                for x, y in v.items():
                    c = xdoc.createElement(x)
                    cv = xdoc.createTextNode(y)
                    c.appendChild(cv)

                    b.appendChild(c)

                a.appendChild(b)

            e.appendChild(a)

        elif nameNode == 'macros_replica':
            # convert string dict to dict type
            obj = json.loads(str(valueNode))

            for k, v in obj.items():
                a = xdoc.createElement(k)
                for x, y in v.items():
                    b = xdoc.createElement(x)
                    bv = None
                    if x == 'replica':
                        bv = xdoc.createTextNode(hostname)
                    else:
                        bv = xdoc.createTextNode(y)
                    b.appendChild(bv)
                    a.appendChild(b)

            e.appendChild(a)

        elif nameNode == 'zookeeper_connect':
            a = xdoc.createElement(zookeeper_servers)

            if len(zk_hosts) > 1:

                i = 1
                if i < len(zk_hosts):
                    for host in zk_hosts:
                        b = xdoc.createElement('node')
                        b.setAttribute('index', str(i))

                        c = xdoc.createElement('host')
                        cv = xdoc.createTextNode(host)
                        c.appendChild(cv)
                        b.appendChild(c)

                        d = xdoc.createElement('port')
                        dv = xdoc.createTextNode('2181')
                        d.appendChild(dv)
                        b.appendChild(d)

                        a.appendChild(b)
                        i = i + 1
            else:
                for host in zk_hosts:
                    b = xdoc.createElement('node')
                    b.setAttribute('index', '1')

                    c = xdoc.createElement('host')
                    cv = xdoc.createTextNode(host)
                    c.appendChild(cv)
                    b.appendChild(c)

                    d = xdoc.createElement('port')
                    dv = xdoc.createTextNode('2181')
                    d.appendChild(dv)
                    b.appendChild(d)

                    a.appendChild(b)

            e.appendChild(a)

    return xdoc.toprettyxml(encoding='utf-8')


# Thrown on any dictionary error
class Dict2XMLException(Exception):
    pass

def _dict_sort_key(key_value):
    key = key_value[0]
    match = re.match('(\d+)__.*', key)
    return match and int(match.groups()[0]) or key

_iter_dict_sorted = lambda dic: sorted(
    dic.iteritems(), key=(lambda key_value: _dict_sort_key(key_value))
)

def _remove_order_id(key):
    match = re.match('\d+__(.*)', key)
    return match and match.groups()[0] or key

DATATYPE_ROOT_DICT = 0
DATATYPE_KEY = 1
DATATYPE_ATTR = 2
DATATYPE_ATTRS = 3

def _check_errors(value, data_type):
    if data_type == DATATYPE_ROOT_DICT:
        if isinstance(value, dict):
            values = value.values()
            if len(values) != 1:
                raise Dict2XMLException(
                    'Must have exactly one root element in the dictionary.')
            elif isinstance(values[0], list):
                raise Dict2XMLException(
                    'The root element of the dictionary cannot have a list as value.')
        else:
            raise Dict2XMLException('Must pass a dictionary as an argument.')

    elif data_type == DATATYPE_KEY:
        if not isinstance(value, basestring):
            raise Dict2XMLException('A key must be a string.')

    elif data_type == DATATYPE_ATTR:
        (attr, attrValue) = value
        if not isinstance(attr, basestring):
            raise Dict2XMLException('An attribute\'s key must be a string.')
        if not isinstance(attrValue, basestring):
            raise Dict2XMLException('An attribute\'s value must be a string.')

    elif data_type == DATATYPE_ATTRS:
        if not isinstance(value, dict):
            raise Dict2XMLException('The first element of a tuple must be a dictionary '
                                    'with a set of attributes for the main element.')

# Recursive core function
def _buildXMLTree(rootXMLElement, key, content, document):
    _check_errors(key, DATATYPE_KEY)
    keyElement = document.createElement(_remove_order_id(key))

    if isinstance(content, tuple) and len(content) == 2:
        (attrs, value) = content
    else:
        (attrs, value) = ({}, content)

    _check_errors(attrs, DATATYPE_ATTRS)
    for (attr, attrValue) in attrs.iteritems():
        _check_errors((attr, attrValue), DATATYPE_ATTR)
        keyElement.setAttribute(attr, '%s' % attrValue)

    if isinstance(value, basestring):
        # Simple text value inside the node
        keyElement.appendChild(document.createTextNode('%s' % value))
        rootXMLElement.appendChild(keyElement)

    elif isinstance(value, dict):
        # Iterating over the children
        for (k, cont) in _iter_dict_sorted(value):
            # Recursively parse the subdictionaries
            _buildXMLTree(keyElement, k, cont, document)
        rootXMLElement.appendChild(keyElement)

    elif isinstance(value, list):
        # Recursively replicate this key element for each value in the list
        for subcontent in value:
            _buildXMLTree(rootXMLElement, key, subcontent, document)

    else:
        raise Dict2XMLException('Invalid value.')

def clickhouseUsersToXML(json_data):
    # convert string dict to dict type
    import ast
    obj = ast.literal_eval(json_data)

    document = minidom.Document()

    # Root call of the recursion
    _check_errors(obj, DATATYPE_ROOT_DICT)
    (key, content) = obj.items()[0]
    _buildXMLTree(document, key, content, document)

    return document.toprettyxml(encoding='utf-8')

if __name__ == '__main__':
    #json_data = open('config.json').read()
    #print clickhouseConfigToXML(json2xml(json_data))

    #metrika_config = open('metrika.json').read()
    #metrika_config_json = json2xml(metrika_config)
    #print clickhouseMetrikaToXML(tcp_port='9000', user='admin', password='admin', ck_hosts=['node1', 'node2', 'node3'],
    #                      zk_hosts=['node1', 'node2', 'node3'], clickhouse_remote_servers='clickhouse_remote_servers',
    #                      hostname='node1', zookeeper_servers='zookeeper-servers',xml_string=metrika_config_json)
    #users_config = open('users.json').read()
    #print clickhouseUsersToXML(users_config)
    pass