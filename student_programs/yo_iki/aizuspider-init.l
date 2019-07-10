(load "package://aizuspider_description/aizuspider-interface.l")
(load "models/arrow-object.l")
(ros::load-ros-manifest "jsk_recognition_msgs")
(aizuspider-init :namespace "AizuSpiderAA")
(setq *a* (arrow))
(objects (list *robot*))
;;(send *robot* :reset-manip-pose)
;;(send *ri* :angle-vector (send *robot* :angle-vector) 5000)
;;(send *ri* :go-pos 5 -1.5 0)

;;(send *ri* :go-pos 4 0.8 0)
;;(send *ri* :go-pos 0 0 90)

(defun irt() (send *irtviewer* :draw-objects))

(defun send-robot()
  (send *robot* :angle-vector (send *ri* :state :angle-vector))
  (irt))
