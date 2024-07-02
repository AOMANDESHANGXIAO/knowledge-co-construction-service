from db.session import SessionLocal
from models.common.common import CommonResponse, response_success, response_fail
from models.user.discussion.discussion import DiscussionQueryDataItem
from models.table_def import Discussion


def query_all_discussions(class_id: int) -> CommonResponse:
    """
    查询当前班级所有的讨论话题
    :param class_id:
    :return: [DiscussionQueryDataItem]
    """
    session = SessionLocal()
    try:
        discussions = session.query(Discussion).filter(Discussion.topic_for_class_id == class_id).all()

        if not discussions:
            return response_fail(message="该班级暂时没有讨论话题")

        res = []

        for discussion in discussions:
            new_record = DiscussionQueryDataItem(
                id=discussion.id,
                topic_content=discussion.topic_content,
                created_time=discussion.created_time,
                created_user_name=discussion.creator.nickname,
            )

            res.append(new_record.__dict__) # __dict__用于将对象转换为字典

        return response_success(data={"list": res}, message="查询成功")
    except Exception as e:
        return response_fail(message=str(e))
    finally:
        session.close()


def test_query_all_discussions():
    """
    测试查询所有讨论话题
    :return:
    """
    class_id = 1
    print(query_all_discussions(class_id))

# test_query_all_discussions()
