import subprocess
def install_sshpass():
    try:
        subprocess.run(["sudo", "apt-get", "install", "-y", "sshpass"], check=True)
        print("install ssh pass thành công.")
    except subprocess.CalledProcessError as e:
        print(f"Error installing sshpass: {e}")
def check_ssh_connection(username, server_ip, ssh_password):
    try:
        subprocess.run(["sshpass", "-V"], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print("chưa install ssh pass")
        install_sshpass()

    try:
        result = subprocess.run(["sshpass", "-p", ssh_password, "ssh", "-o", "StrictHostKeyChecking=no", "-q", f"{username}@{server_ip}", "exit"], check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError:
        return False
def download_file_from_server(remote_path, local_path, username, server_ip, ssh_password):
    try:
        subprocess.run(["sshpass", "-p", ssh_password, "scp", f"{username}@{server_ip}:{remote_path}", local_path], check=True)
        print(f"download file thành công {server_ip}:{remote_path} to {local_path}")
    except subprocess.CalledProcessError as e:
        print(f"Lỗi: {e}")