extends Node3D

var board: RigidBody3D
var stones: Array[RigidBody3D] = []

func _ready():
	# камера
	var cam := Camera3D.new()
	cam.position = Vector3(0, 4, 4)
	cam.look_at(Vector3.ZERO)
	add_child(cam)

	# свет
	var light := OmniLight3D.new()
	light.position = Vector3(0, 2, 0)
	light.light_energy = 3.0
	light.omni_range = 8.0
	add_child(light)

	# доска
	board = RigidBody3D.new()
	board.gravity_scale = 0
	var bmesh := MeshInstance3D.new()
	var box := BoxMesh.new()
	box.size = Vector3(2, 0.1, 2)
	bmesh.mesh = box
	board.add_child(bmesh)
	var bcol := CollisionShape3D.new()
	var bshape := BoxShape3D.new()
	bshape.size = Vector3(2, 0.1, 2)
	bcol.shape = bshape
	board.add_child(bcol)
	add_child(board)

	# камни
	for i in 6:
		var s := RigidBody3D.new()
		s.mass = 0.2
		s.position = Vector3(randf_range(-0.6, 0.6), 0.3, randf_range(-0.6, 0.6))
		var smesh := MeshInstance3D.new()
		var sphere := SphereMesh.new()
		sphere.radius = 0.15
		sphere.height = 0.3
		smesh.mesh = sphere
		s.add_child(smesh)
		var scol := CollisionShape3D.new()
		var sshape := SphereShape3D.new()
		sshape.radius = 0.15
		scol.shape = sshape
		s.add_child(scol)
		add_child(s)
		stones.append(s)

func _process(delta):
	var a := Input.get_accelerometer()
	board.rotation.x = lerpf(board.rotation.x, clampf(a.y, -1, 1) * 0.4, delta * 6)
	board.rotation.z = lerpf(board.rotation.z, clampf(-a.x, -1, 1) * 0.4, delta * 6)
	for s in stones:
		if s.position.y < -2:
			s.linear_velocity = Vector3.ZERO
			s.position = Vector3(randf_range(-0.5, 0.5), 0.3, randf_range(-0.5, 0.5))
