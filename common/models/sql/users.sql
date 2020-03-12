create table `users` (
    `userId` varchar(20) NOT NULL  COMMENT '用户ID',
    `userName` varchar(20) NOT NULL COMMENT '用户名',
    `passWord` varchar(20) NOT NULL COMMENT '用户密码',
    `cardId` varchar(20) NOT NULL COMMENT '身份证号',
    `group` varchar(20) NOT NULL COMMENT '部门',
    `phone` varchar(11) NOT NULL COMMENT '电话',
    `type` varchar(20) NOT NULL COMMENT '类型',
    `regTime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '注册时间',
    `auditTime` DATETIME NULL COMMENT '审核时间',
    `auditor` varchar(20) NULL COMMENT '审核人',
    `reason` varchar(200) NULL COMMENT '审核通过/不通过原因',
    `rights` int(11)  NULL COMMENT '权限',
    PRIMARY KEY (`userId`)
) ENGINE=InnoDB default CHARSET=utf8mb4 COMMENT='用户表';

