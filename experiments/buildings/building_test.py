import xml.etree.cElementTree as ET

class Building:
    name = ""
    x = 0
    y = 0
    size = 1
    height = 2

    def __init__(self, name):
        self.name = name

def main():
    xmlData = writeWorld()
    f = open('test.sdf', 'w')
    f.write(xmlData)
    f.close()
    print 'Done.'

def genBuildingMatrix(startX, startY, rows):
    '''
    Generate a square matrix of buildings of the given size
    '''
    text = ""
    size = 1
    height = 3
    for y in range(rows):
        for x in range(rows):
            name = "building_%d_%d" % (x, y)
            b = Building(name)
            b.size = size
            b.height = height
            b.x = startX + x * size * 1.5
            b.y = startY + y * size * 1.5
            text += writeBuilding(b)
    return text


def writeWorld():
    xmlText = '<?xml version="1.0" ?>\n'
    xmlText += '<sdf version="1.4">\n'
    xmlText += '  <world name="default">\n'
    xmlText += writeScene()
    xmlText += writePhysics()
    xmlText += writeSunLight()
    xmlText += writeGroundPlaneModel()
    xmlText += genBuildingMatrix(0, 0, 10)
    xmlText += '  </world>\n</sdf>'
    return xmlText

def writeBuilding(building):
    return writeBoxModel(building.name, building.x, building.y, 0, building.size, building.size, building.height)

def writeScene():
    text = '<scene>\n'
    text += '  <ambient>1.0 1.0 1.0 1</ambient>\n'
    text += '  <background>0 0 0 1.0</background>\n'
    text += '  <shadows>true</shadows>\n'
    text += '</scene>\n'
    return text

def writePhysics():
    text = '<physics type="ode">\n'
    text += '  <gravity>0 0 -10.0</gravity>\n'
    text += '  <ode>\n'
    text += '    <solver>\n'
    text += '      <type>quick</type>\n'
    text += '      <iters>1000</iters>\n'
    text += '      <sor>1.3</sor>\n'
    text += '    </solver>\n'
    text += '    <constraints>\n'
    text += '      <cfm>0.0</cfm>\n'
    text += '      <erp>1.0</erp>\n'
    text += '      <contact_max_correcting_vel>0.0</contact_max_correcting_vel>\n'
    text += '      <contact_surface_layer>0.0</contact_surface_layer>\n'
    text += '    </constraints>\n'
    text += '  </ode>\n'
    text += '  <max_step_size>0.001</max_step_size>\n'
    text += '</physics>\n'
    text += '<include>\n'
    text += '  <uri>model://ground_plane</uri>\n'
    text += '</include>\n'
    return text

def writeBoxModel(name, x, y, z, w, l, h):
    text = "<model name='%s'>\n" % name
    text += "  <pose>%f %f %f 0 -0 0</pose>\n" % (x, y, z)
    text += "  <link name='link'>\n"
    text += "    <inertial>\n"
    text += "      <mass>1</mass>\n"
    text += "      <inertia>\n"
    text += "        <ixx>1</ixx>\n"
    text += "        <ixy>0</ixy>\n"
    text += "        <ixz>0</ixz>\n"
    text += "        <iyy>1</iyy>\n"
    text += "        <iyz>0</iyz>\n"
    text += "        <izz>1</izz>\n"
    text += "      </inertia>\n"
    text += "    </inertial>\n"
    text += "    <collision name='collision'>\n"
    text += "      <geometry>\n"
    text += "        <box>\n"
    text += "          <size>1 1 1</size>\n"
    text += "        </box>\n"
    text += "      </geometry>\n"
    text += "      <max_contacts>10</max_contacts>\n"
    text += "      <surface>\n"
    text += "        <bounce/>\n"
    text += "        <friction>\n"
    text += "          <ode/>\n"
    text += "        </friction>\n"
    text += "        <contact>\n"
    text += "          <ode/>\n"
    text += "        </contact>\n"
    text += "      </surface>\n"
    text += "    </collision>\n"
    text += "    <visual name='visual'>\n"
    text += "      <geometry>\n"
    text += "        <box>\n"
    text += "          <size>%f %f %f</size>\n" % (w, l, h)
    text += "        </box>\n"
    text += "      </geometry>\n"
    text += "      <material>\n"
    text += "        <script>\n"
    text += "          <uri>file://media/materials/scripts/gazebo.material</uri>\n"
    text += "          <name>Gazebo/Grey</name>\n"
    text += "        </script>\n"
    text += "      </material>\n"
    text += "    </visual>\n"
    text += "    <velocity_decay>\n"
    text += "      <linear>0</linear>\n"
    text += "      <angular>0</angular>\n"
    text += "    </velocity_decay>\n"
    text += "    <self_collide>0</self_collide>\n"
    text += "    <kinematic>0</kinematic>\n"
    text += "    <gravity>1</gravity>\n"
    text += "  </link>\n"
    text += "  <static>0</static>\n"
    text += "</model>\n"
    return text

def writeGroundPlaneModel():
    text = "<model name='ground_plane'>\n"
    text += "  <static>1</static>\n"
    text += "  <link name='link'>\n"
    text += "    <collision name='collision'>\n"
    text += "      <geometry>\n"
    text += "        <plane>\n"
    text += "          <normal>0 0 1</normal>\n"
    text += "          <size>100 100</size>\n"
    text += "        </plane>\n"
    text += "      </geometry>\n"
    text += "      <surface>\n"
    text += "        <friction>\n"
    text += "          <ode>\n"
    text += "            <mu>100</mu>\n"
    text += "            <mu2>100</mu2>\n"
    text += "          </ode>\n"
    text += "        </friction>\n"
    text += "        <bounce/>\n"
    text += "        <contact>\n"
    text += "          <ode/>\n"
    text += "        </contact>\n"
    text += "      </surface>\n"
    text += "      <max_contacts>10</max_contacts>\n"
    text += "    </collision>\n"
    text += "    <visual name='visual'>\n"
    text += "      <cast_shadows>0</cast_shadows>\n"
    text += "      <geometry>\n"
    text += "        <plane>\n"
    text += "          <normal>0 0 1</normal>\n"
    text += "          <size>100 100</size>\n"
    text += "        </plane>\n"
    text += "      </geometry>\n"
    text += "      <material>\n"
    text += "        <script>\n"
    text += "          <uri>file://media/materials/scripts/gazebo.material</uri>\n"
    text += "          <name>Gazebo/Grey</name>\n"
    text += "        </script>\n"
    text += "      </material>\n"
    text += "    </visual>\n"
    text += "    <velocity_decay>\n"
    text += "      <linear>0</linear>\n"
    text += "      <angular>0</angular>\n"
    text += "    </velocity_decay>\n"
    text += "    <self_collide>0</self_collide>\n"
    text += "    <kinematic>0</kinematic>\n"
    text += "    <gravity>1</gravity>\n"
    text += "  </link>\n"
    text += "</model>\n"
    return text

def writeSunLight():
    text = "<light name='sun' type='directional'>\n"
    text += "  <cast_shadows>1</cast_shadows>\n"
    text += "  <pose>0 0 10 0 -0 0</pose>\n"
    text += "  <diffuse>0.8 0.8 0.8 1</diffuse>\n"
    text += "  <specular>0.2 0.2 0.2 1</specular>\n"
    text += "  <attenuation>\n"
    text += "    <range>1000</range>\n"
    text += "    <constant>0.9</constant>\n"
    text += "    <linear>0.01</linear>\n"
    text += "    <quadratic>0.001</quadratic>\n"
    text += "  </attenuation>\n"
    text += "  <direction>-0.5 0.1 -0.9</direction>\n"
    text += "</light>\n"
    return text

if (__name__ == "__main__"):
    main()
