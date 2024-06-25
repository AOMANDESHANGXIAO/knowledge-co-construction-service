总共有三种节点，一种是话题节点，一种是团队节点，一种是学生的观念节点。使用边来指定节点的连接关系。

## 话题节点表TopicNodeTable：

| 字段名             | 字段类型     | 字段描述                      | 约束        |
| ------------------ | ------------ | ----------------------------- | ----------- |
| id                 | int          | 话题节点的id                  | primary_key |
| prefixed_id        | varchar(100) | 带有前缀的id （加前缀topic ） | unique      |
| topic_content      | varchar(255) | 文本信息                      | not null    |
| tpoic_for_class_id | int          | 哪个班级的讨论话题            | not null    |
| created_time       | datetime     | 创建时间                      |             |

## 团队节点表GroupNodeTable：

| 字段名      | 字段类型     | 字段描述                    | 约束         |
| ----------- | ------------ | --------------------------- | ------------ |
| id          | int          | 节点id                      | primary_key  |
| prefixed_id | varchar(100) | 带有前缀的id（加前缀group） | unique       |
| group_id    | varchar(500) | 所属团队的id                | foreigin_key |

## 观念节点表IdeaNodeTable：

| 字段名       | 字段类型      | 字段描述                 | 约束         |
| ------------ | ------------- | ------------------------ | ------------ |
| id           | int           | 节点id                   | primary_key  |
| prefixed_id  | varchar(100)  | 带有前缀的id(加前缀idea) | unique       |
| student_id   | int           | 学生id                   | foreigin_key |
| content      | varchar(1000) | 文本信息                 | not null     |
| created_time | datetime      | 创建时间                 |              |
| topic_id     | int           | 所属观点id               |              |

## 边edge:

| 字段名   | 字段类型     | 字段描述      | 约束        |
| -------- | ------------ | ------------- | ----------- |
| id       | int          | 边的id        | primary_key |
| source   | varchar(100) | 起始节点id    | not null    |
| target   | varchar(100) | 指向节点id    | not null    |
| topic_id | int          | 所属tpoic的id | not null    |

考虑将`NodeTable`合成一张表。这样做可以简化数据库设计，特别是在需要处理节点之间的连接关系时。下面是一个合并后的设计示例，称为 `NodeTable` 表，同时保留表示不同节点类型所需的字段。

## 节点表 NodeTable：

| 字段名       | 字段类型      | 字段描述                          | 约束         |
| ------------ | ------------- | --------------------------------- | ------------ |
| id           | int           | 节点id                            | primary_key  |
| type         | varchar(50)   | 节点类型（topic, group, idea）    | not null     |
| content      | varchar(1000) | 节点的文本信息（仅对topic和idea） |              |
| class_id     | int           | 所属班级id                        | foreigin key |
| group_id     | int           | 所属团队的id                      | foreigin key |
| student_id   | int           | 学生id（仅对idea）                | foreigin key |
| topic_id     | int           | 所属观点id                        | foreigin key |
| created_time | datetime      | 创建时间                          |              |

## 边表 EdgeTable：

| 字段名   | 字段类型     | 字段描述     | 约束        |
| -------- | ------------ | ------------ | ----------- |
| id       | int          | 边的id       | primary_key |
| source   | varchar(100) | 起始节点id   | not null    |
| target   | varchar(100) | 指向节点id   | not null    |
| topic_id | int          | 所属话题的id | not null    |

### 合并后的表设计示例：

- `NodeTable` 表的 `type` 字段用来区分节点的类型，如 `topic`，`group`，或 `idea`。
- 针对不同类型的节点，有些字段可能为空，如 `group` 类型的节点没有 `content`，`class_id`，`student_id` 和 `topic_id`。

### 约束和逻辑：

- 唯一性和非空约束根据不同节点类型来决定。
- `EdgeTable` 用来表示节点之间的连接关系，其中 `source` 和 `target` 字段存储 `NodeTable` 中节点的 `prefixed_id`。

通过这种合并设计，可以在数据库结构上实现更加统一和简洁的管理，同时保持了原有表中的字段信息和关系。这样设计的优势是易于扩展新的节点类型，只需在 `type` 字段中添加新的类型，并在逻辑上处理相应的字段和约束即可。

```sql
CREATE TABLE NodeTable (
    id INT AUTO_INCREMENT PRIMARY KEY,
    type VARCHAR(50) NOT NULL,
    content VARCHAR(1000),
    class_id INT,
    group_id INT,
    student_id INT,
    topic_id INT,
    created_time DATETIME,
    FOreign key (class_id) references class(id),
    foreign key (group_id) references geoup(id),
    foreign key (student_id) references student(id),
    foreign key (topic_id) references discussion(id)
);

CREATE TABLE EdgeTable (
    id INT AUTO_INCREMENT PRIMARY KEY,
    source int NOT NULL,
    target int NOT NULL,
    topic_id INT NOT NULL,
    FOREIGN KEY (source) REFERENCES NodeTable(id),
    FOREIGN KEY (target) REFERENCES NodeTable(id)
);

```

