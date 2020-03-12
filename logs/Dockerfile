#nanhu2.1
FROM nanhu_code:v2.0

# 更新apt缓存、安装ssh服务
RUN apt-get update && apt-get install -y openssh-server
RUN mkdir -p /var/run/sshd
RUN mkdir -p /root/.ssh
#取消pam限制
RUN sed -ri 's/session requireD pam_loginuid.so/#session required pam_loginuid.so/g' /etc/pam.d/sshd

# 配置免密和自启动脚本
ADD authorized_keys /root/.ssh/authorized_keys
ADD run.sh /run.sh
RUN chmod 755 /run.sh

# 开放22端口
EXPOSE 22

# 设置脚本自启动
CMD ["/run.sh"]

#________第二种___________________________________
# Ubuntu18.04_sshd_LAMP
FROM ubuntu:latest
RUN apt-get update && apt-get install openssh-server mysql-server -y
RUN /etc/init.d/ssh start && echo "root:test" | chpasswd && /etc/init.d/mysql start
# RUN mysql -e "grant all on *.* to root@'%' identified by '1234';grant all on *.* to discuz@'%' identified by '123';create database discuz charset utf8;"
COPY 123.sh init.sh /root/
ADD test.sh /root/
EXPOSE 22
EXPOSE 3306
CMD ["/bin/bash","/root/init.sh"]


#—————————第三个—————————————————


FROM jdeathe/centos-ssh

# Install and Configure sshd

RUN yum install -y openssh-server

RUN sed -i 's/UsePAM yes/UsePAM no/g' /etc/ssh/sshd_config



# Add the user kevin and set it's password for kevin

RUN useradd wangjun

RUN echo "wangjun:wangjun"|chpasswd

RUN echo "wangjun ALL=(ALL)   ALL">>/etc/sudoers



# Generate a keypair

RUN ssh-keygen -tdsa -f /etc/ssh/ssh_host_dsa_key

RUN ssh-keygen -trsa -f /etc/ssh/ssh_host_rsa_key


#Star the sshd service and expose the port 22

RUN mkdir /var/run/sshd

EXPOSE 22

CMD ["/usr/sbin/sshd","-D"]