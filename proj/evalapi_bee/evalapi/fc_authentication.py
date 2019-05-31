import fc


def generate_auth(service_name, function_name, invocation_type='Sync',
                  log_type='None', trace_id=None, key='LTAIZtlslPls3GEn', secret='EFE5Byj2r1aO6RPbTem5mUBFOz3klS'):
    endpoint = '30691700.cn-beijing.fc.aliyuncs.com'
    client = fc.Client(accessKeyID=key, accessKeySecret=secret,
                       endpoint=endpoint)
    method = 'POST'
    path = '/{0}/services/{1}/functions/{2}/invocations'.format('2016-08-15', service_name, function_name)
    headers = client._build_common_headers()
    headers['x-fc-invocation-type'] = invocation_type
    headers['x-fc-log-type'] = log_type
    if trace_id:
        headers['x-fc-trace-id'] = trace_id

    # Sign the request and set the signature to headers.
    headers['Authorization'] = client.auth.sign_request(method, path, headers)
    print('http://' + endpoint + path)
    print('headers:')
    for k, v in headers.items():
        print('%s:%s' % (k, v))


if __name__ == '__main__':
    import sys

    if len(sys.argv) > 3:
        key = sys.argv[3]
        secret = sys.argv[4]
        generate_auth(sys.argv[1], sys.argv[2], key=sys.argv[3], secret=sys.argv[4])
    else:
        generate_auth(sys.argv[1], sys.argv[2])

