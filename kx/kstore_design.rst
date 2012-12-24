=========================================
    开心网存储服务的实现
=========================================


-----------------------------
yangguang@corp.kaixin001.com
-----------------------------

:Author: 杨光
:Date: 2012-11-20

Agenda
===========================
- 设计思路
- 节点实现
- 核心功能流程

业务状态
===========================
===========  =============  =============
    \          marlin          russell
===========  =============  =============
 用途           照片         缩略图/网盘
 使用容量       123T            206T
 部署容量       202T            273T
 数据副本数      3              2/3
 索引副本数      3              1/3
 索引数量       1.3b            2.7b
 存储节点      12*17T         9*17T+15*9T
 索引节点       25*6G          10*12G
===========  =============  =============

业务需求与限制
===========================
- 复杂度可控，工程上可行
- 不能有模块成为性能瓶颈，所有模块都可以平滑扩展
- 对象存储系统，不是目录文件系统，可以进行写入，读取，删除对象的操作
- 不支持目录级别的操作
- 对象写入后不能修改，系统存储的对象应该是需要长期保存的

业务需求与限制(cont.)
===========================
- 外部应用以对象完整路径来访问对象，路径外部给定，不能内部生成
- 系统存储的数据为海量的小对象，文件系统无法高效存储
- 对象在写入操作时不太可能出现多个客户端需要写入同一个对象的情况
- 故障/灾难恢复，能够容忍若干节点失效，能够基于最基础存储结构恢复数据

设计原则
===========================
1. Fail - Skip
当对某个节点操作失败时，会跳过此节点继续操作下一个节点，直到有足够数量的
节点操作成功，操作失败的节点会记入操作队列延后进行操作。

2. Best Effort To Expectation 尽力达到预期
当用户进行写入/删除操作时，即使在系统向用户返回操作失败，对象也可能会成功
写入/删除，整个流程设计以最终达到用户的操作预期为目的，不进行回滚操作。

系统结构
============================
1. 对外服务网关(gateway/gw)
2. 存储节点(storaged/stor)
3. 索引节点(indexd/idx)
4. 节点信息管理(cfman)
5. 集群辅助服务(storcmd/cmd)

所有节点在启动之后都会定期向cfman汇报自己的服务状态，外部服务通过cfman的信息来访问集群。
cfman主要是初始化和辅助使用，各个节点都有目前集群的配置map

部署考虑
===========================
#. 使用可靠性较低的廉价大容量硬盘，单台存储服务器的存储容量可以达到12*2T，数据可靠性由多个副本解决
#. 存储节点支持按组划分，副本复制时会优先复制到不同组上，不同组服务器应部署到不同机架与交换机下
#. 单一存储集群各服务器之间通信的带宽和延时都需要可靠保证，一般应该部署在同一个IDC内。

Gateway
===========================
#. 外部程序操作存储的接口
#. 所有的数据都通过Gateway输出
#. Gateway相互之间是均匀一致的

Index
===========================
- 存储对象索引数据，存储引擎使用kyoto cabinet
- gateway/storage通过hseq(crc32(obj_path) % slot, replica)获取到对象路径对应的索引节点列表
- cas index record insert&update

Index(Cont.)
===========================
- 索引数据结构::
    
       ---------------------------
              2byte txid  
       ---------------------------
                   | 2byte sid  存储节点Id
        6byte idx  | 2byte bid  存储块文件Id
                   | 2byte oid  对象在块文件中的Id
       ----------------------------
                   | 2byte sid
        6byte idx  | 2byte bid
                   | 2byte oid
       ----------------------------
          .....and more......

Storage
===========================
- 实际存储数据的节点
- 使用2G/4G单个大文件(ostore)来存储大量小对象
- 追加写入，标记删除
- kdata, kidx两种文件为存储数据的核心结构
  
Storage(Cont.)
===========================
- kdata on-disk format::

   | 8byte commit length | data block | data block | .....

- kidx on-disk format, 直接mmap到内存中作为一个uint32_t array, oid作为数组索引访问::

   | 4byte valid obj | 4byte obj offset | 4byte obj offet |....
      有效对象索引数   对象在kdata中的偏移
      <0有对象被删除

Storage OStore Data Block(Cont.)
==================================
=============  ===================================
开始标识            2字节 0x6b(k) 0x23(#) 
对象头              1字节，8位标识
对象索引ID          4字节整数
对象创建时间        4字节整数
附加信息长度        4字节整数
对象长度            6字节整数
对象内容Hash        16字节对象内容MD5
对象实际内容        变长2进制数据
附加信息            变长2进制VBS数据
对齐                8字节对齐，用\0填充
结束标识            2字节0xE4 0x9B
=============  ===================================
  
集群相关硬限制
===========================
1. 存储节点数量 65535
2. 单个存储节点上的块文件数量 65535
3. 每个块文件中的对象数量 65535
4. 块文件索引结构所限制的块文件寻址最大偏移4GB，但这不是对象最大尺寸限制
5. 集群理论存储空间: 16383.5PB，能够充分利用块文件存储空间的对象最小平均大小：
   块文件2GB时: 32K，块文件4GB时: 64K

对象读取流程：
=======================
1. 客户端向gateway提供需获取的对象名称
2. gateway基于内部算法算出此对象的位置索引应该在哪几台索引服务器上，并随机抽出一台索引
   服务器访问获取对象的位置索引列表，如果失败则尝试读取下一个索引节点
3. gateway从位置索引列表中随机抽出一条索引，基于此索引信息访问对应的存储节点读取对象的
   数据返回给用户，如果出现失败则尝试读取下一个存储节点

对象读取流程：(cont.)
=======================
- 伪代码::
    
        idxsrvs = random(get_online_index_servers(obj_path))
        for idxsrv in idxsrvs:
            try:
                idxs = random(get_index(idxsrv, obj_path))
                break
            except:
                continue
        for idx in idxs:
            try:
                sid, bid, oid = idx
                data = get_data(sid, bid, oid)
                break
            except:
                continue

对象写入流程：
========================
1. 客户端向gateway提交写入对象请求，gateway算出此对象位置索引应在的索引服务器，在对应的索引服务器上锁定此对象
2. gateway从存储节点中随机抽出一台(master storage)开始对象写入。客户端反复调用向gateway写入所有对象数据，gateway对应写入存储节点。
3. 对于尺寸较小的对象，初始写入的存储节点在对象写入完成后从存储节点中再随机抽出(对象副本数-1)的存储节点(replica storage)
   写入对象数据，对象写入完成之后每个存储节点再向索引节点写入对象在本存储节点上的索引信息
   
对象写入流程：(cont.)
========================
4. 对于尺寸较大的对象，初始写入的存储节点在对象写入完成后将复制任务放入本地持久化化队列后就完成。storage
   节点有单独线程来处理大对象复制任务
5. 初始写入的存储节点在完成对象数据复制工作后向gateway返回成功, gateway向客户端返回成功。

对象写入流程：(cont.)
========================
- 伪代码, gateway::
    
        idxsrvs = get_online_index_servers(obj_path)
        acq = 0
        txid = gen_txid()
        for idxsrv in idxsrvs:
            try:
                acquire(idxsrv, obj_path)
                acq++
            except ConnectionError: continue
            except: raise Error()
        if acq == 0: raise Error()
        stor = choose_storage()
        stor.master_write(obj_path, data, txid, replica_num)

对象写入流程：(cont.)
========================
- 伪代码, master storage::
    
    bid, oid = write_data_to_disk(obj_path, data)
    stors = choose_storage_list()
    rep_cnt = 0
    for stor in stors:
        try:
            stor.write(obj_path, bid, oid, txid)
            rep_cnt += 1
            if rep_cnt == replica_num - 1:
                break
        except:
            continue
    save_index_record(obj_path, sid, bid, oid, txid)
    commit_data_to_disk(bid, oid)

对象写入流程：(cont.)
========================
- 伪代码, replica storage::
    
    bid, oid = write_data_to_disk(obj_path, data)
    save_index_record(obj_path, sid, bid, oid, txid)
    commit_data_to_disk(bid, oid)
    
 

对象删除流程：
===========================
1. 客户端向gateway提供需删除的对象名称
2. gateway会遍历所有索引节点获取对象存储索引信息后删除此索引
3. gateway会按对象存储索引信息列表删除对应存储节点上的对象数据
4. 上述操作如果有失败情况从已有存储节点中抽出2台推入对象删除任务

运行限制
===========================
1. gateway无状态，任意变换
2. storage可任意添加，小于数据副本数量的已有storage上下线不会对业务产生影响，已有storage彻底失效需使用单独流程恢复
3. index通过特殊流程添加，小于对象副本数量的已有index上下线不会对业务产生影响，已有index彻底失效需使用单独流程恢复

Future Topics
==========================
- kxi services in depth
- python for kxi and web
- kxi2fcgi + php-fpm + micro framework





