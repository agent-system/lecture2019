(load "package://hrpsys_ros_bridge_tutorials/euslisp/jaxon_red-interface.l")
(jaxon_red-init)
(setq *robot* *jaxon_red*)

(send *robot* :fix-leg-to-coords (make-coords))
(let* ((rarm-coords (make-coords :pos #f(500 -350 300)))
       (larm-coords (make-coords :pos #f(500 350 300)))
       (move-target
	(list (send *robot* :rleg :end-coords)
	      (send *robot* :lleg :end-coords)
	      (send *robot* :rarm :end-coords)
	      (send *robot* :larm :end-coords)
	      ))
       (target-coords
	(list (send *robot* :rleg :end-coords :copy-worldcoords)
	      (send *robot* :lleg :end-coords :copy-worldcoords)
	      rarm-coords
	      larm-coords
	      ))
       (link-list
	(mapcar #'(lambda (limb)
		    (send *robot* :link-list (send limb :parent))) move-target)))

  (objects (list *robot* rarm-coords larm-coords))
  (send *robot* :fullbody-inverse-kinematics target-coords
	:move-target move-target
	:link-list link-list
	)
  
  (send *ri* :angle-vector (send *robot* :angle-vector))
  (send *ri* :wait-interpolation)
  )

(send *ri* :go-pos 3 0 0)
