#!/bin/python3 -u
# -*- coding: utf8 -*-
import json
import sys

import time
from aliyunsdkalidns.request.v20150109 import DescribeDomainRecordInfoRequest, UpdateDomainRecordRequest
from aliyunsdkcore.client import AcsClient
from aliyunsdkecs.request.v20140526 import DescribeSecurityGroupAttributeRequest, RevokeSecurityGroupEgressRequest, \
    RevokeSecurityGroupRequest, AuthorizeSecurityGroupRequest, AuthorizeSecurityGroupEgressRequest


ACCESSKEY = sys.argv[1]
SECRET = sys.argv[2]
ENDPOINT = sys.argv[3]
RECORDID = sys.argv[4]
GROUPID = sys.argv[5]
IP = sys.argv[6]


client = AcsClient(
    ACCESSKEY,
    SECRET,
    ENDPOINT)


def descRecord(recordId):
    request = DescribeDomainRecordInfoRequest.DescribeDomainRecordInfoRequest()
    request.set_RecordId(recordId)
    response = client.do_action_with_exception(request)
    return json.loads(response)


def updateRecord(record):
    recordId = record.get('RecordId').encode('UTF-8')
    RR = record.get('RR').encode('UTF-8')
    Type = record.get('Type').encode('UTF-8')
    value = record.get('Value').encode('UTF-8')
    ttl = record.get('TTL')
    priority = record.get('priority')
    line = record.get('Line').encode('UTF-8')

    request = UpdateDomainRecordRequest.UpdateDomainRecordRequest()
    request.set_RecordId(recordId)
    request.set_RR(RR)
    request.set_Type(Type)
    request.set_Value(value)
    request.set_TTL(ttl)
    if priority != None:
        request.set_Priority(priority.encode('UTF-8'))
    request.set_Line(line)
    response = client.do_action_with_exception(request)
    return json.loads(response)


def execDdns(ip):
    record = descRecord(RECORDID)
    record['Value']=ip
    updateRecord(record)
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), ' - ', 'Update Record Success')


def descSecurityGroup(groupId):
    request = DescribeSecurityGroupAttributeRequest.DescribeSecurityGroupAttributeRequest()
    request.set_SecurityGroupId(groupId)
    response = client.do_action_with_exception(request)
    return json.loads(response)


def revokeIngress(groupId, permission):
    requestRevoke = RevokeSecurityGroupRequest.RevokeSecurityGroupRequest()
    requestRevoke.set_SecurityGroupId(groupId)
    requestRevoke.set_SourceCidrIp(permission['SourceCidrIp'])
    requestRevoke.set_IpProtocol(permission['IpProtocol'])
    requestRevoke.set_PortRange(permission['PortRange'])
    responseRevoke = client.do_action_with_exception(requestRevoke)
    return json.loads(responseRevoke)


def revokeEgress(groupId, permission):
    requestRevoke = RevokeSecurityGroupEgressRequest.RevokeSecurityGroupEgressRequest()
    requestRevoke.set_SecurityGroupId(groupId)
    requestRevoke.set_DestCidrIp(permission['DestCidrIp'])
    requestRevoke.set_IpProtocol(permission['IpProtocol'])
    requestRevoke.set_PortRange(permission['PortRange'])
    responseRevoke = client.do_action_with_exception(requestRevoke)
    return json.loads(responseRevoke)


def authIngress(groupId, ip):
    requestAuth = AuthorizeSecurityGroupRequest.AuthorizeSecurityGroupRequest()
    # requestAuth.set_Description()
    requestAuth.set_SecurityGroupId(groupId)
    requestAuth.set_PortRange('-1/-1')
    requestAuth.set_Policy('Accept')
    requestAuth.set_NicType('internet')
    requestAuth.set_Priority(1)
    requestAuth.set_SourceCidrIp(ip)
    requestAuth.set_IpProtocol("ALL")
    requestAuth.set_SourcePortRange('-1/-1')
    responseAuth = client.do_action_with_exception(requestAuth)
    return json.loads(responseAuth)


def authEgress(groupId, ip):
    requestAuth = AuthorizeSecurityGroupEgressRequest.AuthorizeSecurityGroupEgressRequest()
    requestAuth.set_SecurityGroupId(groupId)
    requestAuth.set_PortRange('-1/-1')
    requestAuth.set_Policy('Accept')
    requestAuth.set_NicType('internet')
    requestAuth.set_Priority(1)
    requestAuth.set_DestCidrIp(ip)
    requestAuth.set_IpProtocol('ALL')
    requestAuth.set_SourcePortRange('-1/-1')
    responseAuth = client.do_action_with_exception(requestAuth)
    return json.loads(responseAuth)


def execAuth(ip):
    securityGroup = descSecurityGroup(GROUPID)
    permissions = securityGroup['Permissions']['Permission']
    for permission in permissions:
        if permission['Direction'] == 'ingress':
            revokeIngress(securityGroup['SecurityGroupId'], permission)
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), ' - ', 'Revoke Ingress Permission Success')
        else:
            revokeEgress(securityGroup['SecurityGroupId'], permission)
            print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), ' - ', 'Revoke Egress Permission Success')

    authIngress(securityGroup['SecurityGroupId'], ip)
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), ' - ', 'Auth Ingress Permission Success')
    authEgress(securityGroup['SecurityGroupId'], ip)
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), ' - ', 'Auth Egress Permission Success')

# main
try:
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), ' - ', 'Dynamic DNS Start.')
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), ' - ', 'IP Address is ', IP)
    execDdns(IP)
    execAuth(IP)
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()), ' - ', 'Dynamic DNS End.')
except BaseException as e:
    print(e.message)
    sys.exit(-1)
sys.exit(1)
