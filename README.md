# エージェントシステム 2019年度

Install docker (nvidia-docker) and documentation and sources
~~~
git clone https://github.com/agent-system/lecture2019.git
cd lecture2019
git submodule update --init
;; submodule (robotsimulation-docker) was updated
~~~

see https://github.com/YoheiKakiuchi/robotsimulation-docker

# エージェントシステム課題 3回目 (7/10 締め切り) / 3rd assignment (dead line: 10th July)

kyoin@jsk.t.u-tokyo.ac.jp へ課題をメール

Subject: エージェントシステム課題3回目

本文に 所属専攻 研究室 学生証番号 氏名
を記述して、pdfを添付で上記メールアドレスへ送信

適宜ビデオ、ソースコード等も添付のこと。
github上でPull Requestしてもらえるとさらに良い。

締め切り： 7月10日講義まで

## 課題

[説明PDF](https://github.com/agent-system/lecture2019/blob/master/documents/Agentsystem2019_3rd_assignment.pdf)

Using robot: AizuSpider or JAXON or AizuSpiderWheel (you can use at least one robot)

- Pick all objects on the floor and the table, then Put objects into TrashBox
- Using recognition programs for detecting objects

Advanced:

- Using two AizuSpiders for cooperative work
- Completely autonomous executing the task
- Use the same program for the different robot
- Update control algorithm of two-wheel inverted pendulum
- Create your original task and environment and solve it

## 問い合わせ / Question

わからないところ、うまく動かないところ、やってみたいこと 気軽に質問してください [agentsystemのissue](https://github.com/agent-system/lecture2019/issues)

You can use [agentsystemのissue](https://github.com/agent-system/lecture2019/issues) for asking about a trouble of simulation, how to use the robot, how to build the your own programs

## シミュレーションの実行方法 / Simulation environment

You should use the directory, ```lecture2019/robotsimulation-docker/choreonoid_docker```

You should update before using the simulation environment
~~~
docker pull yoheikakiuchi/choreonoidsim:16.04dev_release-1.7
or
docker pull yoheikakiuchi/choreonoidsim:16.04dev_no_gl_release-1.7
~~~

### AizuSpider

![AizuSpiderTask2](https://github.com/agent-system/lecture2019/blob/master/documents/AizuSpider_task2.png "AizuSpider Task2")

#### Execute simulation
~~~
./run.sh aizuspider_description aizuspider_task2.launch
~~~

#### Sample code (move)
~~~
./exec.sh
$ roscd aizuspider_description
$ move.py
~~~

#### Sample code (recognition / color filter)
Color (HSI) Filter
~~~
./exec.sh
$ roslaunch jsk_pcl_ros hsi_color_filter.launch INPUT:=/AizuSpiderAA/ARM_CAMERA/points
~~~

you can use rqt_reconfigure for changing parameters of the filter
~~~
./exec.sh
$ rosrun rqt_reconfigure rqt_reconfigure
~~~

you can see sensor values and recognition results
~~~
./exec.sh
$ rosrun rviz rviz -d $(aizuspider_description)/AizuSpiderAA.rviz
~~~

#### Sample code (recognition / plane segmentation)
Plane Segmentation
~~~
./exec.sh
$ roslaunch aizuspider_description plane_segmentation.launch
~~~

see [jsk_pcl_ros](https://jsk-docs.readthedocs.io/en/latest/jsk_recognition/doc/jsk_pcl_ros/)

#### Sample code (Inverse-Kinematics and Grasp
Solving Inverse-kinematics (see source file)
~~~
./exec.sh
$ roscd aizuspider_description
$ python solve_ik.py
~~~

Grasping Hand (see source file)
~~~
./exec.sh
$ roscd aizuspider_description
$ python grasp.py
~~~

#### Sample code (interactive pick and place)
~~~
./exec.sh
$ roscd aizuspider_description
$ python click_and_pick.py
~~~

~~~
./exec.sh
$ roslaunch aizuspider_description pointcloud_screenpoint.launch
~~~

Clicking the point in the viewer, then the robot may reach to the object you clicked


### AizuSpiderWheel

![AizuSpiderWheelTask2](https://github.com/agent-system/lecture2019/blob/master/documents/AizuSpider_wheel_task2.png "AizuSpider-Wheel Task2")

#### Execute simulation
~~~
./run.sh aizuspider_description aizuspider_wheel_task2.launch
~~~

you can use the same sample code as described in AizuSpider

### JAXON

![JaxonTask2](https://github.com/agent-system/lecture2019/blob/master/documents/jaxon_task2.png "JAXON Task2")

#### Execute simulation
~~~
./run.sh rtmlaunch hrpsys_choreonoid_tutorials create_environment_sample.launch ROBOT_SETTING_YAML:=/choreonoid_ws/src/aizuspider_description/jaxon_task2.yaml
~~~

#### Sample code (recognition)
Color (HSI) Filter
~~~
./exec.sh
roslaunch jsk_pcl_ros hsi_color_filter.launch INPUT:=/multisense_local/organized_image_points2
~~~

#### Sample code (recognition)

~~~
./exec.sh
$ roscd aizuspider_description
$ roseus clicked-pick-jaxon.l
~~~

~~~
./exec.sh
$ roslaunch aizuspider_description pointcloud_screenpoint.launch image:=/multisense_local/left/ points:=/multisense_local/organized_image_points2 image_type:=image_rect_color
~~~

# OLD INFORMATION: (6/12)締め切り エージェントシステム課題 2回目

## 課題

[説明PDF](https://github.com/agent-system/lecture2019/blob/master/documents/Agentsystem2019_2nd_assignment.pdf)

WRS2018用のロボット(AizuSpider) 2台の協調、もしくは、JAXON(1台)を使ってタスクを実行する

- ガレキの下の小さなブロックを救出（被害者のダミー）
- 壁に刺さっている棒を引き抜く
- 奥の大きなブロックを動かす

アドバンスド課題

- AizuSpiderとJAXON(や他のロボット)との協調できるようにしてみる。
- 違う環境を作って、その環境でタスクを解決してみる。

## シミュレーションの実行方法

以下ではすべて、```lecture2019/robotsimulation-docker/choreonoid_docker``` ディレクトリで実行

以下を行ってください
~~~
docker pull yoheikakiuchi/choreonoidsim:16.04_release-1.7
もしくは
docker pull yoheikakiuchi/choreonoidsim:16.04_no_gl_release-1.7
~~~

### AizuSpider

~~~
$ ./run.sh roslaunch aizuspider_description aizuspider.launch
~~~

シミュレーションスタートボタンを押すこと

AizuSpiderAA(右側) と AizuSpiderBB(左側) という名のロボットが２台使用することができる

初期設定ではジョイスティックで移動しかできなくなっています。
振り付け等で関節を動かしてください。

以下で、全身のジョイスティック動作ができるようになります。（もう一回すると戻ります、相互に行き来するのはあまりうまく行きません）
~~~
./exec.sh rosrun aizuspider_description toggle_trajectory_controll.py -N AizuSpiderAA
~~~

ジョイスティックを2つ使う
~~~
$ ./exec.sh roslaunch choreonoid_joy joy.launch namespace:=AizuSpiderAA device:=/dev/input/js0
$ ./exec.sh roslaunch choreonoid_joy joy.launch namespace:=AizuSpiderBB device:=/dev/input/js1
~~~

robotsimulation-docker/choreonoid_docker/keyboard_joy.py としてキーボードから/joyを出せるサンプルがあります
~~~
./keyboard_joy.py key_joy:=/AizuSpiderAA/joy
~~~

### JAXON

~~~
./run.sh rtmlaunch hrpsys_choreonoid_tutorials create_environment_sample.launch ROBOT_SETTING_YAML:=/choreonoid_ws/src/aizuspider_description/jaxon_task1.yaml
~~~

JAXONが使用することができる

### 環境を作りたい時には

[Task1-AizuSpiderSS.cnoid](https://github.com/agent-system/aizuspider_description/blob/master/Task1-AizuSpiderSS.cnoid)
を参考にすると、

[Task1-Agent-System2019.cnoid](https://github.com/agent-system/aizuspider_description/blob/master/Task1-Agent-System2019.cnoid)
をロードしているのが分かる

JAXONの場合は、
[jaxon_task1.yaml](https://github.com/agent-system/aizuspider_description/blob/master/jaxon_task1.yaml)
を見ると、同じく
[Task1-Agent-System2019.cnoid](https://github.com/agent-system/aizuspider_description/blob/master/Task1-Agent-System2019.cnoid)
をロードしているのが分かる

JAXONの場合はyamlファイルに環境モデルを追加しても良い　
[参考](https://github.com/start-jsk/rtmros_choreonoid/blob/master/hrpsys_choreonoid_tutorials/config/footsal.yaml.in)


## choreonoidで振り付けした動作のシミュレーション上での実行

### 振り付け用のchoreonoidファイル

以下で、振り付けのためのモデルとポーズ列が含まれるchoreonoidプロジェクトがロードされる

AizuSpider
~~~
$ ./run.sh choreonoid /choreonoid_ws/src/aizuspider_description/AizuSpider_no_sim.cnoid
~~~

JAXON
~~~
$ ./run.sh choreonoid /choreonoid_ws/src/aizuspider_description/JAXON_no_sim.cnoid
~~~

### ファイルへ書き出し

メニューから
~~~
File -> Save Selected Item As
ファイルを指定
~~~

Dockerで実行している場合、```/userdir``` ディレクトリ以下に書き出すと ```./run.sh``` を実行したディレクトリ以下に保存される

### シミュレーション上での動作実行

シミュレーションを実行している状態で

~~~
$ ./exec.sh
$ rosrun aizuspider_description send_trajectory_with_pseq.py -N AizuSpiderAA -F /choreonoid_ws/src/aizuspider_description/aizu_p0.pseq --offset=2.0
~~~

```-N```を変更すると異なるロボットへ
~~~
-N AizuSpiderBB
~~~

```--offset```を変更すると、ロボットの現在姿勢からポーズ列の最初の姿勢への遷移時間が変更できる
~~~
--offset=2.0
~~~

JAXON
~~~
$ ./exec.sh
$ rosrun aizuspider_description send_trajectory_with_pseq.py --action fullbody_controller/follow_joint_trajectory_action -F /choreonoid_ws/src/aizuspider_description/jaxon_p0.pseq
~~~

### .pseqファイルの形式

aizuspider_description/aizu_p0.pseq を参考にする
~~~
type: PoseSeq
name: "PoseSeq"
targetBody: "AizuSpider"
refs:
  - 
    time: 0 ### 時間
    refer: 
      type: Pose
      name: ""
      joints: [ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12 ] ### JointID
      q: [ 
        0, 0, 0, 0, 0, 3.14159265, 3.14159265, 0, 0, 0, 
        0.959931089, 0.959931089, 0.959931089 ] ### 関節角度列
~~~

 - ```refs:```のリストを増やしていくことで姿勢を追加できる
 - 時間と関節角度列をうまく設定する


編集したファイルを、
choreonoid上（振り付け用のプロジェクトが良い）において、ツリー上でロボットモデルを選択して、
以下から読み込むことができる
~~~
File -> Open -> Pose Sequence
~~~

## python インターフェース 

### ROS Topics

トピックを確認できる
~~~
$ rostopic list
~~~

~~~
## Acceleration sensor / Gyro Sensor
/AizuSpiderBB/CHASSIS_ACCELERATION_SENSOR
/AizuSpiderBB/CHASSIS_RATE_GYRO_SENSOR
## Camera Image
/AizuSpiderBB/ARM_CAMERA/image
/AizuSpiderBB/BACK_CAMERA/image
/AizuSpiderBB/FRONT_CAMERA/image
/AizuSpiderBB/LEFT_CAMERA/image
/AizuSpiderBB/RIGHT_CAMERA/image
## Joint Trajectory Action
/AizuSpiderBB/fullbody_controller/command
/AizuSpiderBB/fullbody_controller/follow_joint_trajectory/cancel
/AizuSpiderBB/fullbody_controller/follow_joint_trajectory/feedback
/AizuSpiderBB/fullbody_controller/follow_joint_trajectory/goal
/AizuSpiderBB/fullbody_controller/follow_joint_trajectory/result
/AizuSpiderBB/fullbody_controller/follow_joint_trajectory/status
/AizuSpiderBB/fullbody_controller/state
## Joint States
/AizuSpiderBB/joint_states
~~~

- Joint Trajectory Action

### JAXON

~~~
$ exec.sh
$$ hrpsyspy --robot 'JAXON_RED(Robot)0'
$$ hcf.abc_svc.goPos(1, 0, 0) ## 1m 前方に進む
~~~

以下にいろいろな関数が定義されている
https://github.com/fkanehiro/hrpsys-base/blob/master/python/hrpsys_config.py


## euslispインターフェース

### AizuSpider
~~~
$ exec.sh
$ roscd aizuspider_description
$ roseus aizuspider-interface.l
roseus$ (aizuspider-init)
roseus$ (irtviewer (list *robot*))
roseus$ (send *ri* :angle-vector (send *robot* :angle-vector) 5000)
~~~

### JAXON
~~~
$ exec.sh
$ roscd hrpsys_choreonoid_tutorials/euslisp
$ roseus jaxon_jvrc-interface.l
roseus$ (jaxon_jvrc-init)
roseus$ (irtviewer (list *robot*))
roseus$ (send *ri* :angle-vector (send *robot* :angle-vector) 5000)
~~~

see https://github.com/YoheiKakiuchi/robotsimulation-docker/tree/master/choreonoid_docker

# OLD INFORMATION: (5/8締め切り) エージェントシステム課題１回目

課題は 「Choreonoidの振り付けする」　もしくは　「Dockerでシミュレーションを動かす」のいずれかを提出してください

https://github.com/agent-system/lecture2019/blob/master/documents/%E3%82%A8%E3%83%BC%E3%82%B8%E3%82%A7%E3%83%B3%E3%83%88%E3%82%B7%E3%82%B9%E3%83%86%E3%83%A020190424_docker.pdf


