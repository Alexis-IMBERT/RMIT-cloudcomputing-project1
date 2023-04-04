# Mise en production du projet  

1. Creation de la VM EC2
2. Connexion à la VM en SSH
    - téléchager les clé ssh
    - changer les permission sur la clé .pem
    ```shell
    chmod 400 ./labuser.pem
    ``` 
    - connexion en ssh
    ```bash
    ssh -i labuser.pem ubuntu@[ip/DNS]
    ```
3. git et python sont déja installé pip n'est pas installé  
    ```shell
    curl -O https://bootstrap.pypa.io/get-pip.py
    sudo python3 get-pip.py --user
    sudo echo "export PATH=LOCAL_PATH:$PATH" >> ~/.profile
    sudo source ~/.profile
    sudo pip install awsebcli --upgrade --user
    sudo pip install flask httpx

    ```
4. Téléchargement depuis le git
    ```bash
    git clone git@gitlab.insa-rouen.fr:aimbert/cloudcomputing-project1.git
    git checkout frontend 
    ```
