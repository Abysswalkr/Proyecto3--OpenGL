class Obj(object):
	def __init__(self, filename):
		# Abrimos el archivo .obj y leemos todas las líneas
		with open(filename, "r") as file:
			lines = file.read().splitlines()

		# Inicializamos las listas para vértices, coordenadas de textura, normales y caras
		self.vertices = []
		self.texCoords = []
		self.normals = []
		self.faces = []

		for line in lines:
			# Limpiar espacios en blanco al final de la línea
			line = line.strip()

			# Ignorar líneas en blanco o comentarios
			if not line or line.startswith("#"):
				continue

			# Intentar dividir la línea en prefijo y valor
			try:
				prefix, value = line.split(" ", 1)
			except ValueError:
				continue  # Si no se puede dividir, pasar a la siguiente línea

			# Parsear cada línea según el prefijo
			if prefix == "v":  # Vértices
				try:
					vert = list(map(float, value.split()))
					self.vertices.append(vert)
				except ValueError:
					print(f"Error al convertir vértice en línea: {line}")

			elif prefix == "vt":  # Coordenadas de textura
				try:
					vts = list(map(float, value.split()))
					self.texCoords.append([vts[0], vts[1]])
				except ValueError:
					print(f"Error al convertir coordenada de textura en línea: {line}")

			elif prefix == "vn":  # Normales
				try:
					norm = list(map(float, value.split()))
					self.normals.append(norm)
				except ValueError:
					print(f"Error al convertir normal en línea: {line}")

			elif prefix == "f":  # Caras
				face = []
				verts = value.split()
				for vert in verts:
					try:
						# Divide el valor en índices de vértices, texturas y normales
						vert = list(map(int, vert.split("/")))
						face.append(vert)
					except ValueError:
						print(f"Error al convertir cara en línea: {line}")
				self.faces.append(face)
