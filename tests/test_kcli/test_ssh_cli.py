import subprocess as sub

try:
    o_t = sub.check_output(['ssh' 'root@172.23.28.124'])
    print(o_t.decode('utf-8'))
except Exception as e:
    #print(e.output)
    #print(e.returncode)
    pass
