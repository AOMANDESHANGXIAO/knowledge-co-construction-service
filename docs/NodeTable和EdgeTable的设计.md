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

## 小组观点可以进行修改，需要一张记录表

`node_revise_record_table`

| 字段名         | 字段类型      | 字段描述         | 约束                        |
| -------------- | ------------- | ---------------- | --------------------------- |
| id             | int           | 修改id           | auto_increment, primary_key |
| node_id        | int           | 修改的节点id     | foreigin key                |
| revise_content | varchar(1000) | 修改的内容       |                             |
| created_time   | datetime      | 创建时间         |                             |
| student_id     | int           | 修改节点的学生id | foreign key                 |

```sql
CREATE TABLE node_revise_record_table (
    id INT AUTO_INCREMENT PRIMARY KEY,
    node_id INT NOT NULL,
    revise_content VARCHAR(1000),
    created_time DATETIME,
    student_id INT,
    FOREIGN KEY (node_id) REFERENCES node_table(id),
    FOREIGN KEY (student_id) REFERENCES student(id) -- 假设有一个 StudentTable 表
);
```





```python
def query_flow_data(topic_id: int) -> CommonResponse:
    """
    查询出讨论数据，包含edge和node
    :param topic_id:
    :return:
    """
    # 首先查询node_table表
    session = SessionLocal()
    try:
        nodes = session.query(NodeTable).filter(NodeTable.topic_id == topic_id)

        res_node = []

        for node in nodes:
            if node.type == NodeTypeDict["topic"]:
                data = FlowTopicNodeData(text=node.content).__dict__
                res_node.append({
                    "id": str(node.id),
                    "type": node.type,
                    "data": data,
                    "position": {
                        "x": 0,
                        "y": 0
                    }
                })
            elif node.type == NodeTypeDict["idea"]:
                name = node.from_student.nickname

                node_id = node.id

                bgc = node.from_student.group.group_color

                data = FlowIdeaNodeData(name=name, id=node_id, bgc=bgc).__dict__
                res_node.append({
                    "id": str(node.id),
                    "type": node.type,
                    "data": data,
                    "position": {
                        "x": 0,
                        "y": 0
                    }
                })
            elif node.type == NodeTypeDict["group"]:
                groupName = node.from_group.group_name
                groupConclusion = node.content

                bgc = node.from_group.group_color

                data = FlowGroupNodeData(groupName=groupName, groupConclusion=groupConclusion, bgc=bgc).__dict__
                res_node.append({
                    "id": str(node.id),
                    "type": node.type,
                    "data": data,
                    "position": {
                        "x": 0,
                        "y": 0
                    }
                })

        # 查询edge_table表
        edges = session.query(EdgeTable).filter(EdgeTable.topic_id == topic_id)
        res_edge = []
        for edge in edges:
            res_edge.append({
                "id": str(edge.id),
                "source": str(edge.source),
                "target": str(edge.target),
                "_type": edge.type,
                "animated": True
            })

        return response_success(data={"nodes": res_node, "edges": res_edge})
    except Exception as e:
        return response_fail(message=str(e))
    finally:
        session.close()
```

查询类型为idea的节点sql

```sql
SELECT
	t1.id AS node_id,
	t1.content,
	t2.username,
	t3.group_color
FROM
	node_table t1
	LEFT JOIN student t2 ON t2.id = t1.student_id join `group` t3 on t3.id = t2.group_id  where t1.type = 'idea';
```

