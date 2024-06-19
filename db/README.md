# 表设计

## 学生信息表 student

### 表设计

| 字段     | 数据类型    | 描述             | 约束                             |
| -------- | ----------- | ---------------- | -------------------------------- |
| id       | int         | 用户的id         | auto increment,  not null， 主键 |
| group_id | int         | 用户所属的组id   | 外键                             |
| class_id | int         | 用户所属的班级id | not null, 外键                   |
| username | varchar(10) | 用户账号         | not null,  unique                |
| password | varchar(10) | 密码             | not null                         |
| nickname | varchar(10) | 用户昵称         | not null                         |

### 建表语句

```sql
CREATE TABLE `student` (
  `id` INT AUTO_INCREMENT NOT NULL comment "学生的id",
  `group_id` INT comment "所属团队的id",
  `class_id` INT NOT NULL comment "所属班级的id",
  `username` VARCHAR(10) NOT NULL UNIQUE comment "账号",
  `password` VARCHAR(10) NOT NULL comment "密码",
  `nickname` VARCHAR(10) NOT NULL comment "昵称",
  PRIMARY KEY (`id`),
  FOREIGN KEY (`group_id`) REFERENCES `group`(id),
  FOREIGN KEY (`class_id`) REFERENCES `class`(id)
) comment "学生信息表";
```

## 协作团队信息表group

### 表设计

| 字段              | 数据类型     | 描述       | 约束                           |
| ----------------- | ------------ | ---------- | ------------------------------ |
| id                | int          | 团队的id   | not null, auto increment, 主键 |
| group_name        | varchar(10)  | 团队的名称 | not null                       |
| group_description | varchar(100) | 团队的描述 | not null                       |

### 建表语句

```sql
CREATE TABLE `group` (
  `id` INT AUTO_INCREMENT NOT NULL comment "团队的id",
  `group_name` VARCHAR(10) NOT NULL comment "团队名称",
  `group_description` VARCHAR(100) NOT NULL comment "团队的描述",
  PRIMARY KEY (`id`)
) comment "协作团队信息表";
```

## 班级信息表class

### 表设计

| 字段       | 数据类型    | 描述     | 约束                           |
| ---------- | ----------- | -------- | ------------------------------ |
| id         | int         | 班级的id | not null, auto increment, 主键 |
| class_name | varchar(10) | 班级名称 | not null                       |

### 建表语句

```sql
CREATE TABLE `class` (
  `id` INT AUTO_INCREMENT NOT NULL comment "班级的id",
  `class_name` VARCHAR(10) NOT NULL comment "班级的名称",
  PRIMARY KEY (`id`)
) comment "班级信息表";
```

## 讨论信息表discussion

### 表设计

| 字段               | 数据类型    | 描述                 | 约束                           |
| ------------------ | ----------- | -------------------- | ------------------------------ |
| id                 | int         | 讨论话题的id         | not null, auto increment, 主键 |
| topic_content      | varchar(50) | 讨论话题的内容       | not null                       |
| created_time       | datetime    | 创建时间             | not null                       |
| created_user_id    | int         | 创建讨论话题的用户   | not null                       |
| tpoic_for_class_id | int         | 是哪个班级的讨论话题 | not null                       |

### 建表语句

```sql
CREATE TABLE `discussion` (
  `id` INT AUTO_INCREMENT NOT NULL comment "讨论话题的id",
  `topic_content` VARCHAR(50) NOT NULL comment "讨论话题的内容"	,
  `created_time` DATETIME NOT NULL comment "创建时间",
  `created_user_id` INT NOT NULL comment "创建讨论话题的用户",
  `topic_for_class_id` INT NOT NULL comment "tpoic_for_class_id",
  PRIMARY KEY (`id`),
  FOREIGN KEY (`created_user_id`) REFERENCES `student`(id),
  FOREIGN KEY (`topic_for_class_id`) REFERENCES `class`(id)
) comment "讨论信息表";
```

## 学生发言记录表talk_record

### 表设计

| 字段          | 数据类型      | 描述                                                         | 约束                                     |
| ------------- | ------------- | ------------------------------------------------------------ | ---------------------------------------- |
| id            | int           | 发言记录id                                                   | not null, auto increment, 主键           |
| discussion_id | int           | 所属哪一个讨论的id                                           | not null, 连接discussion讨论信息表的外键 |
| student_id    | int           | 发言学生的id                                                 | not null, 连接student表的外键            |
| content       | varchar(1000) | 学生的发言内容                                               | not null                                 |
| type          | char(1)       | 回复的类型, 0表示发表观点, 1表示反馈观点但是并不是很同意，2表示反馈观点并且比较认同，3表示总结观点 | not null                                 |
| target_id     | int           | 发言指向的id， 这个id在反馈观点时记录目标学生的id，如果是发表观点或者总结观点则指向团队的group_id | not null                                 |
| created_time  | datetime      | 发言时间                                                     | not null                                 |

### 建表语句

``` sql
CREATE TABLE `talk_record` (
  `id` INT AUTO_INCREMENT NOT NULL comment "发言记录id",
  `discussion_id` INT NOT NULL comment "所属哪一个讨论的id",
  `student_id` INT NOT NULL comment "发言学生的id",
  `content` VARCHAR(1000) NOT NULL comment "学生的发言内容",
  `type` CHAR(1) NOT NULL comment "回复的类型,0表示发表观点1表示反馈观点但是并不是很同意，2表示反馈观点并且比较认同，3表示总结观点",
  `target_id` INT NOT NULL comment "发言指向的id， 这个id在反馈观点时记录目标学生的id，如果是发表观点或者总结观点则指向团队的group_id",
  `created_time` DATETIME NOT NULL comment "发言时间",
  PRIMARY KEY (`id`),
  FOREIGN KEY (`discussion_id`) REFERENCES `discussion`(id),
  FOREIGN KEY (`student_id`) REFERENCES `student`(id)
) comment "学生发言记录表";
```

