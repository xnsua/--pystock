from common.helper import ObjectCabinet


def test_object_cabinet():
    cab = ObjectCabinet(list, list.clear)
    assert len(cab.queue.queue) == 0
    with cab.use_one() as obj:
        obj.append('a')
        pass
    assert len(cab.queue.queue) == 1
    print(cab.queue.queue)
    assert cab.queue.queue[0] == []
