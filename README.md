# Deploy


## Structure
```shell
                       \\\\\\\\\\\\\\\\\\
                       || Supervisord  ||
                       \\\\\\\\\\\\\\\\\\
                               ↑ 
                      ┌--------┴---------┐          \\\\\\\\\\\\\\
                ┌-->  || supervisor rpc ||     ┌--> ||   Repo1  ||    
                |     \\\\\\\\\\\\\\\\\\\\     |    \\\\\\\\\\\\\\ 
                |     ||     git rpc    || ----|    
                |     |------------------|     |    \\\\\\\\\\\\\\
                ├-->  ||     Agent      ||     └--> ||  Repo2   ||
                |     \\\\\\\\\\\\\\\\\\\\          \\\\\\\\\\\\\\       
                |                   
 \\\\\\\\\\\    | 
 || Admin || ---┤
 \\\\\\\\\\\    |   
                |  
                |     \\\\\\\\\\\\\\\\\\\\          \\\\\\\\\\\\\\
                ├-->  ||      Agent     ||     ┌--> ||   Repo1  ||    
                |     |------------------|     |    \\\\\\\\\\\\\\ 
                |     ||     git rpc    || ----|    
                |     \\\\\\\\\\\\\\\\\\\\     |    \\\\\\\\\\\\\\
                └-->  || supervisor rpc ||     └--> ||  Repo2   ||
                      └--------┬---------┘          \\\\\\\\\\\\\\       
                               ↓                
                        \\\\\\\\\\\\\\\\\
                        || Supervisord ||
                        \\\\\\\\\\\\\\\\\ 
        
```

### Agent Supervisor
```shell
[inet_http_server]
port = 127.0.0.1:9001
username = user
password = 123
```


### Admin&Agent .env
```shell
# app role: admin or agent
APP_ROLE=admin
#APP_ROLE=agent
# (only agent need) local absolute directory of git repositories
LOCAL_GIT_REPOS="repo1:/var/www/.../repo1,repo2:/var/www/.../repo2"
# (only admin need) local supervisor xmlrpc
SUPERVISOR_URLS=http://user:123@127.0.0.1:9001/RPC2,http://user:123@127.0.0.1:9001/RPC2
# (only admin need) all machine info (host/repo)
# make sure host same with SUPERVISOR_URLS`s host
GIT_REPOS="127.0.0.1/repo1,127.0.0.1/repo2"
```

### Deploy
```shell
# adjust app role in .env, then
sh depoly.sh
```