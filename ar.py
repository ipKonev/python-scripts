import ansible_runner

r=ansible_runner.run(private_data_dir='/root/IAAC/corp_res/ansible/', playbook='corp-playbook.yml',extra_vars="{'addr': }")
print(f'{r.status}: {r.rc}')
