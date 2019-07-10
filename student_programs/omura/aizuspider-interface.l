(require :aizuspider "package://aizuspider_description/AizuSpiderSS.l")
(require :robot-interface "package://pr2eus/robot-interface.l")

(defclass aizuspider-interface
  ;;:super robot-move-base-interface
  :super robot-interface
  ;; :slots ()
  :slots (trans_x trans_y trans_z rot_x rot_y rot_z rot_w tm joy-pub cmd-pub)
  )
(defmethod aizuspider-interface
  (:init
   (&rest args)
   (let ((r (instance AizuSpiderSS-robot :init)))
     ;; make controller configuration from joint-list
     #|
     (dolist (limb (list 'rarm 'lleg 'rleg))
       (let ((key (intern (string limb) *keyword-package*))
             (mname (intern (string-upcase (format nil "~A-controller" limb)) *keyword-package*))
             )
         ;;
         (eval
          `(defmethod aizuspider-interface
             (,mname
              nil
              (list
               (list
                (cons :controller-action ,(format nil "~A_controller/follow_joint_trajectory" limb) )
                (cons :controller-state  ,(format nil "~A_controller/state" limb) )
                (cons :action-type control_msgs::FollowJointTrajectoryAction)
                (cons :joint-names
                      ',(mapcar #'(lambda (j) (send j :name)) (send r key :joint-list)) )
                )
               )))
          )
         ))
     |#
     ;;
     (send-super*
      :init
      :robot r
      ;; :namespace "AizuSpider"
      ;; :move-base-action-name "move_base"
      ;; :base-frame-id "/base_link"
      ;; :odom-topic "/odom"
      :groupname "aizuspider_interface" args)
     )
   ;;
   #|
   (dolist (ct (list :rarm-controller
                     :rleg-controller
                     :lleg-controller))
     (send self :add-controller ct :create-actions nil))
   |#

   (setq joy-pub (format nil "~A/joy" namespace))
   (setq cmd-pub (format nil "~A/cmd_vel" namespace))
   (ros::advertise joy-pub sensor_msgs::Joy 10)
   (ros::advertise cmd-pub geometry_msgs::Twist 10)
   (ros::subscribe (format nil "~A/ground_truth_pose" namespace) geometry_msgs::PoseStamped #'send self :pose-cb)
   (setq trans_x 0.0)
   (setq trans_y 0.0)
   (setq trans_z 0.0)
   (setq rot_x 0.0)
   (setq rot_y 0.0)
   (setq rot_z 0.0)
   (setq rot_w 0.0)
   (setq tm nil)
   )
  ;;
  #|
  (:default-controller nil
   (append (send self :rarm-controller)
           (send self :rleg-controller)
           (send self :lleg-controller))
   )
  |#
  (:default-controller nil
   (list
    (list
     (cons :controller-action "fullbody_controller/follow_joint_trajectory")
     (cons :controller-state  "fullbody_controller/state")
     (cons :action-type control_msgs::FollowJointTrajectoryAction)
     (cons :joint-names (list "FR_FLIPPER" "FL_FLIPPER" "BR_FLIPPER" "BL_FLIPPER"
                              "SHOULDER" "ARM" "FOREARM" "WRIST1" "WRIST2" "HAND"
                              "FINGER1" "FINGER2" "FINGER3"
                              ))
     ))
   )
  #|
  (:rarm-controller nil
   (list
    (list
     (cons :controller-action "rarm_controller/follow_joint_trajectory")
     (cons :controller-state  "rarm_controller/state")
     (cons :action-type control_msgs::FollowJointTrajectoryAction)
     (cons :joint-names (list "r_shoulder_p_joint" "r_shoulder_r_joint" "r_shoulder_y_joint"
                              "r_elbow_joint" "r_wrist_y_joint" "r_wrist_p_joint" "r_wrist_r_joint"
                              "r_hand_y_joint"
                              ))
     ))
   )
  (:larm-controller nil
   (list
    (list
     (cons :controller-action "larm_controller/follow_joint_trajectory")
     (cons :controller-state  "larm_controller/state")
     (cons :action-type control_msgs::FollowJointTrajectoryAction)
     (cons :joint-names (list "l_shoulder_p_joint" "l_shoulder_r_joint" "l_shoulder_y_joint"
                              "l_elbow_joint" "l_wrist_y_joint" "l_wrist_p_joint" "l_wrist_r_joint"
                              "l_hand_y_joint"
                              ))
     ))
   )
  |#
  (:start-grasp
   (&rest args &key (tm 1000) (position 90) &allow-other-keys)
   (let ((av (send self :state :reference-vector)))
     (setf (elt av 6) position)
     (setf (elt av 7) position)
     (setf (elt av 8) position)
     (send *ri* :angle-vector av tm)
     ))
  (:stop-grasp
   (&rest args &key (tm 1000) &allow-other-keys)
   (let ((av (send self :state :reference-vector)))
     (setf (elt av 6) 0)
     (setf (elt av 7) 0)
     (setf (elt av 8) 0)
     (send *ri* :angle-vector av tm)
   ))
  (:pose-cb
   (msg)
   (setq tm (send msg :header :stamp))
   (setq trans_x (send msg :pose :position :x))
   (setq trans_y (send msg :pose :position :y))
   (setq trans_z (send msg :pose :position :z))
   (setq rot_x (send msg :pose :orientation :x))
   (setq rot_y (send msg :pose :orientation :y))
   (setq rot_z (send msg :pose :orientation :z))
   (setq rot_w (send msg :pose :orientation :w))
   )
  (:move-pub
   (trans rot)
   (let* ((msg (instance sensor_msgs::Joy :init
                         :axes (float-vector 0 0 0 0 0 0 0 0)
                         :buttons '(0 0 0 0 0 0 0 0 0 0 0)))
          (cmd (instance geometry_msgs::Twist :init))
          )
     (cond ((> trans 0.0)
            (setf (aref (send msg :axes) 1) -1))
           ((< trans 0.0)
            (setf (aref (send msg :axes) 1) 1)))
     (cond ((> rot 0.0)
            (setf (aref (send msg :axes) 0) -1))
           ((< rot 0.0)
            (setf (aref (send msg :axes) 0) 1)))
     (ros::publish joy-pub msg)
     (cond ((/= trans 0.0)
            (send cmd :linear :x (/ (* 2.0 trans) (float (abs trans)))))
           ((/= rot 0.0)
            (send cmd :angular :z (/ (* 0.5 rot) (float (abs rot))))))
     (ros::publish cmd-pub cmd)
     )
   )
  (:stop-pub
   ()
   (let* ((msg (instance sensor_msgs::Joy :init
                         :axes (float-vector 0 0 0 0 0 0 0 0)
                         :buttons '(0 0 0 0 0 0 0 0 0 0 0)))
          (cmd (instance geometry_msgs::Twist :init))
         )
     (ros::publish joy-pub msg)
     (ros::publish cmd-pub cmd)
     )
   )
  (:go-pos
   (x y rota)
   (let* ((origin-pos (float-vector trans_x trans_y trans_z))
          (origin-rot (float-vector rot_w rot_x rot_y rot_z))
          (pos (float-vector trans_x trans_y trans_z))
          (rot (float-vector rot_w rot_x rot_y rot_z))
          (diff-pos (float-vector 0 0 0))
          (diff-len 0)
          (diff-rot 0)
          (ang (atan2 (float y) (float x)))
          (trans (norm (float-vector x y)))
          (rotation rota)
          )
     (when (> ang pi/2)
       (setq ang (- ang pi))
       (setq trans (- trans))
       )
     (when (< ang -pi/2)
       (setq ang (+ ang pi))
       (setq trans (- trans))
       )
     (if (or (> rotation pi) (< rotation -pi))
       (setq rotation (mod rotation pi)))
     (ros::spin-once)
     (setq origin-pos (float-vector trans_x trans_y trans_z))
     (setq origin-rot (float-vector rot_w rot_x rot_y rot_z))
     (send self :move-pub 0 ang)
     (while (< diff-rot (abs ang))
       (unix:usleep (* 1000 10))
       (ros::spin-once)
       (setq pos (float-vector trans_x trans_y trans_z))
       (setq rot (float-vector rot_w rot_x rot_y rot_z))
       (setq diff-pos (v- pos origin-pos))
       (setq diff-len (norm diff-pos))
       (setq diff-rot (* (- (atan2 (aref rot 3) (aref rot 0)) (atan2 (aref origin-rot 3) (aref origin-rot 0))) 2.0))
       (if (> diff-rot pi) (setq diff-rot (- diff-rot pi)))
       (if (< diff-rot -pi) (setq diff-rot (+ diff-rot pi)))
       (setq diff-rot (abs diff-rot))
       )
     (send self :stop-pub)

     (setq diff-pos (float-vector 0 0 0))
     (setq diff-len 0)
     (setq diff-rot 0)
     (ros::spin-once)
     (setq origin-pos (float-vector trans_x trans_y trans_z))
     (setq origin-rot (float-vector rot_w rot_x rot_y rot_z))
     (send self :move-pub trans 0)
     (while (< diff-len (abs trans))
       (unix:usleep (* 1000 10))
       (ros::spin-once)
       (setq pos (float-vector trans_x trans_y trans_z))
       (setq rot (float-vector rot_w rot_x rot_y rot_z))
       (setq diff-pos (v- pos origin-pos))
       (setq diff-len (norm diff-pos))
       (setq diff-rot (* (- (atan2 (aref rot 3) (aref rot 0)) (atan2 (aref origin-rot 3) (aref origin-rot 0))) 2.0))
       (if (> diff-rot pi) (setq diff-rot (- diff-rot pi)))
       (if (< diff-rot -pi) (setq diff-rot (+ diff-rot pi)))
       (setq diff-rot (abs diff-rot))
       )
     (send self :stop-pub)

     (setq diff-pos (float-vector 0 0 0))
     (setq diff-len 0)
     (setq diff-rot 0)
     (ros::spin-once)
     (setq origin-pos (float-vector trans_x trans_y trans_z))
     (setq origin-rot (float-vector rot_w rot_x rot_y rot_z))
     (send self :move-pub 0 (- rotation ang))
     (while (< diff-rot (abs (- rotation ang)))
       (unix:usleep (* 1000 10))
       (ros::spin-once)
       (setq pos (float-vector trans_x trans_y trans_z))
       (setq rot (float-vector rot_w rot_x rot_y rot_z))
       (setq diff-pos (v- pos origin-pos))
       (setq diff-len (norm diff-pos))
       (setq diff-rot (* (- (atan2 (aref rot 3) (aref rot 0)) (atan2 (aref origin-rot 3) (aref origin-rot 0))) 2.0))
       (if (> diff-rot pi) (setq diff-rot (- diff-rot pi)))
       (if (< diff-rot -pi) (setq diff-rot (+ diff-rot pi)))
       (setq diff-rot (abs diff-rot))
       )
     (send self :stop-pub)
     )
   )
  )

(defun aizuspider-init (&rest args &key (namespace "AizuSpider") &allow-other-keys)
  (if (not (boundp '*ri*))
      (setq *ri* (instance* aizuspider-interface :init
                            :namespace namespace args)))
  (if (not (boundp '*robot*))
      (setq *robot* (AizuSpiderSS)))
  )

;;;;; okiagari functions (thanks to Iori Yanokura[https://github.com/iory] )
(defun okiagari-right ()
  ;; reset pose
  (send *robot* :reset-pose)
  (send *ri* :angle-vector (send *robot* :angle-vector) 1000)
  (send *ri* :wait-interpolation)
  ;;
  (send *robot* :rarm :move-end-pos #f(0 -500 -300))
  (send *ri* :angle-vector
        (send *robota* :angle-vector) 100);;??
  (send *ri* :wait-interpolation)
  ;;
  (send *robot* :reset-pose)
  (send *ri* :angle-vector (send *robot* :angle-vector) 1000)
  (send *ri* :wait-interpolation)
  )
(defun okiagari-left ()
  ;; reset pose
  (send *robot* :reset-pose)
  (send *ri* :angle-vector (send *robot* :angle-vector) 1000)
  (send *ri* :wait-interpolation)
  ;;
  (send *robot* :rarm :move-end-pos #f(0 -500 -300))
  (send *ri* :angle-vector
        (send *robota* :angle-vector) 100);;??
  (send *ri* :wait-interpolation)
  ;;
  (send *robota* :rarm :move-end-pos #f(0 0 -200))
  (send *robota* :forearm :joint-angle 90)
  (send *ri* :angle-vector
        (send *robota* :angle-vector) 100);;??
  (send *ri* :wait-interpolation)
  ;;
  (send *robot* :reset-pose)
  (send *ri* :angle-vector (send *robot* :angle-vector) 1000)
  (send *ri* :wait-interpolation)
  )
;;;;;


;; #f(-90.0 90.0 50.0 180.0 0.0 90.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0)
