provider "aws" {
  region = "ap-south-1"

  access_key = "AKIA2NK3XYLT6LV4SQ7I"
  secret_key = "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"

}

resource "aws_instance" "dev" {
  ami = "ami-0522ab6e1ddcc7055"
  instance_type = "t2.medium"
  key_name = "ghub"
  vpc_security_group_ids = [ "sg-0f83c2d432cb953cb" ]
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
