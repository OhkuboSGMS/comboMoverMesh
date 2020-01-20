import numpy as np
from mayavi import mlab

nx, ny = (10, 5)
dx, dy = (1.0 / nx/6, 1.0 / ny/5)
xRange = np.linspace(0, 1, nx)
yRange = np.linspace(0, 1, ny)

# Generate All Points
xPoints, yPoints = np.meshgrid(xRange, yRange, indexing="ij")
points = []  # TODO 配列からマトリックスに ndenumerate
for x_idx in range(nx):
    for y_idx in range(ny):
        point = (xPoints[x_idx, y_idx], yPoints[x_idx, y_idx])
        print(xPoints[x_idx, y_idx], yPoints[x_idx, y_idx])
        points.append(point)

triangles = []
# Connect Side Points
for x_idx in range(nx-1):
    x_idx =x_idx+1
    for y_idx in range(ny):
        if x_idx <= nx  and y_idx < ny-1 :  # points index connection 時計回り
            triangles.append((x_idx * ny + y_idx, (x_idx -1) * ny + y_idx, (x_idx -1) * ny + y_idx + 1))
        if x_idx > 0 and y_idx < ny-1:  # point index connection 時計回り
            triangles.append((x_idx * ny + y_idx, x_idx * ny + y_idx + 1, (x_idx - 1) * ny + y_idx + 1))
# print(points)
# Vibrate inner points;
for x_idx in range(nx):
    for y_idx in range(ny):
        if 0 < x_idx < nx - 1 and 0 < y_idx < ny - 1:
            # print(points[x_idx * ny + y_idx])
            x, y = points[x_idx * ny + y_idx]
            points[x_idx * ny + y_idx] = (np.random.randn() * dx + x, np.random.randn() * dy + y)
            # print("Changed",points[x_idx * ny + y_idx])

points = np.array(points)
triangles = np.array(triangles)
print("Points", points.shape)
print("Tri", triangles.shape)
print(triangles)
# print(points)
x = np.array(list(map(lambda xy: xy[0], points)))
y = np.array(list(map(lambda xy: xy[1], points)))
z = np.random.random(*y.shape)/20
# print(x)
# print(y)
mlab.figure(1, fgcolor=(0, 0, 0), bgcolor=(1, 1, 1))

mesh = mlab.triangular_mesh(x, y, z, triangles, )#representation="wireframe")

f = np.repeat(np.arange(0,triangles.shape[0]/2),2)#np.mean(triangles, axis=1)
print(f)
mesh.mlab_source.dataset.cell_data.scalars = f
mesh.mlab_source.dataset.cell_data.scalars.name = 'Cell data'
mesh.mlab_source.update()
mesh.parent.update()

mesh2 = mlab.pipeline.set_active_attribute(mesh,
                                           cell_scalars='Cell data')
s2 = mlab.pipeline.surface(mesh2)
mlab.view(90, 0)
mlab.show()
