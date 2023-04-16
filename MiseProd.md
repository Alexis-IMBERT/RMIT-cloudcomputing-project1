# Mise en production du projet  

1. Create EC2 VM
2. Connect to the EC2 VM by ssh : 
    - download ssh key 
    - change permission on .pem key
    ```shell
    chmod 400 ./labsuser.pem
    ``` 
    - connect ssh 
    ```bash
    ssh -i labsuser.pem ubuntu@[ip/DNS]
    ```
3. git and python are already install, pip is not :
    ```shell
    sudo -i
    curl -O https://bootstrap.pypa.io/get-pip.py
    python3 get-pip.py --user
     echo "export PATH=LOCAL_PATH:$PATH" >> ~/.profile
    source ~/.profile
    pip install awsebcli --upgrade --user
    pip install flask httpx boto3

    ```
4. Download of the project from the git
    ```bash
    git clone git@gitlab.insa-rouen.fr:aimbert/cloudcomputing-project1.git
    ```
