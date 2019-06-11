(load "package://hrpsys_ros_bridge_tutorials/euslisp/jaxon_red-interface.l")
(jaxon_red-init)
(setq *robot* *jaxon_red*)

(send *ri* :go-pos 0 1.5 0)
(send *ri* :go-pos 10.6 0 0)

(let ((coords (make-coords :pos #f(400 400 1000) :rpy (float-vector 0 0 pi/2))))
  (objects (list coords *robot*))

  (send *ri* :stop-grasp)
  (send *ri* :wait-interpolation)
  
  (send *robot* :fix-leg-to-coords (make-coords))
  (send *robot* :larm :inverse-kinematics (send (send coords :copy-worldcoords) :move-to (make-coords :pos #f(-50 0 0))))
  (send *ri* :angle-vector (send *robot* :angle-vector) 2000)
  (send *ri* :wait-interpolation)

  (send *robot* :fix-leg-to-coords (make-coords))
  (send *robot* :larm :inverse-kinematics (send (send coords :copy-worldcoords) :move-to (make-coords :pos #f(140 0 0))))
  (send *ri* :angle-vector (send *robot* :angle-vector) 1000)
  (send *ri* :wait-interpolation)

  (send *ri* :start-grasp)
  ;;(send *ri* :wait-interpolation)  
  )  

(send *ri* :go-pos 0 -2.5 0)
(send *ri* :stop-grasp)
(send *ri* :wait-interpolation)
(send *ri* :angle-vector (send *robot* :reset-pose) 2000)


;;(send *ri* :set-auto-balancer-param :is-hand-fix-mode t)
