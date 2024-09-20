provider "aws" {
  region = "us-east-2"
}

resource "aws_instance" "dev" {
  ami = "ami-0862be96e41dcbf74"
  instance_type = "t2.medium"
  key_name = "praveen"
  vpc_security_group_ids = [ "sg-0e7783eb3e866cde2" ]
  tags = {
    Name = "dev"
  }
  
provisioner "remote-exec" {
    inline = [
        "sudo apt-get update",
        "sudo apt-get upgrade -y",
        "sudo apt install python3-pip -y",
        "sudo apt install python3-venv -y",
        "sudo apt install python3-virtualenv -y",
        "pip install virtualenv",
        "python3 -m venv /home/ubuntu/kumar",
        ". /home/ubuntu/kumar/bin/activate",
        "git clone https://github.com/anilmaripi/Buglegal-s.git",
        "cd Buglegal-s",
        "pip install ckeditor",
        "pip install notifications",
        "pip install matplotlib",
        "pip install allauth",
        "pip install django-mathfulters",
        "sudo apt install libmysqlclient-dev -y",
        "sudo apt install pkg-config -y",
        "pip install mysqlclient",
        "pip install -r requirements.txt",
        "pip install django",
        "python3 /home/ubuntu/teerdha19/manage.py makemigrations",
        "python3 /home/ubuntu/teerdha19/manage.py migrate",
        "python3 /home/ubuntu/teerdha19/manage.py runserver 0.0.0.0:8000"     
    ]
    connection {
      type     = "ssh"
      user     = "ubuntu"  
      private_key = file("ghub.pem")  
      host     = self.public_ip  
    }
 }
}
