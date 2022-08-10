import gphoto2 as gp
context = gp.Context()
camera = gp.check_result(gp.gp_camera_new())
gp.check_result(gp.gp_camera_init(camera, context))
text = gp.check_result(gp.gp_camera_get_summary(camera, context))
print(str(text))
camera.exit(context)
