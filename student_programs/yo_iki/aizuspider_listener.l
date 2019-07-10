#!/usr/bin/env roseus
(require "aizuspider-init.l")
(require "models/arrow-object")
(load "test.l")

;(ros::roseus "listener")
(defclass pose-cb-class
  :super propertied-object
  :slots (arr command))
  (defmethod pose-cb-class
  (:init ()
    (objects (setq arr (arrow)))
    (ros::subscribe "target_pose" geometry_msgs::PoseStamped #'send self :pose-cb)
    (ros::subscribe "command" std_msgs::String #'send self :command-cb))
  (:pose-cb (msg)
    (send arr :newcoords (ros::tf-pose-stamped->coords msg))
    (ros::ros-info "Get pose ~a" arr))
  (:command-cb (msg)
    (setq command (send msg :data))
    (ros::ros-info "Get command ~a" command))
  (:arr () arr)
  (:command () command)
  (:reset-command () (setq command "")))

;(defun init-pose())

(setq *release-av* #f(-70 120 100 -60.0 60.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0 0.0))
(setq *cube* (make-cube 1 1 1))
(setq *face-count* 5)

(defun start ()
  (do-until-key
    (send m :reset-command)
    (ros::spin-once)
    (objects (list *cube* *a* *robot*))
    (cond
      ((equal (send m :command) "MANIP")
        (send *robot* :reset-manip-pose)
        (send-ri :grasp t))
      ((equal (send m :command) "RELEASE")
        (send *robot* :angle-vector *release-av*)
        (send-ri :grasp t)
        (send *ri* :wait-interpolation)
        (send-ri :grasp nil)
        (send *ri* :wait-interpolation)
        (send *robot* :reset-manip-pose)
        (send-ri :grasp nil))
      ((equal (send m :command) "PREVIEW")
        (send *robot* :rarm :inverse-kinematics (send m :arr)))
      ((equal (send m :command) "EXECUTE")
        (send-ri :grasp nil)
        (send *ri* :wait-interpolation)
        (send-ri :grasp t))
      ((equal (send m :command) "CANCEL")
        (send-ri :grasp nil)
        (send *ri* :wait-interpolation)
        (send *robot* :reset-manip-pose)
        (send-ri :grasp nil))
      ((equal (send m :command) "SELECT")
        (view-box (one-shot-subscribe "/selected_bbox"
                  jsk_recognition_msgs::BoundingBox))
        (setq *face-count* 0)
        (set-face 0)
        (ros::publish "set_pose" (ros::coords->tf-pose-stamped
          (send *a* :worldcoords) "AizuSpiderAA/CHASSIS"))
        (ros::sleep))
      ((equal (send m :command) "ADJUST")
        (setq *face-count* (1+ *face-count*))
        (if (> *face-count* 5)
          (setq *face-count* 0))
        (set-face *face-count*)
        (ros::publish "set_pose" (ros::coords->tf-pose-stamped
          (send *a* :worldcoords) "AizuSpiderAA/CHASSIS"))
        (ros::sleep)))
  ))

;(defun start ()
;  (do-until-key
;    (send m :reset-command)
;    (ros::spin-once)
;    (send *irtviewer* :draw-objects)
;    (send *robot* :rarm :inverse-kinematics (send m :arr))
;    (if (equal (send m :command) "EXECUTE")
;      (send-ri)
;      (if (equal (send m :command) "CANCEL")
;        (return nil))))
;)

;(defun send-ri ()
;  (send *ri* :angle-vector (send *robot* :angle-vector) 5000)
;  (send *ri* :wait-interpolation))

(setq m (instance pose-cb-class :init))
(ros::advertise "set_pose" geometry_msgs::PoseStamped 1)
(ros::rate 100)
(start)

;robot_state_publisher
;joint_state_publisher
